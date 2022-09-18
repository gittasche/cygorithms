from . import c_array
from typing import (
    Any,
    Type,
    Optional,
    List,
    Tuple
)


class Stack:
    def __init__(
        self,
        dtype: Type,
        size: Optional[int] = None,
        data: None | List[Any] | Tuple[Any] = None
    ) -> None:
        if size is None and data is None:
            args = (0, [])
        elif size is None:
            if not isinstance(data, (list, tuple)):
                raise TypeError(
                    "`data` must be an instance of list"
                    f" or tuple, got {type(data).__name__}."
                )
            args = (len(data), data)
        elif data is None:
            raise ValueError(
                "`data` must be passed as argument if"
                " `size` is not `None`."
            )
        else:
            if not isinstance(data, (list, tuple)):
                raise TypeError(
                    "`data` must be an instance of list"
                    f" or tuple, got {type(data).__name__}."
                )
            if size != len(data):
                raise ValueError(
                    "`size` must be equal `len(data)`,"
                    f" got `size` = {size}, len(data) = {len(data)}."
                )
            args = (size, data)
        kwargs = {}
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
