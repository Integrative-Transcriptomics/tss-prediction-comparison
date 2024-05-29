import wiggelen as wig
import pandas as pd
import operator
import numpy as np


# this file contains a wiggle parser and useful mathematical methods for the work with wiggle files
# we will parse the wiggle files to pandas DataFrames since working with these is a lot easier


def parse_wiggle_to_DataFrame(wiggle):
    """
    parses a wiggle file to a pandas DataFrame
    :param wiggle: path to a wiggle file
    :return: pandas DataFrame
    """
    lst_of_triple = []

    for region, position, value in wig.fill(wig.walk(open(wiggle))):
        lst_of_triple.append((region, position, value))
    return pd.DataFrame(lst_of_triple, columns=["region", "position", "value"])


# the following methods expect the input DataFrame to be of form: col1 -> region, col2 -> position, col3 -> value
# methods for operations on single DataFrames:

def __apply_operation(operation, data_frame, x, start, stop):
    """
    applys a given value x with a given arithmetic operation to interval of values in column "value" of given DataFrame
    :param operation: math operation from operator Module
    :param data_frame: Data_frame; col1 -> region, col2 -> position, col3 -> value
    :param x
    :param start: first value of data_frame which operation will be applied on
    :param stop: last value of data_frame which operation will be applied on
    :return data_frame
    """

    for i in range(start-1, stop):
        data_frame.at[i, 'value'] = operation(data_frame.at[i, 'value'], x)
    return data_frame


def add_x_to_values(data_frame, x, start, stop):
    """
    adds x to each value of given interval in "value" of data_frame
    :param data_frame: DataFrame; col1 -> region, col2 -> position, col3 -> value
    :param x
    :param start: first value of data_frame which x will be added to
    :param stop: last value of data_frame which x will be added to
    :return: data_frame
    """
    return __apply_operation(operator.add, data_frame, x, start, stop)


def sub_x_to_values(data_frame, x, start, stop):
    """
    subtracts x from each value of given interval in "value" column of data_frame
    :param data_frame: Data_frame; col1 -> region, col2 -> position, col3 -> value
    :param x
    :param start: first value of data_frame which x will be subtracted from
    :param stop: last value of data_frame which x will be subtracted from
    :return: data_frame
    """
    return __apply_operation(operator.sub, data_frame, x, start, stop)


def mult_x_to_values(data_frame, x, start, stop):
    """
    multiplies each value of given interval in "value" column of data_frame with x
    :param data_frame: Data_frame; col1 -> region, col2 -> position, col3 -> value
    :param x
    :param start: first value of data_frame which will be multiplied with x
    :param stop: last value of data_frame which x will be multiplied with x
    :return: data_frame
    """
    return __apply_operation(operator.mul, data_frame, x, start, stop)


def div_x_to_values(data_frame, x, start, stop):
    """
    divides each value of given interval in "value" column of data_frame with x
    :param data_frame: Data_frame; col1 -> region, col2 -> position, col3 -> value
    :param x
    :param start: first value of data_frame which will be divided by x
    :param stop: last value of data_frame which x will be divided by x
    :return: data_frame
    """
    return __apply_operation(operator.truediv, data_frame, x, start, stop)


def filter_df(data_frame, start, stop):
    """
    extracts the interval between the given positions from a data frame as a new data frame
    :param data_frame: Data_frame; col1 -> region, col2 -> position, col3 -> value
    :param start: start of interval
    :param stop: end of interval
    :return: data frame
    """
    if stop is None:
        stop = data_frame.iloc[-1]["position"]

    if start != 0:
        start -= 1

    data_frame = data_frame[start:stop]

    return data_frame


def median_of_values(data_frame, start=0, stop=None):
    """
    calculates the median of the values of the given interval, None values are ignored
    :param data_frame: Data_frame; col1 -> region, col2 -> position, col3 -> value
    :param start: start of interval
    :param stop: end of interval(included)
    :return: median
    """
    data_frame = filter_df(data_frame, start, stop)

    return data_frame["value"].median()


def quantil_of_values(data_frame, q, start=0, stop=None):
    """
    calculates the q-quantile of the values in the specified interval
    :param data_frame: Data_frame; col1 -> region, col2 -> position, col3 -> value
    :param q: quantile
    :param start: start of interval
    :param stop: end of interval(included)
    :return: quantile
    """
    data_frame = filter_df(data_frame, start, stop)

    return data_frame["value"].quantile(q)


def mean_of_values(data_frame, start=0, stop=None):
    """
    calculates mean of the values of the given interval, None values are ignored
    :param data_frame: Data_frame; col1 -> region, col2 -> position, col3 -> value
    :param start: start of interval
    :param stop: end of interval(included)
    :return: mean
    """

    data_frame = filter_df(data_frame, start, stop)

    return data_frame["value"].mean()


def std_of_values(data_frame, start=0, stop=None):
    """
    calculates the standard deviation of the values of the given interval, None values are ignored
    :param data_frame: Data_frame; col1 -> region, col2 -> position, col3 -> value
    :param start: start of interval
    :param stop: end of interval(included)
    :return: std
    """
    data_frame = filter_df(data_frame, start, stop)
    return data_frame["value"].std(ddof=0)


# methods for operations on multiple DataFrames:

def __apply_operation_to_multiple_df(lst_of_df, operation):
    """
    Computes DataFrame which holds a value x at position i in column "value".
    x is calculated with 'operation' and the values at position i of column "value" of all DataFrames in lst_of_df
    The "value" columns of the DataFrames in lst_of_df are expected to be of same length.
    :param lst_of_df: holds DataFrames
    :param operation: operation which will be applied
    :return: new_df
    """
    new_df = lst_of_df[0]
    for row in range(len(new_df["value"])):
        values_of_dfs = []
        for df in lst_of_df:
            values_of_dfs.append(df.at[row, "value"])
        new_df.at[row, "value"] = operation(values_of_dfs)
    return new_df


def median_of_multiple_df(lst_of_df):
    """
    Computes DataFrame which holds a median at position x.
    The median is calculated from the values at position x of column "value" of all DataFrames in lst_of_df
    The "value" columns of the DataFrames in lst_of_df are expected to be of same length.
    :param lst_of_df: holds DataFrames
    :return: new_df with median as values
    """
    return __apply_operation_to_multiple_df(lst_of_df, np.median)


def add_values_of_multiple_df(lst_of_df):
    """
    Computes DataFrame which holds a sum at position x.
    The sum is calculated from the values at position x of column "value" of all DataFrames in lst_of_df
    The "value" columns of the DataFrames in lst_of_df are expected to be of same length.
    :param lst_of_df: holds DataFrames
    :return: new_df with sum as values
    """
    return __apply_operation_to_multiple_df(lst_of_df, sum)


def get_max_values_of_multiple_df(lst_of_df):
    """
    Computes DataFrame which holds a max at position x.
    The max is calculated from the values at position x of column "value" of all DataFrames in lst_of_df
    The "value" columns of the DataFrames in lst_of_df are expected to be of same length.
    :param lst_of_df: holds DataFrames
    :return: new_df with max as values
    """
    return __apply_operation_to_multiple_df(lst_of_df, max)


def get_min_values_of_multiple_df(lst_of_df):
    """
    Computes DataFrame which holds a min at position x.
    The sum is calculated from the values at position x of column "value" of all DataFrames in lst_of_df
    The "value" columns of the DataFrames in lst_of_df are expected to be of same length.
    :param lst_of_df: holds DataFrames
    :return: new_df with min as values
    """
    return __apply_operation_to_multiple_df(lst_of_df, min)


#TODO: Implement a function that provides the input for the prediction of TSSs and accounts for possible multiple conditions.

