import pytest

from cygorithms.arrays import Stack


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
def test_arrays_stack(dtype, container):
    st = Stack(dtype, data=container)

    assert st.peek() == container[-1]

    assert st.pop() == container[-1]
    assert st.peek() == container[-2]

    st.push(container[-1])
    assert st.peek() == container[-1]

    for _ in container:
        st.pop()
    assert st.is_empty()
