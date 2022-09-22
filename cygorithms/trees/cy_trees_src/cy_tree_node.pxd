cdef class CyTreeNode:
    cdef public bint is_root
    cdef public object data
    cdef public int left
    cdef public int right
    cdef public int parent
