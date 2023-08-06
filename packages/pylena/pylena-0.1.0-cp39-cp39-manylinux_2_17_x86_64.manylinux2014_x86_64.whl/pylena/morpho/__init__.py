"""
Mathematical morphology
"""

from .se import make_structuring_element_2d
from .soperations import *

__all__ = [
    "make_structuring_element_2d",
    "erosion",
    "dilation",
    "opening",
    "closing",
    "gradient"
]