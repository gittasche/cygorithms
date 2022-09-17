from . import c_array
from typing import Any


class Stack:
    def __init__(self, dtype, *args, **kwargs) -> None:
        self.stack = c_array.ArrayStack(dtype, *args, **kwargs)

    def is_empty(self) -> bool:
        return self.stack.is_empty()

    def __len__(self) -> int:
        return len(self.stack)

    def push(self, item: Any) -> None:
        self.stack.push(item)

    def pop(self) -> Any:
        return self.stack.pop()

    def peek(self) -> Any:
        return self.stack.peek()
