import wiggelen as wig
import pandas as pd
import os
import operator


# this file contains useful mathematical methods for the work with wiggle files


# parsing wiggle file to pandas DataFrame for further processing:

wiggle = os.path.relpath('..\\..\\tests\\test_files\\test.wig')
def parse_wiggle_to_DataFrame(wiggle):
    """
    parses a wiggle file to a pandas DataFrame
    :param wiggle: path to a wiggle file
    :return: pandas DataFrame
    """
    lst_of_triple = []

    for region, position, value in wig.fill(wig.walk(open(wiggle))):
        lst_of_triple.append((region, position, value))
    return pd.DataFrame(lst_of_triple)


# Aron
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
    for i in range(start, stop):
        data_frame.at[i, 'value'] = operation(data_frame.at[i, 'value'], x)
    return data_frame

# Addition
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


# Subtraktion
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


# Multiplikation
def mult_x(data_frame, x, start, stop):
    """
    multiplies each value of given interval in 'value column' of data_frame with x
    :param data_frame: Data_frame; col1 -> region, col2 -> position, col3 -> value
    :param x
    :param start: first value of data_frame which will be multiplied with x
    :param stop: last value of data_frame which x will be multiplied with x
    :return: data_frame
    """
    return __apply_operation(operator.mul(), data_frame, x, start, stop)


# Division
def div_x(data_frame, x, start, stop):
    """
    divides each value of given interval in 'value column' of data_frame with x
    :param data_frame: Data_frame; col1 -> region, col2 -> position, col3 -> value
    :param x
    :param start: first value of data_frame which will be divided by x
    :param stop: last value of data_frame which x will be divided by x
    :return: data_frame
    """
    return __apply_operation(operator.truediv(), data_frame, x, start, stop)


# Amelie
# Median
# Quantil
# Mean
# Standartabweichung


