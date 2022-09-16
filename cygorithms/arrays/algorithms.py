from . import c_algorithms
from .arrays import OneDArray
from typing import Callable, Optional
from numbers import Integral


def selection_sort(
    array: OneDArray,
    *,
    comp: Optional[Callable] = None,
    begin: Optional[int] = None,
    end: Optional[int] = None
) -> OneDArray:
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

    c_algorithms.selection_sort(
        array.array,
        **kwargs
    )

    return array


def merge_sort(
    array: OneDArray,
    *,
    comp: Optional[Callable] = None,
    begin: Optional[int] = None,
    end: Optional[int] = None
) -> OneDArray:
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

    c_algorithms.merge_sort(
        array.array,
        **kwargs
    )

    return array
