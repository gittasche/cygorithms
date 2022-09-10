import pytest

from cygorithms.arrays import (
    OneDArray,
    DynamicOneDArray,
    selection_sort,
    merge_sort
)


@pytest.mark.parametrize(
    "array_type",
    [
        OneDArray,
        DynamicOneDArray
    ]
)
@pytest.mark.parametrize(
    "dtype, container, filler",
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
        assert arr[2] is None


@pytest.mark.parametrize(
    "array_type",
    [
        OneDArray,
        DynamicOneDArray
    ]
)
@pytest.mark.parametrize(
    "sort_alg",
    [
        selection_sort,
        merge_sort
    ]
)
@pytest.mark.parametrize(
    "dtype, container",
    [
        (
            int,
            [3, 1, 2, 5, 3, 2, 2, 1, 5, 6, 8, 1, 2, 4, 1]
        ),
        (
            str,
            ["c", "d", "a", "c", "ef", "f", "b", "ad", "dd", "e", "b"]
        )
    ]
)
@pytest.mark.parametrize(
    "comp",
    [
        None,
        lambda u, v: u >= v
    ]
)
def test_arrays_algs(array_type, sort_alg, dtype, container, comp):
    arr = array_type(dtype, container)
    if comp is None:
        sorted_container = sorted(container)
    else:
        sorted_container = sorted(container)[::-1]

    sort_alg(arr, comp=comp)
    
    for el, check in zip(sorted_container, arr):
        assert el == check
