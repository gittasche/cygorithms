import pytest

from cygorithms.linked_list import (
    SingleLinkedList,
    SingleCircularLinkedList,
    DoubleLinkedList,
    DoubleCircularLinkedList
)

@pytest.mark.parametrize("list_type",
    [
        SingleLinkedList,
        SingleCircularLinkedList,
        DoubleLinkedList,
        DoubleCircularLinkedList
    ]
)
def test_linked_list(list_type):
    l = list_type([1, 2, 3], [1, 2], [1])
    if "Circular" in list_type.__name__:
        assert l.insert_after(5, [0, 0]).insert_after(6, [1, 1]).popright()[3] == [1, 1]
    else:
        assert l.insert_after(2, [0, 0]).insert_after(-1, [1, 1]).popright()[3] == [0, 0]

    l = list_type([1, 2, 3], [1, 2], [1])
    assert l.addleft([-1, -1]).addleft([-2, -2])[1] == [-1, -1]

    l = list_type([1, 2, 3], [1, 2], [1])
    assert l.addleft([-1, -1]).addleft([-2, -2]).insert_after(0, [0, 0]).popleft()[0] == [0, 0]

    l = list_type([1, 2, 3], [1, 2], [1])
    assert l.popright().popleft().insert_after(0, [0, 0])[0] == [1, 2]
