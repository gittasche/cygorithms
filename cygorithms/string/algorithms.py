import ctypes
from typing import List

from .algorithms_types import set_kmp_traits


def knuth_morris_pratt(text: str, query: str) -> List[int]:
    """
    Knuth-Morris-Pratt algorithm for pattern
    string search implemented with ctypes.

    Parameters
    ----------
    text : str
        original text to search in
    query : str
        pattern to be searched in ``text``

    Returns
    -------
    positions : list of integers
        positions of occurrences of ``query`` in ``text``
    """
    if not isinstance(text, str):
        raise TypeError(
            "`text` must be a string instance,"
            f" got instance of type {type(text).__name__}"
        )
    if not isinstance(query, str):
        raise TypeError(
            "`query` must be a string instance,"
            f" got instance of type {type(query).__name__}"
        )

    if len(text) == 0 or len(query) == 0:
        return []

    build_kmp_table_func, do_match_func, kmp_free = set_kmp_traits()

    c_text = ctypes.c_char_p(bytes(text, "utf-8"))
    c_text_len = ctypes.c_size_t(len(text))
    c_query = ctypes.c_char_p(bytes(query, "utf-8"))
    c_query_len = ctypes.c_size_t(len(query))
    c_num_positions = ctypes.c_int(0)

    c_kmp_table = build_kmp_table_func(c_query, c_query_len)
    c_positions = do_match_func(
        ctypes.byref(c_num_positions),
        c_text,
        c_text_len,
        c_query,
        c_query_len,
        c_kmp_table
    )
    positions = [c_positions[i] for i in range(c_num_positions.value)]
    kmp_free(c_positions, c_kmp_table)

    return positions
