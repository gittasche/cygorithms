cmake_minimum_required(VERSION 3.14 FATAL_ERROR)

project(cygorithms_ctypes
    VERSION 0.0.1
    DESCRIPTION "Ctypes utilities for cygorithms."
    LANGUAGES C)

message(STATUS "CMake version ${CMAKE_VERSION}")

include(GNUInstallDirs)

option(BUILD_STATIC_LIB "Build static library" OFF)

add_subdirectory(${cygorithms_ctypes_SOURCE_DIR}/src)

if (BUILD_STATIC_LIB)
    add_library(cygorithms_ctypes STATIC)
else (BUILD_STATIC_LIB)
    add_library(cygorithms_ctypes SHARED)
endif (BUILD_STATIC_LIB)
target_link_libraries(cygorithms_ctypes PRIVATE obj_cygorithms_ctypes)
target_include_directories(cygorithms_ctypes
    INTERFACE
    $<INSTALL_INTERFACE:$<INSTALL_PREFIX>/include>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}/include>)
