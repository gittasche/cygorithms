import os
import platform
import ctypes


def find_lib_path() -> str:
    """
    Get path to ctypes extension
    """
    curr_path = os.path.abspath(os.path.dirname(os.path.expanduser(__file__)))
    if platform.system() == "Windows":
        dll_path = "cygorithms_ctypes.dll"
    elif platform.system() == "Linux":
        dll_path = "libcygorithms_ctypes.so"
    ctypes_lib_path = os.path.join(curr_path, dll_path)

    if not os.path.exists(ctypes_lib_path) or not os.path.isfile(ctypes_lib_path):
        raise ModuleNotFoundError(
            "Ctypes extension for CYgorithms"
            f" not found in candidate path {ctypes_lib_path}."
            f" Python package path {curr_path}."
        )

    return ctypes_lib_path


def load_lib() -> ctypes.CDLL:
    """
    Load ctypes extension from path
    """
    lib_path = find_lib_path()
    lib_success = False
    try:
        lib = ctypes.cdll.LoadLibrary(lib_path)
        setattr(lib, "path", os.path.normpath(lib_path))
        lib_success = True
    except OSError as e:
        err_msg = e
    if not lib_success:
        libname = os.path.basename(lib_path)
        raise ModuleNotFoundError(
            f"CYgorithms library ({libname}) could not be loaded."
            f"Error message: {err_msg}"
        )
    return lib
