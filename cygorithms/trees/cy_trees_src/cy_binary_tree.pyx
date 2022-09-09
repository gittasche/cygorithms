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
            if self.tree[i] is not None:
                all_data.append(self.tree[i].data)
        return str(all_data)

cdef class BinarySearchTree(BinaryTree):
    def insert(self, val):
        cdef int curr_idx
        curr_idx = self.search(val)
        if curr_idx != -1:
            return

        curr_idx = self.root_idx
        if self.tree[curr_idx].data is None:
            self.tree[curr_idx].data = val
            return

        cdef CyTreeNode new_node
        new_node = CyTreeNode(val)

        while True:
            if self.comp(val, self.tree[curr_idx].data):
                if self.tree[curr_idx].left == -1:
                    new_node.parent = curr_idx
                    self.tree.append(new_node)
                    self.tree[curr_idx].left = self.size
                    self.size += 1
                    break
                curr_idx = self.tree[curr_idx].left
            else:
                if self.tree[curr_idx].right == -1:
                    new_node.parent = curr_idx
                    self.tree.append(new_node)
                    self.tree[curr_idx].right = self.size
                    self.size += 1
                    break
                curr_idx = self.tree[curr_idx].right

        return self

    def search(self, val):
        cdef int curr_idx
        curr_idx = self.root_idx
        if self.tree[curr_idx].data is None:
            return
        while curr_idx != -1:
            if self.tree[curr_idx].data == val:
                break
            if self.comp(val, self.tree[curr_idx].data):
                curr_idx = self.tree[curr_idx].left
            else:
                curr_idx = self.tree[curr_idx].right
        return curr_idx

    def delete(self, val):
        cdef int curr_idx, succ, succ_parent, child
        cdef object new_indices, root_data

        curr_idx = self.search(val)
        if curr_idx == -1:
            return

        if self.tree[curr_idx].left == -1 and self.tree[curr_idx].right == -1:
            if self.tree[curr_idx].parent == -1:
                self.tree[self.root_idx].data = None
            else:
                if self.tree[self.tree[curr_idx].parent].left == curr_idx:
                    self.tree[self.tree[curr_idx].parent].left = -1
                else:
                    self.tree[self.tree[curr_idx].parent].right = -1
                new_indices = self.tree.delete(curr_idx)
                # if new_indices is not None:
                #     root_data = self.tree[self.root_idx].data
                #     self.root_idx = new_indices[root_data]

        elif self.tree[curr_idx].left != -1 and self.tree[curr_idx].right != -1:
            succ = self.tree[curr_idx].right
            succ_parent = succ
            while self.tree[succ].left != -1:
                succ_parent = succ
                succ = self.tree[succ].left
            if succ != self.root_idx:
                self.tree[succ_parent].left = self.tree[succ].right
            else:
                self.tree[succ_parent].right = self.tree[succ].right
            if self.tree[succ].right != -1:
                self.tree[self.tree[succ].right].parent = succ_parent
            if succ != -1:
                # root_data = self.tree[self.root_idx].data
                new_indices = self.tree.delete(succ)
                # if new_indices is not None:
                #     self.root_idx = new_indices[root_data]

        else:
            if self.tree[curr_idx].left != -1:
                child = self.tree[curr_idx].left
            else:
                child = self.tree[curr_idx].right
            if self.tree[curr_idx].parent == -1:
                self.tree[self.root_idx].left = self.tree[child].left
                self.tree[self.root_idx].right = self.tree[child].right
                self.tree[self.root_idx].data = self.tree[child].data
                self.tree[self.root_idx].parent = -1
                root_data = self.tree[self.root_idx].data
                new_indices = self.tree.delete(child)
                if new_indices is not None:
                    self.root_idx = new_indices[root_data]
            else:
                if self.tree[self.tree[curr_idx].parent].left == curr_idx:
                    self.tree[self.tree[curr_idx].parent].left = child
                else:
                    self.tree[self.tree[curr_idx].parent].right = child
                self.tree[child].parent = self.tree[curr_idx].parent
                # root_data = self.tree[self.root_idx].data
                new_indices = self.tree.delete(curr_idx)
                # if new_indices is not None:
                #     self.tree[curr_idx].parent = new_indices
            
        return self