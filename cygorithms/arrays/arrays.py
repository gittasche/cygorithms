from . import c_array
from typing import Any


class OneDArray:
    """
    One dimensional array class. Creates C-contigous
    array of python dtype with constant size.

    Parameters
    ----------
    dtype : python type
        data type of array elements
    """
    def __init__(self, dtype, *args, **kwargs) -> None:
        self.array = c_array.OneDArray(dtype, *args, **kwargs)

    @property
    def size(self) -> int:
        return self.array.size

    def __len__(self) -> int:
        return len(self.array)

    def __getitem__(self, index: int) -> Any:
        return self.array[index]

    def __setitem__(self, index: int, value: Any) -> None:
        self.array[index] = value

    def _to_str(self, num: int) -> str:
        self__str__ = "["
        self__str__ += ", ".join(str(self.array.__getitem__(i)) for i in range(num))
        self__str__ += "]"
        return self__str__

    def __str__(self) -> str:
        return self._to_str(len(self.array))

    def fill(self, value: Any) -> None:
        """
        Fill all array elements with value.

        Parameters
        ---------
        value : Any
            filler value of type same as array elements type
        """
        self.array.fill(value)


class DynamicOneDArray(OneDArray):
    """
    Dynamic one dimensional array. Creates C-contigous array
    of python dtype with automatically size expanding and shrinking.
    """
    def __init__(self, dtype, *args, **kwargs) -> None:
        self.array = c_array.DynamicOneDArray(dtype, *args, **kwargs)

    def __str__(self) -> str:
        return super()._to_str(self.array._last_pos_filled + 1)

    def append(self, value: Any) -> None:
        """
        Append element to end of array

        Parameters
        ----------
        value : Any
            value to append
        """
        self.array.append(value)

    def delete(self, index: int) -> None:
        """
        Delete element from array.
        Correctly this method will set a ``None`` value
        instead of deleted element to save C-contigousity of array.

        Parameters
        ----------
        index : int
            index of element to delete
        """
        self.array.delete(index)
