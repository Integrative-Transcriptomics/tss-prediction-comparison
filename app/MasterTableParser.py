import pandas as pd
from enum import Enum


class TSS_TYPES(Enum):
    """
    Enum class representing TSS_Types.
    """
    Primary = 1
    Secondary = 2
    Internal = 3
    Antisense = 4
    Orphan = 5


WANTED_COLUMNS = ["Condition", "detected", "Pos", "Strand", "Primary", "Secondary", "Internal", "Antisense", "Locus_tag"]


def parse_master_table_to_df(master_table):
    """
    Parses a MasterTable in TSV format and returns a dictionary,
    which holds parsed data for each condition of MasterTable data.
    The created DataFrames hold only detected Positions and the columns: "Pos", "Strand", "TSS-type".
    :param master_table:
    :return: dictionary with condition as key and data_frame with parsed data as value
    """
    df = pd.read_csv(master_table, sep="\t")
    df = __delete_unwanted_columns(df, WANTED_COLUMNS)
    df = __delete_not_detected_positions(df)
    conditions = __get_conditions_of_df(df)
    dfs_for_each_condition = {}
    for cond in conditions:
        df_copy = df.copy()
        df_for_cond = __create_df_for_condition(cond, df_copy)
        dfs_for_each_condition[cond] = df_for_cond
    return dfs_for_each_condition


def __create_df_for_condition(condition, data_frame):
    """
    Creates a DataFrame for a condition from a given MasterTable.
    :param condition: represents a condition which is included in MasterTable
    :param data_frame: represents the MasterTable
    :return: DataFrame holding relevant data for given condition in columns: "Pos", "Strand" and "TSS type"
    """
    data_frame = __drop_rows_with_unwanted_conditions(condition, data_frame)
    data_frame = __summarize_TSS_TYPES(data_frame)
    data_frame = data_frame.drop_duplicates()
    data_frame = data_frame.reset_index(drop=True)
    return data_frame


def __drop_rows_with_unwanted_conditions(condition, data_frame):
    """
    Drops all rows of given DataFrame which do not have a given condition in "Condition" column.
    :param condition:
    :param data_frame:
    :return: DataFrame which holds only rows that represent the given condition
    """
    for ind in data_frame.index:
        if data_frame.at[ind, "Condition"] != condition:
            data_frame = data_frame.drop([ind])
    return data_frame


def __get_conditions_of_df(data_frame):
    """
    Iterates over the given DataFrame and returns a list of all Conditions which can be found in it.
    :param data_frame:
    :return: list of all Conditions
    """
    conditions = []
    column_of_conditions = data_frame["Condition"].tolist()
    for con in column_of_conditions:
        if con not in conditions:
            conditions.append(con)
    return conditions


def __delete_not_detected_positions(data_frame):
    """
    Iterates over the "Detected" column of given DataFrame and only keeps the positions which are detected.
    :param data_frame:
    :return:
    """
    for ind in data_frame.index:
        if data_frame.at[ind, "detected"] == 0:
            data_frame = data_frame.drop([ind])
    return data_frame


def __summarize_TSS_TYPES(data_frame):
    """
    Iterates over every row of given DataFrame
    and adds a TSS-label (derived from binary TSS-classification) to row "TSS type".
    The rows involved in the binary TSS-classification are dropped afterwards.
    :param data_frame:
    :return:
    """
    tss_type_of_positions = []
    for ind in data_frame.index:
        for type in TSS_TYPES:
            if data_frame.at[ind, "Locus_tag"] == type.name.lower():
                tss_type_of_positions.append(type.name)
                break
            elif data_frame.at[ind, type.name] == 1:
                tss_type_of_positions.append(type.name)
                break
    data_frame["TSS type"] = tss_type_of_positions
    return __delete_unwanted_columns(data_frame, ["Pos", "Strand", "TSS type"])


def __delete_unwanted_columns(data_frame, wanted_columns):
    """
    Gets a DataFrame and drops all columns which are not in wanted_columns.
    :param data_frame
    :param wanted_columns: Columns which should not be dropped
    :return: DataFrame only containing wanted_columns
    """
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
