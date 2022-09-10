from . import c_algorithms
from .arrays import OneDArray
from typing import Callable, Optional


def selection_sort(
    array: OneDArray,
    *,
    comp: Optional[Callable] = None,
    begin: Optional[int] = None,
    end: Optional[int] = None
) -> OneDArray:
    kwargs = {}
    if comp is not None:
        kwargs["comp"] = comp
    if begin is not None:
        kwargs["begin"] = begin
    if end is not None:
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
    begin: Optional[Callable] = None,
    end: Optional[Callable] = None
) -> OneDArray:
    kwargs = {}
    if comp is not None:
        kwargs["comp"] = comp
    if begin is not None:
        kwargs["begin"] = begin
    if end is not None:
        kwargs["end"] = end

    c_algorithms.merge_sort(
        array.array,
        **kwargs
    )

    return array
