import pandas as pd


wanted_columns = ["detected", "Pos", "Strand", "Primary", "Secondary", "Internal", "Antisense"]
TSS_types = ["Primary", "Secondary", "Internal", "Antisense"]


def parse_master_table_to_df(master_table):
    df = pd.read_csv(master_table)
    print(df)
    df = __delete_unwanted_columns(df, wanted_columns)
    df = __sumarize_TSS_types(df)
    positions = df["Pos"]
    for row_index in range(len(positions)):
        if df.at[row_index, "detected"] == 0:
            df.drop(df.index[row_index], inplace=True)
    return df


def __sumarize_TSS_types(data_frame):
    data_frame["TSS type"] = []
    positions = data_frame["Pos"]
    for row_index in range(len(positions)):
        for type in TSS_types:
            if data_frame.at[row_index, type] == 1:
                data_frame.at[row_index, "TSS_type"] = type
    return __delete_unwanted_columns(data_frame, ["detected", "Pos", "Strand", "TSS type"])


def __delete_unwanted_columns(data_frame, wanted_columns):
    columns = data_frame.columns[0].split("\t")
    for col in columns:
        for wanted_col in wanted_columns:
            if col == wanted_col:
                continue
            else:
                data_frame = data_frame.drop(columns=[col])
    return data_frame


#file = file_path = 'tests/test_files/MasterTable_Example.xlsx'
#df = parse_master_table_to_df(file)
#print(df)
