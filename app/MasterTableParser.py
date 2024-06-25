import pandas as pd


def parse_master_table_to_df(masterTable):
    df = pd.read_csv(masterTable)
    wanted_columns = ['detected', 'Pos', 'Strand', 'Locus_tag']
    __delete_unwanted_columns(wanted_columns, df)
    positions = df['Pos']
    for row_index in range(len(positions)):
        if df.at[row_index, 'detected'] == 0:
            df.drop(df.index[row_index], inplace=True)
    return df


def __delete_unwanted_columns(wanted_columns, df):
    for col in df.columns.tolist():
        for wanted_col in wanted_columns:
            if col == wanted_col:
                continue
            else: del df[col]


#file = file_path = 'tests/test_files/MasterTable_Example.xlsx'
#df = parse_master_table_to_df(file)
#print(df)