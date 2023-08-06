"""
Base
"""

__all__ = ['check_type', 'check_numpy_dtype', 'morpho']

from . import morpho as morpho
from .utils import *

__version__ = "dev"
try:
    from .version import version
    __version__ = version
except ImportError:
    pass
