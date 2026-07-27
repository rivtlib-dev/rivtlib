"""
This file contains functions for calculating properties of rectangular
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


def midspan_delta(ln, w, e, i):
    """mid-span deflection of simply supported beam with UDL

    Args:
        l (float): span
        w (float): uniform load
        e (float): modulus of elasticity
        i (float): moment of inertia

    Returns:
        float: mid-span deflection
    """
    return 5 * w * ln**4 / (384 * e * i)
