DECIMAL_PLACES = 10
MULTIPLIER = 10**DECIMAL_PLACES


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
