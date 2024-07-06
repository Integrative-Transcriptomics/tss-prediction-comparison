import pydoc

import pandas as pd
from enum import Enum
from json import loads, dumps
from app import GFFParser as ps
import re


class TSSType(Enum):
    PRIMARY = "pTSS/sTSS"
    INTERNAL = "iTSS"
    ANTISENSE = "asTSS"
    ORPHAN = "orphan"


def extract_gene_name(attributes):
    """
    Helper function for classify. Expects a string and extracts the substring after 'Name='.
    If this pattern is not found, the function returns None.
    :param attributes
    :return: gene name
    """
    match = re.search(r'Name=([^;]+)', attributes)
    return match.group(1) if match else None


class GffFormatException(Exception):
    """Exception raised when the GFF file format is incorrect"""
    pass


def classify(gff_df, tss_list, confidence_list, strand):
    """
    Classifies TSS based on their position relative to genes in a GFF file.
    :param gff_df:  DataFrame containing information from a GFF file
    :param tss_list: a list of all predicted TSS
    :param confidence_list: list that assigns a confidence value to each of the TSS in tss_list
    :param strand: the strand on which the TSS were predicted(True for reverse and False for forward)
    :return: tss_classified: data frame that contains the position, classified type, confidence value,
    and corresponding gene name of the TSS
    """
    gff_df = ps.parse_gff_to_df(gff_df)

    tss_classified = []
    gff_df['gene name'] = gff_df['attributes'].apply(extract_gene_name)

    if gff_df['gene name'].isnull().all():
        raise GffFormatException(
            "the attributes column of your GFF file does not contain gene names in the format 'Name=..")

    gff_fw = gff_df[(gff_df['strand'] == "+")]
    gff_rv = gff_df[(gff_df['strand'] == "-")]

    distances = calculate_distances_to_next_gene(gff_df, tss_list, strand)

    for tss, confidence, distance in zip(tss_list, confidence_list, distances):

        if not strand:
            intern = gff_fw[(gff_fw['end'] >= tss) & (gff_fw['start'] <= tss)]
            prim = gff_fw[(gff_fw['start'] >= tss) & (gff_fw['start'] - 200 <= tss)]
            anti = gff_rv[(gff_rv['end'] + 100 >= tss) & (gff_rv['start'] - 100 <= tss)]

        else:
            intern = gff_rv[(gff_rv['end'] >= tss) & (gff_rv['start'] <= tss)]
            prim = gff_rv[(gff_rv['start'] >= tss) & (gff_rv['start'] - 200 <= tss)]
            anti = gff_fw[(gff_fw['end'] + 100 >= tss) & (gff_fw['start'] - 100 <= tss)]

        possible_class = []
        gene_names = []

        if not intern.empty:
            possible_class.extend([TSSType.INTERNAL.value] * len(intern))
            gene_names.extend(intern['gene name'].tolist())

        if not prim.empty:
            possible_class.extend([TSSType.PRIMARY.value] * len(prim))
            gene_names.extend(prim['gene name'].tolist())

        if not anti.empty:
            possible_class.extend([TSSType.ANTISENSE.value] * len(anti))
            gene_names.extend(anti['gene name'].tolist())

        if len(possible_class) == 0:
            possible_class = [TSSType.ORPHAN.value]
            gene_names.append(None)

        tss_classified.extend([(tss, classification, confidence, gene_name, distance) for classification, gene_name in
                               zip(possible_class, gene_names)])

    classified_df = pd.DataFrame(tss_classified, columns=['Pos', 'TSS type', 'confidence', 'gene name', 'distance'])

    return classified_df


def calculate_distances_to_next_gene(gff_df, positions, strand):
    """
    Calculates distances to the next gene in the specified direction for each position in the list.
    :param gff_df: DataFrame containing GFF file information
    :param positions: List of positions from which to calculate distances.
    :param strand: Strand direction (True for reverse, False for forward).
    :return: List of distances corresponding to each position. None is used for positions where no gene is found.
    """
    distances = []

    for pos in positions:
        if strand:
            relevant_genes = gff_df[(gff_df['strand'] == '-') & (gff_df['start'] <= pos)]
            if not relevant_genes.empty:
                next_gene = relevant_genes.loc[relevant_genes['end'].idxmax()]
                if next_gene['start'] <= pos <= next_gene['end']:
                    distance = 0
                else:
                    distance = pos - next_gene['end']
            else:
                distance = None
        else:
            relevant_genes = gff_df[(gff_df['strand'] == '+') & (gff_df['end'] >= pos)]
            if not relevant_genes.empty:
                next_gene = relevant_genes.loc[relevant_genes['start'].idxmin()]
                if next_gene['start'] <= pos <= next_gene['end']:
                    distance = 0
                else:
                    distance = next_gene['start'] - pos
            else:
                distance = None

        distances.append(distance)

    return distances


def find_common_tss(prediction, master_table, strand):
    """
    Identifies common TSS detected by TSS Predator and our prediction.
    :param prediction:  DataFrame containing the position, type, and corresponding gene name of the predicted TSS
    :param master_table: DataFrame containing the master table data generated by TSS predator
    :param strand: the strand on which the TSS were predicted(True for reverse and False for forward)
    :return: common_tss_df: data frame that holds the position, type, and corresponding gene name of the TSS that were
    found by both TSS predator and our prediction
    """
    if not strand:
        mt_relevant_columns = master_table[master_table['Strand'] == '+']

    else:
        mt_relevant_columns = master_table[master_table['Strand'] == '-']

    mt_relevant_columns = mt_relevant_columns[['Pos', 'TSS type']].reset_index(drop=True)

    expanded_prediction = pd.concat([
        prediction.assign(**{'Pos': prediction['Pos'] + offset})
        for offset in range(-5, 6)
    ])

    common_tss_df = pd.merge(expanded_prediction, mt_relevant_columns, on=['Pos', 'TSS type'],
                             how='inner').drop_duplicates()

    return common_tss_df


# fehler wenn df leer ist
def calculate_frequency_of_tss_classes(common_tss_df):
    type_counts = common_tss_df['TSS type'].value_counts()
    all_types = [e.value for e in TSSType]
    type_counts = type_counts.reindex(all_types, fill_value=0)
    total_count = type_counts.sum()
    relative_frequencies = type_counts / total_count

    return relative_frequencies


def recall_and_precision_return_obj(common_tss_df, prediction_df, master_table_df):
    result_dict = {"recall": len(common_tss_df.index) / len(master_table_df.index),
                   "precision": len(common_tss_df.index) / len(prediction_df.index)}
    result_json = loads(dumps(result_dict))
    return result_json


def freq_return_obj(common_tss_df, prediction_df, master_table_df):
    result_dict = {'common_tss': calculate_frequency_of_tss_classes(common_tss_df).to_dict(),
                   'prediction': calculate_frequency_of_tss_classes(prediction_df).to_dict(),
                   'TSS_predator': calculate_frequency_of_tss_classes(master_table_df).to_dict()}
    result_json = loads(dumps(result_dict))
    return result_json



'''
mt = {
    'Pos': [25675, 31366, 31650, 32000, 405, 400],
    'TSS type': ["iTSS", "asTSS", "pTSS/sTSS", "asTSS", "iTSS", "pTSS/sTSS"],
    'detected': ['1', '1', '1', '0', '1', '1'],
    'Locus_tag': ['esdnc', 'aada', 'Wqwq', 'wwisd', 'wwisd', 'wwisd'],
    'Strand': ["+", "-", "+", "+", "+", "+"]
}

df = pd.DataFrame(mt)

cl = classify("../tests/test_files/NC_004703.gff", [400, 25675, 31362, 31650], [0.9, 0.5, 0.7, 0.8], False)
print(cl)
co = find_common_tss(cl, df, False)
print(co)
with open("csv_file", 'w', newline='') as f:
    cl.to_csv(f, index=False)'''

#print(freq_return_obj(cl, co, df))
#print(recall_and_precision_return_obj(co, cl, df))
