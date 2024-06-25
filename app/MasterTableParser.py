import pandas as pd


wanted_columns = ["detected", "Pos", "Strand", "Primary", "Secondary", "Internal", "Antisense"]
TSS_types = ["Primary", "Secondary", "Internal", "Antisense"]


def parse_master_table_to_df(master_table):
    df = pd.read_csv(master_table, sep='\t', index_col="Pos")
    print(df)

    df = df[~df.index.duplicated(keep='first')]
    print(df)

    # delete not detected positions
    #positions = df["Pos"]
    #for row_index in range(len(positions)):
    #    if df.at[row_index, "detected"] == "0":
    #        df.drop(df.index[row_index], inplace=True)

    df = __delete_unwanted_columns(df, wanted_columns)
    df = __summarize_TSS_types(df)
    return df


def __summarize_TSS_types(data_frame):
    summarized_type_column = []
    positions = data_frame["Pos"]
    for row_index in range(len(positions)):
        for type in TSS_types:
            if data_frame.at[row_index, type] == 1:
                summarized_type_column.append(type)
                break

    # debug line
    print(len(summarized_type_column))

    data_frame["TSS type"] = summarized_type_column
    return __delete_unwanted_columns(data_frame, ["detected", "Pos", "Strand", "TSS type"])


def __delete_unwanted_columns(data_frame, wanted_columns):
    columns = data_frame.columns.tolist()
    for col in columns:
        if col in wanted_columns:
            continue
        else:
            data_frame = data_frame.drop(columns=[col])
    return data_frame


<<<<<<< HEAD
file_path = "../tests/test_files/MasterTable_chrom.tsv"
df = parse_master_table_to_df(file_path)
print(df)
=======
#file = file_path = 'tests/test_files/MasterTable_Example.xlsx'
#df = parse_master_table_to_df(file)
#print(df)
>>>>>>> c2d8026603299c002bf7902d017fdc10cbdb2a51
