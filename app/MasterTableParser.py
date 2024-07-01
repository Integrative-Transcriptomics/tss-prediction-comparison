import pandas as pd


WANTED_COLUMNS = ["Condition", "detected", "Pos", "Strand", "Primary", "Secondary", "Internal", "Antisense", "Locus_tag"]
TSS_TYPES = ["Primary", "Secondary", "Internal", "Antisense", "Orphan"]


def parse_master_table_to_df(master_table):
    df = pd.read_csv(master_table, sep="\t")
    df = __delete_unwanted_columns(df, WANTED_COLUMNS)
    df = __delete_not_detected_positions(df)
    conditions = __get_conditions_of_df(df)
    dfs_for_each_condition = {}
    for cond in conditions:
        df_copy = df.copy()
        df_for_cond = __create_df_for_condition(cond, df_copy)
        df_for_cond = df_for_cond.reset_index(drop=True)
        dfs_for_each_condition[cond] = df_for_cond
    return dfs_for_each_condition


def __create_df_for_condition(condition, data_frame):
    data_frame = __drop_rows_with_unwanted_conditions(condition, data_frame)
    data_frame = __summarize_TSS_TYPES(data_frame)
    data_frame = data_frame.drop_duplicates()
    return data_frame


def __drop_rows_with_unwanted_conditions(condition, data_frame):
    for ind in data_frame.index:
        if data_frame.at[ind, "Condition"] != condition:
            data_frame = data_frame.drop([ind])
    return data_frame


def __get_conditions_of_df(data_frame):
    conditions = []
    column_of_conditions = data_frame["Condition"].tolist()
    for con in column_of_conditions:
        if con not in conditions:
            conditions.append(con)
    return conditions


def __delete_not_detected_positions(data_frame):
    for ind in data_frame.index:
        if data_frame.at[ind, "detected"] == 0:
            data_frame = data_frame.drop([ind])
    return data_frame


def __summarize_TSS_TYPES(data_frame):
    tss_type_of_positions = []
    for ind in data_frame.index:
        for type in TSS_TYPES:
            if data_frame.at[ind, "Locus_tag"] == type.lower():
                tss_type_of_positions.append(type)
                break
            elif data_frame.at[ind, type] == 1:
                tss_type_of_positions.append(type)
                break
    data_frame["TSS type"] = tss_type_of_positions
    return __delete_unwanted_columns(data_frame, ["Pos", "Strand", "TSS type"])


def __delete_unwanted_columns(data_frame, wanted_columns):
    columns = data_frame.columns.tolist()
    for col in columns:
        if col in wanted_columns:
            continue
        else:
            data_frame = data_frame.drop(columns=[col])
    return data_frame


file_path = "../tests/test_files/SmallMasterTable.tsv"
dfs = parse_master_table_to_df(file_path)
for condition in dfs.keys():
    print("condition: " + condition + "\n")
    print(dfs.get(condition))
    print("\n")
