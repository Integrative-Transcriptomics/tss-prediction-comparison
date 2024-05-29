import wiggelen as wig
import pandas as pd
import os
import operator


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


def __apply_operation(operation, data_frame, x, start, stop):
    """
    applys a given value x with a given arithmetic operation to interval of values of given wiggle
    :param operation: math operation from operator Module
    :param data_frame: DataFrame; col1 -> region, col2 -> position, col3 -> value
    :param x
    :param start: first value of data_frame which operation will be applied on
    :param stop: last value of data_frame which operation will be applied on
    :return data_frame
    """
    for i in range(start-1, stop):
        data_frame.at[i, 'value'] = operation(data_frame.at[i, 'value'], x)
    return data_frame


def add_x(data_frame, x, start, stop):
    """
    adds x to each value of given interval in 'value column' of data_frame
    :param data_frame: DataFrame; col1 -> region, col2 -> position, col3 -> value
    :param x
    :param start: first value of data_frame which x will be added to
    :param stop: last value of data_frame which x will be added to
    :return: data_frame
    """
    return __apply_operation(operator.add, data_frame, x, start, stop)


def sub_x(data_frame, x, start, stop):
    """
    subtracts x from each value of given interval in 'value column' of data_frame
    :param data_frame: Data_frame; col1 -> region, col2 -> position, col3 -> value
    :param x
    :param start: first value of data_frame which x will be subtracted from
    :param stop: last value of data_frame which x will be subtracted from
    :return: data_frame
    """
    return __apply_operation(operator.sub, data_frame, x, start, stop)


def mult_x(data_frame, x, start, stop):
    """
    multiplies each value of given interval in 'value column' of data_frame with x
    :param data_frame: Data_frame; col1 -> region, col2 -> position, col3 -> value
    :param x
    :param start: first value of data_frame which will be multiplied with x
    :param stop: last value of data_frame which x will be multiplied with x
    :return: data_frame
    """
    return __apply_operation(operator.mul, data_frame, x, start, stop)


def div_x(data_frame, x, start, stop):
    """
    divides each value of given interval in 'value column' of data_frame with x
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


def median(data_frame, start=0, stop=None):
    """
    calculates the median of the values of the given interval, None values are ignored
    :param data_frame: Data_frame; col1 -> region, col2 -> position, col3 -> value
    :param start: start of interval
    :param stop: end of interval(included)
    :return: median
    """
    data_frame = filter_df(data_frame, start, stop)

    return data_frame["value"].median()


def quantil(data_frame, q, start=0, stop=None):
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


def mean(data_frame, start=0, stop=None):
    """
    calculates mean of the values of the given interval, None values are ignored
    :param data_frame: Data_frame; col1 -> region, col2 -> position, col3 -> value
    :param start: start of interval
    :param stop: end of interval(included)
    :return: mean
    """

    data_frame = filter_df(data_frame, start, stop)

    return data_frame["value"].mean()


def std(data_frame, start=0, stop=None):
    """
    calculates the standard deviation of the values of the given interval, None values are ignored
    :param data_frame: Data_frame; col1 -> region, col2 -> position, col3 -> value
    :param start: start of interval
    :param stop: end of interval(included)
    :return: std
    """
    data_frame = filter_df(data_frame, start, stop)
    return data_frame["value"].std(ddof=0)