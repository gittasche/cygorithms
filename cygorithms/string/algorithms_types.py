import ctypes
from typing import Tuple, Callable

from ..libpath import load_lib


LIB = load_lib()


def set_kmp_traits() -> Tuple[Callable]:
    build_kmp_table_func = LIB.build_kmp_table
    build_kmp_table_func.restype = ctypes.POINTER(ctypes.c_int)
    build_kmp_table_func.argtypes = [
        ctypes.POINTER(ctypes.c_char),
        ctypes.c_size_t
    ]


    do_match_func = LIB.do_match
    do_match_func.restype = ctypes.POINTER(ctypes.c_int)
    do_match_func.argtypes = [
        ctypes.POINTER(ctypes.c_int),
        ctypes.c_char_p,
        ctypes.c_size_t,
        ctypes.c_char_p,
        ctypes.c_size_t,
        ctypes.POINTER(ctypes.c_int)
    ]


    kmp_free = LIB.kmp_free
    kmp_free.restype = None
    kmp_free.argtypes = [
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int)
    ]

    return build_kmp_table_func, do_match_func, kmp_free
