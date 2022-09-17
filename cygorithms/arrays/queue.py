from . import c_array
from typing import Any


class Queue:
    def __init__(self, dtype, *args, **kwargs) -> None:
        self.queue = c_array.ArrayQueue(dtype, *args, **kwargs)

    def is_empty(self) -> bool:
        return self.queue.is_empty()

    def __len__(self) -> int:
        return len(self.queue)

    def push(self, item: Any) -> None:
        self.queue.push(item)

    def pop(self) -> Any:
        return self.queue.pop()

    def peek(self) -> Any:
        return self.queue.peek()
