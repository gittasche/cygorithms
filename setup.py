import subprocess
import logging
import os
from platform import system
from setuptools import setup, find_packages, Extension
from setuptools.command import build_ext
from Cython.Build import cythonize
from codecs import open


__name__ = "cygorithms"
__version__ = "0.0.1"


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


extensions = []
extensions.extend(get_array_ext())
extensions.extend(get_linked_list_ext())
extensions.extend(get_trees_ext())


# class CMakeExtension(Extension):
#     def __init__(self, name, sources):
#         super().__init__(name=name, sources=[])


# class BuildExt(build_ext.build_ext):
#     logger = logging.getLogger("CYgorithms build_ext")

#     def build(
#         self,
#         src_dir,
#         build_dir,
#         generator,
#         build_tool = None
#     ):
#         cmake_cmd = ["cmake", src_dir, generator]
#         self.logger.info(f"Run CMake command: {cmake_cmd}")
#         subprocess.check_call(cmake_cmd, cwd=build_dir)

#         if system() != "Windows":
#             subprocess.check_call([build_tool], cwd=build_dir)
#         else:
#             subprocess.check_call(["cmake", "--build", ".",
#                                    "--config", "Release"], cwd=build_dir)
    
#     def build_cmake_extension(self):
#         build_dir = self.build_temp
#         src_dir = "cygorithms_ctypes"
        
#         if not os.path.exists(build_dir):
#             os.mkdir(build_dir)
        
#         if system() == "Windows":
#             vs = "-GVisual Studio 17 2022"
#             self.build(src_dir, build_dir, vs)



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
    setup_requires=["Cython>=0.29.32"],
    packages=find_packages(),
    ext_modules=cythonize(extensions),
    include_package_data=True,
    zip_safe=False
)
