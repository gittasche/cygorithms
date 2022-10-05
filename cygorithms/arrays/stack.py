from . import c_array
from typing import (
    Any,
    Type,
    Optional,
    Union,
    List,
    Tuple
)


class Stack:
    """
    Contiguous memory stack class

    Parameters
    ----------
    dtype: python type
        type of data in stack
    size: int, optional
        size of stack, default ``len(data)`` if
        ``data`` is provided and ``0`` if its not
    data: sequence, optional
        sequence of elements of type ``dtype`` to input
        into stack, default empty list
    """
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
        self.stack = c_array.ArrayStack(dtype, *args, **kwargs)

    def is_empty(self) -> bool:
        """
        Check if stack is empty

        Returns
        -------
        bool, True if empty else False
        """
        return self.stack.is_empty()

    def __len__(self) -> int:
        return len(self.stack)

    def push(self, item: Any) -> None:
        """
        Push ``item`` to the stack

        Parameters
        ----------
        item: any
            object of type ``dtype``
        """
        self.stack.push(item)

    def pop(self) -> Any:
        """
        Get top element if stack not empty
        and pop it from stack

        Returns
        -------
        Any, top element
        """
        return self.stack.pop()

    def peek(self) -> Any:
        """
        Get top element if stack not empty

        Returns
        -------
        Any, top element
        """
        return self.stack.peek()
