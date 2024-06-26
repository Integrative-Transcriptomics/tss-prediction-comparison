import pandas as pd


WANTED_COLUMNS = ["detected", "Pos", "Strand", "Primary", "Secondary", "Internal", "Antisense"]
TSS_TYPES = ["Primary", "Secondary", "Internal", "Antisense"]


def parse_master_table_to_df(master_table):

    # parse tsv and take "Pos" column as index
    df = pd.read_csv(master_table, sep='\t', index_col="Pos")
    print(df)
    # delete all duplicate lines (oriented on "Pos" column)
    df = df[~df.index.duplicated(keep='first')]
    print(df)
    # add index column "Pos" as normal col to df
    df = df.reset_index()
    print(df)

    df = __delete_not_detected_positions(df)
    df = __delete_unwanted_columns(df, WANTED_COLUMNS)
    df = __summarize_TSS_TYPES(df)
    return df

def __delete_duplicates(data_frame):
    return None


def __delete_not_detected_positions(data_frame):
    positions = data_frame["Pos"]
    for pos in positions:
        if data_frame.at[pos, "detected"] == "0":
            data_frame.drop(data_frame.index[pos], inplace=True)
    return data_frame

def __summarize_TSS_TYPES(data_frame):
    summarized_type_column = []
    positions = data_frame["Pos"]
    for row_index in range(len(positions)):
        for type in TSS_TYPES:
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


file_path = "../tests/test_files/MasterTable_chrom.tsv"
df = parse_master_table_to_df(file_path)
print(df)
