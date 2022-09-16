file(GLOB_RECURSE LIB_SOURCES *.c *.h)

add_library(obj_cygorithms_ctypes OBJECT)
target_sources(obj_cygorithms_ctypes PRIVATE ${LIB_SOURCES})

target_include_directories(obj_cygorithms_ctypes
    PRIVATE
    ${cygorithms_ctypes_SOURCE_DIR}/include
)
