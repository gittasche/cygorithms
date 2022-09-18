import pytest

from cygorithms.trees import (
    BinarySearchTree,
    BinaryTreeTraversal
)


def test_binary_tree():
    bst = BinarySearchTree()
    assert bst.is_empty()

    bst.insert(3)
    assert bst.search(3)
    assert not bst.is_empty()
    bst.delete(3)
    assert not bst.search(3)
    assert bst.is_empty()

    # build binary search tree
    # 	      2
    #       /   \
    #      0     4
    #     / \   / \
    #   -1   1 3   5
    bst.insert(2)
    bst.insert(4)
    bst.insert(3)
    bst.insert(5)
    bst.insert(0)
    bst.insert(1)
    bst.insert(-1)

    assert bst.search(1)
    assert bst.search(0)
    assert bst.search(3)

    bst.delete(5)
    bst.delete(-1)
    bst.delete(2)
    bst.delete(4)

    assert not bst.search(-1)
    assert not bst.search(2)
    assert bst.search(3)

    bst.delete(0)
    bst.delete(3)
    bst.delete(1)

    assert bst.is_empty()


@pytest.mark.parametrize(
    "strategy, order, check",
    [
        (
            "depth_first_search",
            "in_order",
            [-1, 0, 1, 2, 3, 4, 5]
        ),
        (
            "depth_first_search",
            "pre_order",
            [2, 0, -1, 1, 4, 3, 5]
        ),
        (
            "depth_first_search",
            "post_order",
            [-1, 1, 0, 3, 5, 4, 2]
        ),
        (
            "breadth_first_search",
            None,
            [2, 0, 4, -1, 1, 3, 5]
        )
    ]
)
def test_binary_tree_traversal(strategy, order, check):
    bst = BinarySearchTree()

    # build binary search tree
    # 	      2
    #       /   \
    #      0     4
    #     / \   / \
    #   -1   1 3   5
    bst.insert(2)
    bst.insert(4)
    bst.insert(3)
    bst.insert(5)
    bst.insert(0)
    bst.insert(1)
    bst.insert(-1)

    btt = BinaryTreeTraversal(bst)
    args = (order,) if order is not None else ()
    assert getattr(btt, strategy)(*args) == check
