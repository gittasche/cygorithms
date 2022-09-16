import ctypes
import sys
import os.path


curr_dir = os.path.abspath(os.path.dirname(os.path.expanduser(__file__)))
if sys.platform == "win32":
    kmp_extension = ".dll"
elif sys.platform.startswith("Linux"):
    kmp_extension = ".so"
kmp_path = os.path.join(curr_dir, "../../cygorithms_ctypes/build/Debug/cygorithms_ctypes" + kmp_extension)
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


def knuth_morris_pratt(text, query):
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
    positions = [c_positions[i] for i in range(2)]

    return positions
