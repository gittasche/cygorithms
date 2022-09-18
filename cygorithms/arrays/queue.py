from . import c_array
from typing import (
    Any,
    Type,
    Optional,
    Union,
    List,
    Tuple
)


class Queue:
    def __init__(
        self,
        dtype: Type,
        size: Optional[int] = None,
        data: Optional[Union[List[Any], Tuple[Any]]] = None
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
