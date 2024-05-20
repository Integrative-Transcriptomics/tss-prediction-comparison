import numpy as np
import wiggelen as wig
import pandas as pd
import os


# this file contains useful mathematical methods for the work with wiggle files


# example; parsing wiggle file:

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

    print(lst_of_triple)
    return pd.DataFrame(lst_of_triple)

# print(parse_wiggle_to_DataFrame(wiggle))


# Aron
# Addition
# Subtraktion
# Multiplikation
# Division


# Amelie
# Median
# Quantil
# Mean
# Standartabweichung


