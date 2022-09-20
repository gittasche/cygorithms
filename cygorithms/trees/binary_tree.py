from __future__ import annotations
from typing import (
    Callable,
    Any,
    List,
    Literal,
    Optional
)

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
        comp: Callable[[Any, Any], bool] = lambda u, v: u < v
    ):
        if not hasattr(comp, "__call__"):
            raise TypeError(
                "`comp` must be callable,"
                f" got `comp` of type {type(comp).__name__}"
            )
        self.tree = tree_type(val, comp)

    def __str__(self) -> str:
        return self.tree.__str__()

    def is_empty(self) -> bool:
        return self.tree.is_empty()

    def insert(self, val: Any) -> BinaryTree:
        self.tree.insert(val)
        return self

    def delete(self, val: Any) -> BinaryTree:
        self.tree.delete(val)
        return self

    def search(self, val: Any) -> bool:
        idx = self.tree.search(val)
        return idx != -1


class BinarySearchTree(BinaryTree):
    def __init__(
        self,
        val: Optional[Any] = None,
        comp: Callable[[Any, Any], bool] = lambda u, v: u < v
    ):
        super().__init__(CyBinarySearchTree, val, comp)


class BinaryTreeTraversal:
    def __init__(self, tree: BinaryTree):
        self.proc = CyBinaryTreeTraversal(tree.tree)

    def depth_first_search(
        self,
        order: Literal["in_order", "pre_order", "post_order"] = "in_order"
    ) -> List[Any]:
        if order not in ("in_order", "pre_order", "post_order"):
            raise ValueError(
                "Got unknown order."
            )
        return getattr(self.proc, "_" + order)()

    def breadth_first_search(self) -> List[Any]:
        return self.proc.breadth_first_search()
