import pytest

from cygorithms.trees import BinaryHeap


@pytest.mark.parametrize(
    "comp, content, sorted_content",
    [
        (
            "min",
            [3, 1, 2, 5, 3, 2, 2, 1, 5, 6, 8, 1, 2, 4, 1],
            [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 5, 5, 6, 8]
        ),
        (
            "max",
            [3, 1, 2, 5, 3, 2, 2, 1, 5, 6, 8, 1, 2, 4, 1],
            [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 5, 5, 6, 8][::-1]
        )
    ]
)
def test_heap(comp, content, sorted_content):
    hp = BinaryHeap(comp=comp)
    assert hp.is_empty()

    for el in content:
        hp.insert(el)

    for check in sorted_content:
        assert hp.extract() == check
