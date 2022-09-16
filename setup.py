import os
import logging
import subprocess
import shutil
from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
from codecs import open
from setuptools.command import build_ext, install_lib
from platform import system


__name__ = "cygorithms"
__version__ = "0.0.1"

CURR_DIR = os.path.abspath(os.path.dirname(__file__))


def lib_name():
    if system() == "Windows":
        name = "cygorithms_ctypes.dll"
    elif system() == "Linux":
        name = "libcygorithms_ctypes.so"
    return name


class CMakeExtension(Extension):
    def __init__(self, name):
        super().__init__(name=name, sources=[])


class BuildExt(build_ext.build_ext):
    logger = logging.getLogger("CYgorithms build_ext")

    def build_extension(self, ext):
        if isinstance(ext, CMakeExtension):
            self.build_cmake_extension()
        else:
            super().build_extension(ext)

    def build_cmake_extension(self):
        ext_lib_name = lib_name()

        lib_package_path = os.path.join(CURR_DIR, __name__, ext_lib_name)
        if os.path.exists(lib_package_path):
            self.logger.info("Found shared library, skipping build.")

        ext_src_dir = os.path.join(CURR_DIR, "cygorithms_ctypes")
        if not os.path.exists(ext_src_dir):
            raise OSError(
                f"CMake source directory {ext_src_dir} not found."
            )
        
        ext_build_dir = os.path.join(ext_src_dir, "build")

        self.logger.info(f"Building from source. {ext_lib_name}")
        if not os.path.exists(ext_build_dir):
            os.mkdir(ext_build_dir)

        self.build(ext_src_dir, ext_build_dir)
        if system() == "Windows":
            lib_path = os.path.join(ext_build_dir, "Release", ext_lib_name)
        elif system() == "Linux":
            lib_path = os.path.join(ext_build_dir, ext_lib_name)
        lib_dst_path = os.path.join(CURR_DIR, __name__)
        shutil.copy(lib_path, lib_dst_path)

    def build(self, src_dir, build_dir):
        if system() == "Windows":
            cmake_cmd = [
                "cmake",
                src_dir,
                "-GVisual Studio 17 2022",
                "-DCMAKE_CONFIGURATION_TYPES=Release",
                "-A",
                "x64"
            ]
            cmake_build_cmd = [
                "cmake",
                "--build",
                build_dir,
                "--config",
                "Release"
            ]
        elif system() == "Linux":
            cmake_cmd = [
                "cmake",
                src_dir,
                "-DBUILD_STATIC_LIB=OFF",
                "-GNinja"
            ]
            cmake_build_cmd = [
                "cmake",
                "--build",
                build_dir
            ]

        os.chdir(build_dir)
        subprocess.run(cmake_cmd)
        subprocess.run(cmake_build_cmd)
        os.chdir(CURR_DIR)


class InstallLib(install_lib.install_lib):
    logger = logging.getLogger("CYgorithms install_lib")

    def install(self):
        outfiles = super().install()

        dst = os.path.join(self.install_dir, __name__, lib_name())
        src = os.path.join(CURR_DIR, __name__, lib_name())
        self.logger.info(f"Installing shared library: {src}")
        dst, _ = self.copy_file(src, dst)
        outfiles.append(dst)
        return outfiles


def get_array_ext():
    array_name = ".".join([__name__, "arrays", "c_array"])
    array_sources = [
        "/".join([__name__, "arrays", "c_array_src", "array.c"])
    ]

    array_ext = Extension(
        name=array_name,
        sources=array_sources
    )

    algorithms_name = ".".join([__name__, "arrays", "c_algorithms"])
    algorithms_sources = [
        "/".join([__name__, "arrays", "c_algorithms_src", "algorithms.c"])
    ]

    algorithms_ext = Extension(
        name=algorithms_name,
        sources=algorithms_sources
    )

    array_ext_full = [array_ext, algorithms_ext]

    return array_ext_full


def get_linked_list_ext():
    linked_list_name = ".".join([__name__, "linked_list", "cy_linked_list"])
    linked_list_sources = [
        "/".join([__name__, "linked_list", "cy_linked_list_src", "cy_linked_list.pyx"])
    ]

    linked_list_ext = Extension(
        name=linked_list_name,
        sources=linked_list_sources
    )

    linked_list_ext_full = [linked_list_ext]

    return linked_list_ext_full


def get_trees_ext():
    trees_name = ".".join([__name__, "trees", "cy_trees"])
    trees_sources = [
        "/".join([__name__, "trees", "cy_trees_src", "cy_binary_tree.pyx"])
    ]

    trees_ext = Extension(
        name=trees_name,
        sources=trees_sources
    )

    trees_ext_full = [trees_ext]

    return trees_ext_full


def get_cmake_ext():
    cmake_ext_name = "cygorithms_ctypes"

    cmake_ext = CMakeExtension(
        name=cmake_ext_name
    )

    cmake_ext_full = [cmake_ext]
    return cmake_ext_full


extensions = []
extensions.extend(get_array_ext())
extensions.extend(get_linked_list_ext())
extensions.extend(get_trees_ext())
extensions.extend(get_cmake_ext())


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name=__name__,
    version=__version__,
    description="Algorithms written on Cython",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: C",
        "Programming Language :: Python",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    author="gittasche",
    python_requires=">=3.9",
    setup_requires=["Cython>=0.29.32", "cmake>=3.14"],
    packages=find_packages(),
    ext_modules=cythonize(extensions),
    cmdclass={
        "build_ext": BuildExt,
        "install_lib": InstallLib
    },
    include_package_data=True,
    zip_safe=False
)
