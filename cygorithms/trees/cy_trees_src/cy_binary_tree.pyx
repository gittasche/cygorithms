import cython
from cy_trees_src.cy_tree_node cimport CyTreeNode
from cygorithms.arrays.c_array import DynamicOneDArray, OneDArray
from cygorithms.arrays.c_array import ArrayStack, ArrayQueue


cdef class CyBinaryTree:
    cdef int root_idx
    cdef object tree
    cdef int size
    cdef object comp

    def __init__(self, object val, object comp):
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


cdef class CyBinarySearchTree(CyBinaryTree):
    def is_empty(self):
        return self.tree[self.root_idx].data is None
    
    def insert(self, object val):
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

    def search(self, object val):
        cdef int curr_idx

        curr_idx = self.root_idx
        if self.tree[curr_idx].data is None:
            return -1
        while curr_idx != -1:
            if self.tree[curr_idx].data == val:
                break
            if self.comp(val, self.tree[curr_idx].data):
                curr_idx = self.tree[curr_idx].left
            else:
                curr_idx = self.tree[curr_idx].right
        return curr_idx

    def delete(self, object val):
        cdef int curr_idx, succ, succ_parent, child

        curr_idx = self.search(val)
        if curr_idx == -1:
            return

        if self.tree[curr_idx].left == -1 and self.tree[curr_idx].right == -1:
            if self.tree[curr_idx].is_root:
                self.tree[self.root_idx].data = None
            else:
                if self.tree[self.tree[curr_idx].parent].left == curr_idx:
                    self.tree[self.tree[curr_idx].parent].left = -1
                else:
                    self.tree[self.tree[curr_idx].parent].right = -1
                self.tree.delete(curr_idx)

        elif self.tree[curr_idx].left != -1 and self.tree[curr_idx].right != -1:
            succ = self.tree[curr_idx].right
            succ_parent = succ
            while self.tree[succ].left != -1:
                succ_parent = succ
                succ = self.tree[succ].left
            self.tree[curr_idx].data = self.tree[succ].data
            if succ != self.root_idx:
                self.tree[succ_parent].left = self.tree[succ].right
            else:
                self.tree[succ_parent].right = self.tree[succ].right
            if self.tree[succ].right != -1:
                self.tree[self.tree[succ].right].parent = succ_parent
            if succ != -1:
                self.tree.delete(succ)

        else:
            if self.tree[curr_idx].left != -1:
                child = self.tree[curr_idx].left
            else:
                child = self.tree[curr_idx].right
            if self.tree[curr_idx].is_root:
                self.tree[self.root_idx].left = self.tree[child].left
                self.tree[self.root_idx].right = self.tree[child].right
                self.tree[self.root_idx].data = self.tree[child].data
                self.tree[self.root_idx].parent = -1
                self.tree.delete(child)
            else:
                if self.tree[self.tree[curr_idx].parent].left == curr_idx:
                    self.tree[self.tree[curr_idx].parent].left = child
                else:
                    self.tree[self.tree[curr_idx].parent].right = child
                self.tree[child].parent = self.tree[curr_idx].parent
                self.tree.delete(curr_idx)


cdef class CyBinaryTreeTraversal:
    cdef CyBinaryTree tree

    def __init__(self, CyBinaryTree tree):
        self.tree = tree
    
    def _in_order(self):
        cdef object st
        cdef int node

        visit = []
        node = self.tree.root_idx
        st = ArrayStack(int, 0, [])
        while not st.is_empty() or node != -1:
            if node != -1:
                st.push(node)
                node = self.tree.tree[node].left
            else:
                node = st.pop(node)
                visit.append(self.tree.tree[node].data)
                node = self.tree.tree[node].right
        return visit

    def _pre_order(self):
        cdef object st
        cdef int node

        visit = []
        node = self.tree.root_idx
        st = ArrayStack(int, 1, [node])
        while not st.is_empty():
            node = st.pop()
            visit.append(self.tree.tree[node].data)
            if self.tree.tree[node].right != -1:
                st.push(self.tree.tree[node].right)
            if self.tree.tree[node].left != -1:
                st.push(self.tree.tree[node].left)
        return visit

    def _post_order(self):
        cdef object st, last
        cdef int node, l, r

        visit = []
        node = self.tree.root_idx
        st = ArrayStack(int, 1, [node])
        last = OneDArray(int, self.tree.size)
        last.fill(0)
        while not st.is_empty():
            node = st.peek()
            l = self.tree.tree[node].left
            r = self.tree.tree[node].right
            if (l == -1 or last[l]) and (r == -1 or last[r]):
                st.pop()
                visit.append(self.tree.tree[node].data)
                last[node] = 1
                continue
            if not (r == -1 or last[r]):
                st.push(r)
            if not (l == -1 or last[l]):
                st.push(l)
        return visit

    def breadth_first_search(self):
        cdef object qu
        cdef int node
        node = self.tree.root_idx
        visit = []
        qu = ArrayQueue(int, 1, [node])
        while not qu.is_empty():
            node = qu.pop()
            visit.append(self.tree.tree[node].data)
            if self.tree.tree[node].left != -1:
                qu.push(self.tree.tree[node].left)
            if self.tree.tree[node].right != -1:
                qu.push(self.tree.tree[node].right)
        return visit
