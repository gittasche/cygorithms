cdef class CyTreeNode:
    def __init__(self, object val):
        self.is_root = False
        self.data = val
        self.left = -1
        self.right = -1
        self.parent = -1

    def __str__(self):
        return str(self.data)
