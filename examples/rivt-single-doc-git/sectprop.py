"""
This script contains functions for calculating properties of rectangular
sections.

    - section(b,d) : section modulus
    - inertia(b,d) : moment of interia

"""


def rectsect(b, d):
    """section modulus of rectangle

    Args:
        b (float): width
        d (float): depth

    Returns:
        float: section modulus
    """
    return b * d**2 / 6.0


def rectinertia(b, d):
    """moment of inertia of rectangle

    Args:
        b (float): width
        d (float): depth

    Returns:
        float: inertia
    """
    return b * d**3 / 12.0
