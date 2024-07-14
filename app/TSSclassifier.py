import pydoc

import pandas as pd
from enum import Enum
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


def prepare_gff(gff_df):
    """
        adds a column gene name to the data frame and splits it into two dfs gff_forward and gff_reverse
        :param gff_df: DataFrame containing information from a GFF file
        :return: gff_fw, gff_rv
        """
    gff_df['gene name'] = gff_df['attributes'].apply(extract_gene_name)

    if gff_df['gene name'].isnull().all():
        raise GffFormatException(
            "the attributes column of your GFF file does not contain gene names in the format 'Name=..")

    gff_fw = gff_df[(gff_df['strand'] == "+")]
    gff_rv = gff_df[(gff_df['strand'] == "-")]

    return gff_fw, gff_rv


def assign_tss_class(tss, confidence, distance, gff_fw, gff_rv, strand):
    """
    assigns a tss type to the tss
    :param tss: the predicted TSS
    :param confidence: the confidence value with which the TSS was predicted
    :param distance: Distance to the next gene.
    :param gff_fw: DataFrame for forward strand genes of the given gff.
    :param gff_rv: DataFrame for reverse strand genes of the given gff.
    :param strand: the strand on which the TSS was predicted(True for reverse and False for forward)
    :return:List of classified TSS records.
    """
    if not strand:
        intern = gff_fw[(gff_fw['end'] >= tss) & (gff_fw['start'] <= tss)]
        prim = gff_fw[(gff_fw['start'] > tss) & (gff_fw['start'] - 300 <= tss)]
        anti = gff_rv[(gff_rv['end'] + 100 >= tss) & (gff_rv['start'] - 100 <= tss)]

    else:
        intern = gff_rv[(gff_rv['end'] >= tss) & (gff_rv['start'] <= tss)]
        prim = gff_rv[(gff_rv['end'] < tss) & (gff_rv['end'] + 300 >= tss)]
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

    return [(tss, classification, confidence, gene_name, distance) for classification, gene_name in
            zip(possible_class, gene_names)]


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
    tss_classified = []

    gff_fw, gff_rv = prepare_gff(gff_df)

    distances = calculate_distances_to_next_gene(gff_df, tss_list, strand)

    for tss, confidence, distance in zip(tss_list, confidence_list, distances):
        tss_classified.extend(assign_tss_class(tss, confidence, distance, gff_fw, gff_rv, strand))

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
    :return: common_tss_df: data frame that contains the position, classified type, confidence value,
    and corresponding gene name of the TSSs that were found by both TSS predator and our prediction
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
