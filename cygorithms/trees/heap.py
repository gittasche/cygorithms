from __future__ import annotations
from typing import (
    Callable,
    Any,
    Optional,
    Union
)

from cygorithms.trees.cy_heap import CyBinaryHeap


COMPS = {
    "min": lambda u, v: u < v,
    "max": lambda u, v: u > v
}


class BinaryHeap:
    def __init__(
        self,
        val: Optional[Any] = None,
        comp: Union[Callable[[Any, Any], bool], str] = lambda u, v: u < v
    ) -> None:
        if comp in COMPS:
            self.comp = COMPS[comp]
        elif hasattr(comp, "__call__"):
            self.comp = comp
        else:
            raise TypeError(
                "`comp` must be 'min', 'max' or callable,"
                f" got `comp` of type {type(comp).__name__}"
            )
        if val is None:
            self.heap = None
        else:
            self.heap = CyBinaryHeap(val, comp)

    def is_empty(self) -> bool:
        if self.heap is None:
            return True
        else:
            return self.heap.is_empty()

    def insert(self, val: Any) -> BinaryHeap:
        if self.heap is None:
            self.heap = CyBinaryHeap(val, self.comp)
        else:
            self.heap.insert(val)
        return self

    def extract(self) -> Any:
        if self.is_empty():
            raise ValueError(
                "Heap is empty."
            )
        return self.heap.extract()
