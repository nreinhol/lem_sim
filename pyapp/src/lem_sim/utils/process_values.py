import numpy as np


def truncate_values_of_array(array):
    Ndecimals = 2
    decade = 10**Ndecimals
    return np.trunc(array * decade) / decade
