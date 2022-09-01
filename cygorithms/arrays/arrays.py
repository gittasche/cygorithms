from . import c_array
from typing import Any

class OneDArray:
    def __init__(self, dtype, *args, **kwargs):
        self.array = c_array.OneDArray(dtype, *args, **kwargs)

    @property
    def size(self):
        return self.array.size

    def __len__(self):
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
        self.array.fill(value)

class DynamicOneDArray(OneDArray):
    def __init__(self, dtype, *args, **kwargs):
        self.array = c_array.DynamicOneDArray(dtype, *args, **kwargs)

    def __str__(self):
        return super()._to_str(self.array._last_pos_filled + 1)

    def append(self, value: Any) -> None:
        self.array.append(value)

    def delete(self, index: int) -> None:
        self.array.delete(index)
