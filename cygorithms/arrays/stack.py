from . import c_array


class Stack:
    def __init__(self, dtype, *args, **kwargs):
        self.stack = c_array.ArrayStack(dtype, *args, **kwargs)

    def is_empty(self):
        return self.stack.is_empty()

    def __len__(self):
        return len(self.stack)

    def push(self, item):
        self.stack.push(item)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack.peek()
