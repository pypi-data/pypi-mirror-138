from ..pylena_cxx import morpho as cxx
from ..pylena_cxx.morpho import structuring_element_2d
from ..utils import check_numpy_dtype, check_type

import numpy as np

@check_numpy_dtype(ind=0, dtypes=[np.uint8])
@check_type(ind=1, wanted_types=[structuring_element_2d, np.ndarray])
def erosion(img, se):
    """
    Performs an erosion by a structuring element.

    Given a structuring element :math:`B`, the erosion :math:`\\varepsilon(f)` of the input image
    :math:`f` is defined as

    .. math::

        \\varepsilon(f)(x) = \\bigwedge \{f(y), y \in B_x\}

    Args
    ----
    img: 2-D array (dtype=uint8)
        The image to be processed
    se: structuring_element_2d or 2-D array
        The structuring element

    Return
    ------
    2-D array
        The resulting image

    Example
    -------

    >>> img = ... # Get an image
    >>> from pylena.morpho import make_structuring_element_2d, erosion
    >>> se = make_structring_element_2d("rect", 10, 10)
    >>> out = erosion(img, se)
    """
    if issubclass(type(se), np.ndarray):
        if se.ndim != 2:
            raise ValueError("Structuring element should be a 2D array")
        se = se.astype(bool)
        return cxx.erosion(img, structuring_element_2d(se))
    return cxx.erosion(img, se)

@check_numpy_dtype(ind=0, dtypes=[np.uint8])
@check_type(ind=1, wanted_types=[structuring_element_2d, np.ndarray])
def dilation(img, se):
    """
    Performs an dilation by a structuring element.

    Given a structuring element :math:`B`, the dilation :math:`\delta(f)` of the input image
    :math:`f` is defined as

    .. math::

        \delta(f)(x) = \\bigvee \{f(y), y \in B_x\}

    Args
    ----
    img: 2-D array (dtype=uint8)
        The image to be processed
    se: structuring_element_2d or 2-D array
        The structuring element

    Return
    ------
    2-D array
        The resulting image

    Example
    -------

    >>> img = ... # Get an image
    >>> from pylena.morpho import make_structuring_element_2d, dilation
    >>> se = make_structring_element_2d("rect", 10, 10)
    >>> out = dilation(img, se)
    """
    if issubclass(type(se), np.ndarray):
        if se.ndim != 2:
            raise ValueError("Structuring element should be a 2D array")
        se = se.astype(bool)
        return cxx.dilation(img, structuring_element_2d(se))
    return cxx.dilation(img, se)

@check_numpy_dtype(ind=0, dtypes=[np.uint8])
@check_type(ind=1, wanted_types=[structuring_element_2d, np.ndarray])
def opening(img, se):
    """
    Performs an opening by a structuring element.

    Given a structuring element :math:`B`, the dilation :math:`\gamma(f)` of the input image
    :math:`f` is defined as

    .. math::

        \gamma(f) = \delta_{B}(\\varepsilon_{B}(f))

    Args
    ----
    img: 2-D array (dtype=uint8)
        The image to be processed
    se: structuring_element_2d or 2-D array
        The structuring element

    Return
    ------
    2-D array
        The resulting image

    Example
    -------

    >>> img = ... # Get an image
    >>> from pylena.morpho import make_structuring_element_2d, opening
    >>> se = make_structring_element_2d("rect", 10, 10)
    >>> out = opening(img, se)
    """
    if issubclass(type(se), np.ndarray):
        if se.ndim != 2:
            raise ValueError("Structuring element should be a 2D array")
        se = se.astype(bool)
        return cxx.opening(img, structuring_element_2d(se))
    return cxx.opening(img, se)

@check_numpy_dtype(ind=0, dtypes=[np.uint8])
@check_type(ind=1, wanted_types=[structuring_element_2d, np.ndarray])
def closing(img, se):
    """
    Performs an closing by a structuring element.

    Given a structuring element :math:`B`, the dilation :math:`\gamma(f)` of the input image
    :math:`f` is defined as

    .. math::

        \gamma(f) = \\varepsilon_{B}(\delta_{B}(f))

    Args
    ----
    img: 2-D array (dtype=uint8)
        The image to be processed
    se: structuring_element_2d or 2-D array
        The structuring element

    Return
    ------
    2-D array
        The resulting image

    Example
    -------

    >>> img = ... # Get an image
    >>> from pylena.morpho import make_structuring_element_2d, closing
    >>> se = make_structring_element_2d("rect", 10, 10)
    >>> out = closing(img, se)
    """
    if issubclass(type(se), np.ndarray):
        if se.ndim != 2:
            raise ValueError("Structuring element should be a 2D array")
        se = se.astype(bool)
        return cxx.closing(img, structuring_element_2d(se))
    return cxx.closing(img, se)

@check_numpy_dtype(ind=0, dtypes=[np.uint8])
@check_type(ind=1, wanted_types=[structuring_element_2d, np.ndarray])
def gradient(img, se):
    """
    Performs a morphological gradient, also called **Beucher** gradient.

    Given a structuring element :math:`B` and an image :math:`f`, the morphological gradient is defined as

    .. math::

        \\rho_B = \delta_B - \\varepsilon_B

    Args
    ----
    img: 2-D array (dtype=uint8)
        The image to be processed
    se: structuring_element_2d or 2-D array
        The structuring element

    Return
    ------
    2-D array
        The resulting image

    Example
    -------

    >>> img = ... # Get an image
    >>> from pylena.morpho import make_structuring_element_2d, gradient
    >>> se = make_structring_element_2d("rect", 10, 10)
    >>> out = gradient(img, se)
    """
    if issubclass(type(se), np.ndarray):
        if se.ndim != 2:
            raise ValueError("Structuring element should be a 2D array")
        se = se.astype(bool)
        return cxx.gradient(img, structuring_element_2d(se))
    return cxx.gradient(img, se)