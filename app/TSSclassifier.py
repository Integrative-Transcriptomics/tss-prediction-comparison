import pandas as pd
import GFFParser as ps
from enum import Enum


class TSSType(Enum):
    PRIMARY = "pTSS/sTSS"
    INTERNAL = "iTSS"
    ANTISENSE = "asTSS"
    OTHER = "other"


def classify(filepath, TSS_dict, strand):
    gff_df = ps.parse_gff_to_df(filepath)
    tss_classified = {}

    gff_fw = gff_df[(gff_df['strand'] == "+")]
    gff_rv = gff_df[(gff_df['strand'] == "-")]

    for tss in TSS_dict["TSS Sites"]:

        if strand == "+":
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
            possible_class = [TSSType.OTHER.value]

        tss_classified[tss] = possible_class

    data_tuples = [(k, tss_type) for k, v in tss_classified.items() for tss_type in v]

    tss_classified = pd.DataFrame(data_tuples, columns=['TSS site', 'TSS type'])

    return tss_classified


def find_common_tss(prediction, master_table, strand):

    if (strand == "+"):
        mt_relevant_columns = master_table[master_table['strand'] == '+']

    else:
        mt_relevant_columns = master_table[master_table['strand'] == '-']

    mt_relevant_columns = mt_relevant_columns[['TSS site', 'TSS type']].reset_index(drop=True)

   # print (mt_relevant_columns)

    #common_tss_df = pd.merge(prediction, mt_relevant_columns, on=['TSS site', 'TSS type'], how='inner')

    expanded_prediction = pd.concat([
        prediction.assign(**{'TSS site': prediction['TSS site'] + offset})
        for offset in range(-5, 6)
    ])

    common_tss_df = pd.merge(expanded_prediction, mt_relevant_columns, on=['TSS site', 'TSS type'],
                             how='inner').drop_duplicates()

    return common_tss_df


def to_csv(df1, df2, master_table):
    mt_relevant_columns = master_table[['TSS site', 'TSS type']]
    dfs = [(df1, 'prediction'), (df2, 'shared tss'), (mt_relevant_columns, 'master Table')]

    csv_file = 'comparison.csv'
    with open(csv_file, 'w', newline='') as f:
        for df, name in dfs:
            freq = calculate_frequency_of_tss_classes(df)

            f.write(f"{name}\n")
            f.write(f"freq: primary/secondary:{freq['pTSS/sTSS']}, internal:{freq['iTSS']}, antisense: {freq['asTSS']}, other: {freq['other']}\n")
            df.to_csv(f, index=False)


def to_excel(our_prediction, df2, master_table):
    mt_relevant_columns = master_table[['TSS site', 'TSS type']]
    dfs = [(our_prediction, 'prediction'), (df2, 'shared tss'), (mt_relevant_columns, 'master table')]

    excel_file = 'comparison.xlsx'
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        for df, name in dfs:
            freq = calculate_frequency_of_tss_classes(df)
            df.to_excel(writer, sheet_name=name, index=False)
            worksheet = writer.sheets[name]

            start_col = df.shape[1] + 1
            worksheet.write(0, start_col, 'Frequency Data')

            row = 1
            for label, value in freq.items():
                worksheet.write(row, start_col, label)
                worksheet.write(row, start_col + 1, value)
                row += 1

        worksheet = writer.sheets["shared tss"]

        metrics = [
            ("recall", len(df2.index) / len(master_table.index)),
            ("precision", len(df2.index) / len(our_prediction.index))
        ]
        for i, (label, value) in enumerate(metrics):
            worksheet.write(i, df2.shape[1] + 4, label)
            worksheet.write(i, df2.shape[1] + 5, value)


def calculate_frequency_of_tss_classes(common_tss_df):
    type_counts = common_tss_df['TSS type'].value_counts()
    all_types = [e.value for e in TSSType]
    type_counts = type_counts.reindex(all_types, fill_value=0)
    total_count = type_counts.sum()
    relative_frequencies = type_counts / total_count

    return relative_frequencies


mt = {
    'TSS site': [25675, 31366, 31650, 32000],
    'TSS type': ["iTSS", "asTSS", "pTSS/sTSS", "asTSS"],
    'detected': ['1', '1', '1', '0'],
    'Locus_tag': ['esdnc', 'aada', 'Wqwq', 'wwisd'],
    'strand': ["+", "-", "+", "+"]
}

df = pd.DataFrame(mt)

cl = classify("../tests/test_files/NC_004703.gff", {"TSS Sites": [400, 25675, 31362, 31650]}, "+")
print(cl)
co = find_common_tss(cl, df, "+")
print(co)
#print(calculate_frequency_of_tss_classes(cl)["iTSS"])
#to_csv(cl, co, df)
to_excel(cl, co, df)

