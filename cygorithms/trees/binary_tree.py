from __future__ import annotations
from typing import Callable, Any, List, Literal

from cygorithms.trees.cy_trees import (
    CyBinaryTree,
    CyBinarySearchTree,
    CyBinaryTreeTraversal
)


class BinaryTree:
    def __init__(
        self,
        tree_type: CyBinaryTree,
        val: Any,
        comp: Callable = lambda u, v: u < v
    ):
        self.tree = tree_type(val, comp)

    def __str__(self) -> str:
        return self.__str__

    def insert(self, val: Any) -> BinaryTree:
        self.tree.insert(val)
        return self

    def delete(self, val: Any) -> BinaryTree:
        self.tree.delete(val)
        return self

    def search(self, val: Any) -> int:
        idx = self.tree.search(val)
        return idx


class BinarySearchTree(BinaryTree):
    def __init__(self, val: Any, comp: Callable = lambda u, v: u < v):
        super().__init__(CyBinarySearchTree, val, comp)


class BinaryTreeTraversal:
    def __init__(self, tree: BinaryTree):
        self.proc = CyBinaryTreeTraversal(tree.tree)

    def depth_first_search(self, order: Literal["in_order"] = "in_order") -> List[Any]:
        if order not in ("in_order",):
            raise ValueError(
                "Got unknown order."
            )
        return getattr(self.proc, "_" + order)()