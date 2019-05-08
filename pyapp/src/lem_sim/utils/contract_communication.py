import numpy as np

DECIMAL_PLACES = 2
MULTIPLIER = 10**DECIMAL_PLACES


def prepare_for_sending(value):
    if type(value) is np.ndarray:
        value = value.tolist()
        return shift_decimal_right(value)
    else:
        return shift_decimal_right(value)


def prepare_for_storing(value):
    if type(value) is list:
        value = shift_decimal_left(value)
        return np.array(value)
    else:
        return shift_decimal_left(value)


def shift_decimal_right(value):
    if type(value) is list:
        return [int(i * MULTIPLIER) for i in value]
    if type(value) is int or float:
        return int(value * MULTIPLIER)


def shift_decimal_left(value):
    if type(value) is list:
        return [float(i / MULTIPLIER) for i in value]
    if type(value) is int or float:
        return float(value / MULTIPLIER)
