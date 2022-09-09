import cython
from cygorithms.arrays.c_array import DynamicOneDArray

cdef class CyTreeNode:
    cdef public bint is_root
    cdef public object data
    cdef public int left
    cdef public int right
    cdef public int parent

    def __init__(self, val):
        self.is_root = False
        self.data = val
        self.left = -1
        self.right = -1
        self.parent = -1

cdef class BinaryTree:
    cdef int root_idx
    cdef object tree
    cdef int size
    cdef object comp

    def __init__(self, val, comp):
        root = CyTreeNode(val)
        root.is_root = True
        self.root_idx = 0
        self.tree = DynamicOneDArray(CyTreeNode, [root])
        self.size = 1
        self.comp = comp

    @cython.nonecheck(False)
    def __str__(self):
        cdef int i
        all_data = []
        for i in range(self.tree._last_pos_filled + 1):
            all_data.append(self.tree[i].data)
        return str(all_data)

cdef class BinarySearchTree(BinaryTree):
    def insert(self, val):
        cdef CyTreeNode new_node
        cdef int curr_idx, prev_idx
        new_node = CyTreeNode(val)
        curr_idx = self.root_idx

        if self.tree[curr_idx].data is None:
            self.tree[curr_idx].data = val
            return

        while True:
            if not self.comp(val, self.tree[curr_idx].data):
                if self.tree[curr_idx].right == -1:
                    new_node.parent = curr_idx
                    self.tree.append(new_node)
                    self.tree[curr_idx].right = self.size
                    self.size += 1
                    break
                curr_idx = self.tree[curr_idx].right
            else:
                if self.tree[curr_idx].left == -1:
                    new_node.parent = curr_idx
                    self.tree.append(new_node)
                    self.tree[curr_idx].left = self.size
                    self.size += 1
                    break
                curr_idx = self.tree[curr_idx].left

    def search(self, val):
        cdef int curr_idx
        curr_idx = self.root_idx
        if self.tree[curr_idx].data is None:
            return
        while curr_idx is not None:
            if self.tree[curr_idx].data == val:
                break
            if self.comp(val, self.tree[curr_idx].data):
                curr_idx = self.tree[curr_idx].left
            else:
                curr_idx = self.tree[curr_idx].right
        return curr_idx