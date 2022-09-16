import pytest

from cygorithms.string import knuth_morris_pratt


@pytest.mark.parametrize(
    "text, query, check",
    [
        (
            "avcaccacac",
            "ac",
            [3, 6, 8]
        ),
        (
            "sfdjfsjd sf sf",
            "sf",
            [0, 9, 12]
        ),
        (
            "asddssdcsad",
            "das",
            []
        )
    ]
)
def test_string(text, query, check):
    res = knuth_morris_pratt(text, query)
    assert res == check
