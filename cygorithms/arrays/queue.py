from . import c_array


class Queue:
    def __init__(self, dtype, *args, **kwargs):
        self.queue = c_array.ArrayQueue(dtype, *args, **kwargs)

    def is_empty(self):
        return self.queue.is_empty()

    def __len__(self):
        return len(self.queue)

    def push(self, item):
        self.queue.push(item)

    def pop(self):
        return self.queue.pop()

    def peek(self):
        return self.queue.peek()
