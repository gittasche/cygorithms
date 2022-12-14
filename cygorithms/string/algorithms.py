import ctypes
import os.path
import platform
from typing import List


curr_dir = os.path.abspath(os.path.dirname(os.path.expanduser(__file__)))
if platform.system() == "Windows":
    rel_lib_path = "../cygorithms_ctypes.dll"
elif platform.system() == "Linux":
    rel_lib_path = "../libcygorithms_ctypes.so"
kmp_path = os.path.join(curr_dir, rel_lib_path)
kmp_lib = ctypes.cdll.LoadLibrary(kmp_path)


build_kmp_table_func = kmp_lib.build_kmp_table
build_kmp_table_func.restype = ctypes.POINTER(ctypes.c_int)
build_kmp_table_func.argtypes = [
    ctypes.POINTER(ctypes.c_char),
    ctypes.c_size_t
]


do_match_func = kmp_lib.do_match
do_match_func.restype = ctypes.POINTER(ctypes.c_int)
do_match_func.argtypes = [
    ctypes.POINTER(ctypes.c_int),
    ctypes.c_char_p,
    ctypes.c_size_t,
    ctypes.c_char_p,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_int)
]


kmp_free = kmp_lib.kmp_free
kmp_free.restype = None
kmp_free.argtypes = [
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int)
]


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
