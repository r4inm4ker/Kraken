"""Kraken - maths.mathUtils module.

Utility functions for math operations.
"""

import math

def checkDivisor(value):
    """Checks if value is valid for division

    Return:
    True if is bad divisor.

    """

    if value == None or value == 0.0:
        return True

    return False


def radToDeg(value):
    """Convert value to degrees."""

    return value * (180.0 / math.pi)


def degToRad(value):
    """Convert value to radians."""

    return value * (math.pi / 180.0)