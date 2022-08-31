import pytest

from cygorithms.arrays import (
    OneDArray,
    DynamicOneDArray
)

@pytest.mark.parametrize("array_type",
    [
        OneDArray,
        DynamicOneDArray
    ]
)
@pytest.mark.parametrize("dtype, container, filler",
    [
        (
            int,
            [1, 2, 3, 4],
            5
        ),
        (
            str,
            ["a", "b", "c", "d"],
            "e"
        ),
        (
            tuple,
            [(1, 2, 3, 4), (1, 2, 3), (1, 2), (1,)],
            (0,)
        )
    ]
)
def test_arrays(array_type, dtype, container, filler):
    print(container)
    arr = array_type(dtype, 4, container)
    assert len(arr) == arr.size
    for el, check in zip(arr, container):
        assert el == check

    if "Dynamic" in array_type.__class__.__name__:
        arr.append(filler)
        assert arr[4] == filler
        arr.delete(2)
        assert arr[2] == None
