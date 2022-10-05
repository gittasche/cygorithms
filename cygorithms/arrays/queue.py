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
    """
    Contiguous memory queue class

    Parameters
    ----------
    dtype: python type
        type of data in queue
    size: int, optional
        size of queue, default ``len(data)`` if
        ``data`` is provided and ``0`` if its not
    data: sequence, optional
        sequence of elements of type ``dtype`` to input
        into queue, default empty list  
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
        self.queue = c_array.ArrayQueue(dtype, *args, **kwargs)

    def is_empty(self) -> bool:
        """
        Check if queue is empty

        Returns
        -------
        bool, True if empty else False
        """
        return self.queue.is_empty()

    def __len__(self) -> int:
        return len(self.queue)

    def push(self, item: Any) -> None:
        """
        Push ``item`` to the queue

        Parameters
        ----------
        item: any
            object of type ``dtype``
        """
        self.queue.push(item)

    def pop(self) -> Any:
        """
        Get first element if queue not empty
        and pop it from queue

        Returns
        -------
        Any, first element
        """
        return self.queue.pop()

    def peek(self) -> Any:
        """
        Get first element if queue not empty

        Returns
        -------
        Any, first element
        """
        return self.queue.peek()
