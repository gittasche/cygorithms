import pytest

from cygorithms.arrays import Queue


@pytest.mark.parametrize(
    "dtype, container",
    [
        (
            int,
            [1, 2, 3, 4, 5]
        ),
        (
            str,
            ["a", "b", "c", "d", "e"]
        )
    ]
)
def test_arrays_queue(dtype, container):
    qu = Queue(dtype, container)

    assert qu.peek() == container[0]

    assert qu.pop() == container[0]
    assert qu.peek() == container[1]

    qu.push(container[0])
    assert qu.peek() == container[1]

    for _ in container:
        qu.pop()
    assert qu.is_empty()
