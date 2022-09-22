from __future__ import annotations
from typing import (
    Callable,
    Any,
    Optional
)

from cygorithms.trees.cy_heap import CyBinaryHeap

class Heap:
    def __init__(
        self,
        val: Optional[Any] = None,
        comp: Callable[[Any, Any], bool] = lambda u, v: u < v
    ) -> None:
        if not hasattr(comp, "__call__"):
            raise TypeError(
                "`comp` must be callable,"
                f" got `comp` of type {type(comp).__name__}"
            )
        self.comp = comp
        if val is None:
            self.heap = None
        else:
            self.heap = CyBinaryHeap(val, comp)
    
    def is_empty(self) -> bool:
        if self.heap is None:
            return True
        else:
            return self.heap.is_empty()

    def insert(self, val: Any) -> Heap:
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
