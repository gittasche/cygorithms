import cython

cdef class CyLinkedListNode:
    cdef object data
    cdef CyLinkedListNode next

    def __init__(self, val):
        self.data = val
        self.next = None

cdef class CyDoubleLinkedListNode:
    cdef object data
    cdef CyDoubleLinkedListNode next
    cdef CyDoubleLinkedListNode prev

    def __init__(self, val):
        self.data = val
        self.next = None
        self.prev = None

cdef class CyBaseLinkedList:
    cdef CyLinkedListNode begin
    cdef CyLinkedListNode end
    cdef int list_len

    def __init__(self):
        self.begin = None
        self.end = None
        self.list_len = 0

    @cython.nonecheck(False)
    cdef CyLinkedListNode get_node(self, int index):
        cdef CyLinkedListNode current
        cdef int i

        current = self.begin
        for i in range(index):
            current = current.next
        return current

    @cython.nonecheck(False)
    def __len__(self):
        return self.list_len

    @cython.nonecheck(False)
    def __str__(self):
        all_data = []
        current = self.begin

        while current is not None:
            all_data.append(current.data)
            current = current.next
            if current is self.begin:
                break

        return str(all_data)

    def __setitem__(self, int index, object val):
        self.get_node(index).data = val

    def __getitem__(self, int index):
        return self.get_node(index).data

cdef class CyLinkedList(CyBaseLinkedList):
    def addright(self, object val):
        cdef CyLinkedListNode new_node
        new_node = CyLinkedListNode(val)

        if self.begin is None:
            self.begin = new_node
            self.end = new_node
        else:
            self.end.next = new_node
            self.end = new_node

        self.list_len += 1
        return self

    def addleft(self, object val):
        cdef CyLinkedListNode new_node
        new_node = CyLinkedListNode(val)

        if self.begin is None:
            self.begin = new_node
            self.end = new_node
        else:
            new_node.next = self.begin
            self.begin = new_node

        self.list_len += 1
        return self

    def popright(self):
        if self.list_len <= 1:
            self.begin = None
            self.end = None
            self.list_len = 0
        else:
            pre_end = self.get_node(self.list_len - 2)
            self.end = pre_end
            self.end.next = None
            self.list_len -= 1

        return self

    def popleft(self):
        if self.list_len <= 1:
            self.begin = None
            self.end = None
            self.list_len = 0
        else:
            self.begin = self.begin.next
            self.list_len -= 1

        return self

    @cython.nonecheck(False)
    def insert_after(self, int index, object val):
        cdef CyLinkedListNode new_node
        new_node = CyLinkedListNode(val)
        current = self.get_node(index)

        new_node.next = current.next
        current.next = new_node
        if new_node.next is None:
            self.end = new_node

        self.list_len += 1
        return self

cdef class CyCircularLinkedList(CyLinkedList):
    def addright(self, object val):
        cdef CyLinkedListNode new_node
        new_node = CyLinkedListNode(val)

        if self.begin is None:
            self.begin = new_node
            self.end = new_node
        else:
            self.end.next = new_node
            self.end = new_node
            self.end.next = self.begin

        self.list_len += 1
        return self
        
    def addleft(self, object val):
        cdef CyLinkedListNode new_node
        new_node = CyLinkedListNode(val)

        if self.begin is None:
            self.begin = new_node
            self.end = new_node
        else:
            new_node.next = self.begin
            self.begin = new_node
            self.end.next = self.begin

        self.list_len += 1
        return self

    def popright(self):
        if self.list_len <= 1:
            self.begin = None
            self.end = None
            self.list_len = 0
        else:
            pre_end = self.get_node(self.list_len - 2)
            self.end = pre_end
            self.end.next = self.begin
            self.list_len -= 1

        return self

    def popleft(self):
        if self.list_len <= 1:
            self.begin = None
            self.end = None
            self.list_len = 0
        else:
            self.begin = self.begin.next
            self.end.next = self.begin
            self.list_len -= 1

        return self

    @cython.nonecheck(False)
    def insert_after(self, int index, object val):
        cdef CyLinkedListNode new_node
        new_node = CyLinkedListNode(val)
        current = self.get_node(index)

        new_node.next = current.next
        current.next = new_node
        if new_node.next is self.begin:
            self.end = new_node

        self.list_len += 1
        return self


cdef class CyBaseDoubleLinkedList:
    cdef CyDoubleLinkedListNode begin
    cdef CyDoubleLinkedListNode end
    cdef int list_len

    def __init__(self):
        self.begin = None
        self.end = None
        self.list_len = 0

    @cython.nonecheck(False)
    cdef CyDoubleLinkedListNode get_node(self, int index):
        cdef CyDoubleLinkedListNode current
        cdef int i, reduced_idx
        reduced_idx = index % self.list_len

        if reduced_idx <= self.list_len // 2:
            current = self.begin
            for i in range(reduced_idx):
                current = current.next
        else:
            current = self.end
            for i in range(self.list_len - reduced_idx - 1):
                current = current.prev

        return current

    @cython.nonecheck(False)
    def __len__(self):
        return self.list_len

    @cython.nonecheck(False)
    def __str__(self):
        all_data = []
        current = self.begin

        while current is not None:
            all_data.append(current.data)
            current = current.next
            if current is self.begin:
                break

        return str(all_data)

    def __setitem__(self, int index, object val):
        self.get_node(index).data = val

    def __getitem__(self, int index):
        return self.get_node(index).data

cdef class CyDoubleLinkedList(CyBaseDoubleLinkedList):
    def addright(self, object val):
        cdef CyDoubleLinkedListNode new_node
        new_node = CyDoubleLinkedListNode(val)

        if self.begin is None:
            self.begin = new_node
            self.end = new_node
        else:
            new_node.prev = self.end
            self.end.next = new_node
            self.end = new_node

        self.list_len += 1
        return self
    
    def addleft(self, object val):
        cdef CyDoubleLinkedListNode new_node
        new_node = CyDoubleLinkedListNode(val)

        if self.begin is None:
            self.begin = new_node
            self.end = new_node
        else:
            new_node.next = self.begin
            self.begin.prev = new_node
            self.begin = new_node

        self.list_len += 1
        return self
        
    def popright(self):
        if self.list_len <= 1:
            self.begin = None
            self.end = None
            self.list_len = 0
        else:
            self.end = self.end.prev
            self.end.next = None
            self.list_len -= 1

        return self

    def popleft(self):
        if self.list_len <= 1:
            self.begin = None
            self.end = None
            self.list_len = 0
        else:
            self.begin = self.begin.next
            self.begin.prev = None
            self.list_len -= 1

        return self
        
    @cython.nonecheck(False)
    def insert_after(self, int index, object val):
        cdef CyDoubleLinkedListNode new_node
        new_node = CyDoubleLinkedListNode(val)
        current = self.get_node(index)

        new_node.next = current.next
        if new_node.next is not None:
            new_node.next.prev = new_node
        current.next = new_node
        new_node.prev = current
        if new_node.next is None:
            self.end = new_node

        self.list_len += 1
        return self

cdef class CyDoubleCircularLinkedList(CyDoubleLinkedList):
    def addright(self, object val):
        cdef CyDoubleLinkedListNode new_node
        new_node = CyDoubleLinkedListNode(val)

        if self.begin is None:
            self.begin = new_node
            self.end = new_node
        else:
            new_node.prev = self.end
            self.end.next = new_node
            self.end = new_node
            self.end.next = self.begin
            self.begin.prev = self.end

        self.list_len += 1
        return self

    def addleft(self, object val):
        cdef CyDoubleLinkedListNode new_node
        new_node = CyDoubleLinkedListNode(val)

        if self.begin is None:
            self.begin = new_node
            self.end = new_node
        else:
            new_node.next = self.begin
            self.begin.prev = new_node
            self.begin = new_node
            self.end.next = self.begin
            self.begin.prev = self.end

        self.list_len += 1
        return self
        
    def popright(self):
        if self.list_len <= 1:
            self.begin = None
            self.end = None
            self.list_len = 0
        else:
            self.end = self.end.prev
            self.end.next = self.begin
            self.begin.prev = self.end
            self.list_len -= 1

        return self

    def popleft(self):
        if self.list_len <= 1:
            self.begin = None
            self.end = None
            self.list_len = 0
        else:
            self.begin = self.begin.next
            self.end.next = self.begin
            self.begin.prev = self.end
            self.list_len -= 1

        return self

    @cython.nonecheck(False)
    def insert_after(self, int index, object val):
        cdef CyDoubleLinkedListNode new_node
        new_node = CyDoubleLinkedListNode(val)
        current = self.get_node(index)

        new_node.next = current.next
        current.next.prev = new_node
        new_node.prev = current
        current.next = new_node
        if new_node.next is self.begin:
            self.end = new_node

        self.list_len += 1
        return self
