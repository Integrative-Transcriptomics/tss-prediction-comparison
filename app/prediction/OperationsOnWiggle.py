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

    for region, position, value in wig.fill(wig.walk(open(wiggle, "r"))):
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

    for i in range(start - 1, stop):
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


def fill_dataframe(df, full_positions):
    """
    fills up all the positions of the df that are included in full_positions and dont already hold a value
    with 0
    :param df: DataFrames
    :param full_positions: range object that contains all the positions for which the df should have values
    :return: df_full
    """
    region = df['region'].iloc[0]
    df_full = pd.DataFrame({'position': full_positions})
    df_full = df_full.merge(df, on='position', how='left').fillna(0)
    df_full['region'] = region
    df_full = df_full[['region', 'position', 'value']]
    return df_full


def __apply_operation_to_multiple_df(lst_of_df, operation):
    """
    Computes DataFrame which holds a value x at position i in column "value".
    x is calculated with 'operation' and the values at position i of column "value" of all DataFrames in lst_of_df
    :param lst_of_df: holds DataFrames
    :param operation: operation which will be applied
    :return: new_df
    """
    max_length = max(len(df) for df in lst_of_df)
    full_positions = range(1, max_length + 1)

    for i in range(len(lst_of_df)):
        lst_of_df[i] = fill_dataframe(lst_of_df[i], full_positions)

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
    :param lst_of_df: holds DataFrames
    :return: new_df with median as values
    """
    return __apply_operation_to_multiple_df(lst_of_df, np.median)


def add_values_of_multiple_df(lst_of_df):
    """
    Computes DataFrame which holds a sum at position x.
    The sum is calculated from the values at position x of column "value" of all DataFrames in lst_of_df
    :param lst_of_df: holds DataFrames
    :return: new_df with sum as values
    """
    return __apply_operation_to_multiple_df(lst_of_df, sum)


def get_max_values_of_multiple_df(lst_of_df):
    """
    Computes DataFrame which holds a max at position x.
    The max is calculated from the values at position x of column "value" of all DataFrames in lst_of_df
    :param lst_of_df: holds DataFrames
    :return: new_df with max as values
    """
    return __apply_operation_to_multiple_df(lst_of_df, max)


def get_min_values_of_multiple_df(lst_of_df):
    """
    Computes DataFrame which holds a min at position x.
    The sum is calculated from the values at position x of column "value" of all DataFrames in lst_of_df
    :param lst_of_df: holds DataFrames
    :return: new_df with min as values
    """
    return __apply_operation_to_multiple_df(lst_of_df, min)

def mean_absolute_deviation(data_frame):
    """
    calculates the mean absolute deviation of the values, None values are ignored
    :param data_frame: Data_frame; col1 -> region, col2 -> position, col3 -> value
    :return: MAD
    """

    median = median_of_values(data_frame)

    return np.median(np.abs(data_frame["value"] - median))


#TODO: Implement a function that provides the input for the prediction of TSSs and accounts for possible multiple conditions.

def z_score(data_frame):
    """
       Computes a modified z score using the median and MAD.
       :param data_frame: Data_frame; col1 -> region, col2 -> position, col3 -> value
       :return: pandas DataFrame
       """

    median = median_of_values(data_frame)
    mad = mean_absolute_deviation(data_frame)
    modified_z_scores = 0.6745 * (data_frame["value"] - median) / mad
    modified_z_scores.name = "zscore"
    return modified_z_scores

def gradients(data_frame):
    """
           Computes the first and second gradient (approximation of derivative) for a given DataFrame.
           :param data_frame: Data_frame; col1 -> region, col2 -> position, col3 -> value
           :return: pandas DataFrame 1st, 2nd gradient
    """

    first_gradient = np.gradient(data_frame["value"])

    second_gradient = np.gradient(first_gradient)

    gradient_data_frame = pd.DataFrame({"first gradient": first_gradient, "second gradient": second_gradient})

    gradient_data_frame.index = data_frame.index.values

    return gradient_data_frame


def previous(data_frame):
    """
    Computes the previous value for each value in the DataFrame.
    :param data_frame: Data_frame; col1 -> region, col2 -> position, col3 -> value
    :return: pandas DataFrame
    """
    previous = 0
    previous_values = []
    for value in data_frame["value"].values:
        previous_values += [previous]
        previous = value

    return pd.Series(previous_values, name="previous", index=data_frame.index.values)


def parse_for_prediction(wiggle_files):
    """
    Computes final pre prepared DataFrame for prediction.
    The sum is calculated from the values at position x of column "value" of all DataFrames in lst_of_df
    :param wiggle_files: list of paths to wiggle files
    :return: pandas DataFrame
    """

    parsed_dfs = [parse_wiggle_to_DataFrame(wiggle) for wiggle in wiggle_files]

    median_df = median_of_multiple_df(parsed_dfs)

    median_df = median_df.dropna()

    zscore = z_score(median_df)

    gradient_df = gradients(median_df)

    previous_df = previous(median_df)

    prediction_df = pd.concat([median_df["value"], zscore, gradient_df["first gradient"],
                               gradient_df["second gradient"], previous_df], axis=1)

    #filtering
    prediction_df = prediction_df[prediction_df["first gradient"] > 0]
    prediction_df = prediction_df[prediction_df["zscore"] > 0]

    return prediction_df
