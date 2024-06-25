import pandas as pd
from enum import Enum
from json import loads, dumps
import GFFParser as ps

class TSSType(Enum):
    PRIMARY = "pTSS/sTSS"
    INTERNAL = "iTSS"
    ANTISENSE = "asTSS"
    ORPHAN = "orphan"


def classify(gff_df, TSS_dict, strand):
    #gff_df = ps.parse_gff_to_df(gff_df)


    tss_classified = {}

    gff_fw = gff_df[(gff_df['strand'] == "+")]
    gff_rv = gff_df[(gff_df['strand'] == "-")]

    for tss in TSS_dict:

        if not strand:
            intern = gff_fw[(gff_fw['end'] >= tss) & (gff_fw['start'] <= tss)]
            prim = gff_fw[(gff_fw['start'] >= tss) & (gff_fw['start'] - 200 <= tss)]
            anti = gff_rv[(gff_rv['end'] + 100 >= tss) & (gff_rv['start'] - 100 <= tss)]

        else:
            intern = gff_rv[(gff_rv['end'] >= tss) & (gff_rv['start'] <= tss)]
            prim = gff_rv[(gff_rv['start'] >= tss) & (gff_rv['start'] - 200 <= tss)]
            anti = gff_fw[(gff_fw['end'] + 100 >= tss) & (gff_fw['start'] - 100 <= tss)]

        possible_class = []

        if not intern.empty:
            possible_class.append(TSSType.INTERNAL.value)

        if not prim.empty:
            possible_class.append(TSSType.PRIMARY.value)

        if not anti.empty:
            possible_class.append(TSSType.ANTISENSE.value)

        if len(possible_class) == 0:
            possible_class = [TSSType.ORPHAN.value]

        tss_classified[tss] = possible_class

    data_tuples = [(k, tss_type) for k, v in tss_classified.items() for tss_type in v]

    tss_classified = pd.DataFrame(data_tuples, columns=['pos', 'TSS type'])

    return tss_classified


def find_common_tss(prediction, master_table, strand):
    if not strand:
        mt_relevant_columns = master_table[master_table['strand'] == '+']

    else:
        mt_relevant_columns = master_table[master_table['strand'] == '-']

    mt_relevant_columns = mt_relevant_columns[['pos', 'TSS type']].reset_index(drop=True)

    #common_tss_df = pd.merge(prediction, mt_relevant_columns, on=['TSS site', 'TSS type'], how='inner')

    expanded_prediction = pd.concat([
        prediction.assign(**{'pos': prediction['pos'] + offset})
        for offset in range(-5, 6)
    ])

    common_tss_df = pd.merge(expanded_prediction, mt_relevant_columns, on=['pos', 'TSS type'],
                             how='inner').drop_duplicates()

    return common_tss_df


def to_csv(df1, df2, master_table):
    mt_relevant_columns = master_table[['pos', 'TSS type']]
    dfs = [(df1, 'prediction'), (df2, 'shared_TSS'), (mt_relevant_columns, 'TSS_predator')]

    for df, name in dfs:
        csv_file = f'{name}.csv'
        with open(csv_file, 'w', newline='') as f:
            df.to_csv(f, index=False)


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
    'pos': [25675, 31366, 31650, 32000, 405, 400],
    'TSS type': ["iTSS", "asTSS", "pTSS/sTSS", "asTSS", "iTSS", "pTSS/sTSS"],
    'detected': ['1', '1', '1', '0', '1', '1'],
    'Locus_tag': ['esdnc', 'aada', 'Wqwq', 'wwisd', 'wwisd', 'wwisd'],
    'strand': ["+", "-", "+", "+", "+", "+"]
}

df = pd.DataFrame(mt)

cl = classify("../tests/test_files/NC_004703.gff", [400, 25675, 31362, 31650], False)
print(cl)
co = find_common_tss(cl, df, False)
print(co)
to_csv(cl, co, df)

print(freq_return_obj(cl, co, df))
print(recall_and_precision_return_obj(co, cl, df))'''
