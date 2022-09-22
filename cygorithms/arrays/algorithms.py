from . import c_algorithms
from .arrays import OneDArray
from typing import (
    Callable,
    Optional,
    Dict,
    Any
)
from numbers import Integral


def _get_kwargs(
    comp: Optional[Callable[[Any, Any], bool]] = None,
    begin: Optional[int] = None,
    end: Optional[int] = None
) -> Dict:
    kwargs = {}
    if comp is not None:
        if not hasattr(comp, "__call__"):
            raise TypeError(
                "`comp` must be callable,"
                f" got `comp` of type {type(comp).__name__}"
            )
        kwargs["comp"] = comp
    if begin is not None:
        if not isinstance(begin, Integral):
            raise TypeError(
                "`begin` must be of integer type,"
                f" got `begin` of type {type(begin).__name__}"
            )
        kwargs["begin"] = begin
    if end is not None:
        if not isinstance(begin, Integral):
            raise TypeError(
                "`end` must be of integer type,"
                f" got `end` of type {type(begin).__name__}"
            )
        kwargs["end"] = end
    return kwargs


def selection_sort(
    array: OneDArray,
    *,
    comp: Optional[Callable[[Any, Any], bool]] = None,
    begin: Optional[int] = None,
    end: Optional[int] = None
) -> OneDArray:
    """
    Selection sort algorithm for array.

    Parameters
    ----------
    array : OneDArray instance
        array to sort
    comp : callable, optional
        comprasion function ``comp(u: Any, v: Any) -> bool``,
        by default ascending sort to be performed, such that
        ``comp = lambda u, v: u >= v``.
    begin : int, optional
        begin of interval to sort, by default ``begin = 0``
    end : int, optional
        end of interval to sort, by default ``end = 0``

    Returns
    -------
    array : OneDArray instance
        Array ``array`` sorted inplace in interval ``[begin, end)``
    """
    kwargs = _get_kwargs(comp, begin, end)

    c_algorithms.selection_sort(
        array.array,
        **kwargs
    )

    return array


def merge_sort(
    array: OneDArray,
    *,
    comp: Optional[Callable[[Any, Any], bool]] = None,
    begin: Optional[int] = None,
    end: Optional[int] = None
) -> OneDArray:
    """
    Merge sort algorithm for array.

    Parameters
    ----------
    array : OneDArray instance
        array to sort
    comp : callable, optional
        comprasion function ``comp(u: Any, v: Any) -> bool``,
        by default ascending sort to be performed, such that
        ``comp = lambda u, v: u >= v``.
    begin : int, optional
        begin of interval to sort, by default ``begin = 0``
    end : int, optional
        end of interval to sort, by default ``end = 0``

    Returns
    -------
    array : OneDArray instance
        Array ``array`` sorted inplace in interval ``[begin, end)``
    """
    kwargs = _get_kwargs(comp, begin, end)

    c_algorithms.merge_sort(
        array.array,
        **kwargs
    )

    return array


def quick_sort(
    array: OneDArray,
    *,
    comp: Optional[Callable[[Any, Any], bool]] = None,
    begin: Optional[int] = None,
    end: Optional[int] = None
) -> OneDArray:
    """
    Quick sort algorithm for array.

    Parameters
    ----------
    array : OneDArray instance
        array to sort
    comp : callable, optional
        comprasion function ``comp(u: Any, v: Any) -> bool``,
        by default ascending sort to be performed, such that
        ``comp = lambda u, v: u >= v``.
    begin : int, optional
        begin of interval to sort, by default ``begin = 0``
    end : int, optional
        end of interval to sort, by default ``end = 0``

    Returns
    -------
    array : OneDArray instance
        Array ``array`` sorted inplace in interval ``[begin, end)``
    """
    kwargs = _get_kwargs(comp, begin, end)

    c_algorithms.quick_sort(
        array.array,
        **kwargs
    )

    return array
