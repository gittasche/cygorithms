import cython
from cy_trees_src.cy_tree_node cimport CyTreeNode
from cygorithms.arrays.c_array import DynamicOneDArray


cdef class CyBinaryHeap:
    cdef int root_idx
    cdef object heap
    cdef int size
    cdef object comp

    def __init__(self, object val, object comp):
        root = CyTreeNode(val)
        root.is_root = True
        self.root_idx = 0
        self.heap = DynamicOneDArray(CyTreeNode, [root])
        self.size = 1
        self.comp = comp

    @cython.nonecheck(False)
    def __str__(self):
        cdef int i

        all_data = []
        for i in range(self.tree._last_pos_filled + 1):
            if self.heap[i] is not None:
                all_data.append(self.heap[i].data)
        return str(all_data)

    def _heapify(self, int i):
        cdef int target, l, r, j
        cdef object temp
        while True:
            target = i
            l = 2 * i + 1
            r = 2 * i + 2

            for j in range(l, r + 1):
                if j < self.size:
                    if self.comp(self.heap[j].data, self.heap[target].data):
                        target = j
                else:
                    break
            
            if target != i:
                temp = self.heap[i].data
                self.heap[i].data = self.heap[target].data
                self.heap[target].data = temp
                i = target
            else:
                break

    def insert(self, val):
        cdef int i, parent
        cdef object temp
        cdef CyTreeNode new_node
        new_node = CyTreeNode(val)
        self.heap.append(new_node)
        self.size += 1
        i = self.size - 1
        self.heap[i].left = 2 * i + 1
        self.heap[i].right = 2 * i + 2

        while True:
            parent = (i - 1) // 2
            # can not use `i == 0 or self.comp(...)`
            # because Cython checks second condition
            # even in case `i = 0` such that `parent = -1`
            if i == 0:
                break
            if self.comp(self.heap[parent].data, self.heap[i].data):
                break
            else:
                temp = self.heap[i].data
                self.heap[i].data = self.heap[parent].data
                self.heap[parent].data = temp
                i = parent

    def extract(self):
        val_to_extract = self.heap[0].data
        temp = self.heap[0].data
        self.heap[0].data = self.heap[self.size - 1].data
        self.heap[self.size - 1].data = temp
        self.heap.delete(self.size - 1)
        self.size -= 1
        self._heapify(0)
        return val_to_extract

    def is_empty(self):
        return self.size == 0
