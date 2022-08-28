from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

from .cy_linked_list import (
    CyLinkedList,
    CyCircularLinkedList,
    CyDoubleLinkedList,
    CyDoubleCircularLinkedList
)

class BaseLinkedList(ABC):
    """
    ABC for Linked lists.
    """
    def __init__(self, list_type, args):
        self.list = list_type()
        for arg in args:
            self.list.addright(arg)

    def __len__(self) -> int:
        return self.list.__len__()

    def __str__(self) -> str:
        return self.list.__str__()

    @abstractmethod
    def _check_index(self, index):
        raise NotImplementedError()

    def __setitem__(self, index: int) -> None:
        index = self._check_index(index)
        self.list.__setitem__(index)

    def __getitem__(self, index: int) -> Any:
        index = self._check_index(index)
        return self.list.__getitem__(index)

    def addright(self, val: Any) -> BaseLinkedList:
        """
        add element ``val`` too the end of the list.

        Parameters
        ----------
        val : any
            python object to add

        Returns
        -------
        self : list itself
        """
        self.list.addright(val)
        return self

    def addleft(self, val) -> BaseLinkedList:
        """
        add element ``val`` too the begin of the list.

        Parameters
        ----------
        val : any
            python object to add

        Returns
        -------
        self : list itself
        """
        self.list.addleft(val)
        return self

    def popright(self) -> BaseLinkedList:
        """
        pop element from the end of the list.

        Returns
        -------
        self : list itself
        """
        self.list.popright()
        return self

    def popleft(self) -> BaseLinkedList:
        """
        pop element from the begin of the list.

        Returns
        -------
        self : list itself
        """
        self.list.popleft()
        return self

    def insert_after(self, index: int, val: Any) -> BaseLinkedList:
        """
        insert element ``val`` after ``index``-th element

        Parameters
        ----------
        index : int
            index after which ``val`` will be inserted
        val : any
            python object to insert

        Returns
        -------
        self : list itself
        """
        index = self._check_index(index)
        self.list.insert_after(index, val)
        return self

class SingleLinkedList(BaseLinkedList):
    """
    Single linked list of python objects:
    
    ``begin`` -> ... -> ``end``

    requires less memory then Double linked memory,
    but have slower indexing.

    Parameters
    ----------
    args : Any arguments
        python objects to insert with initialization
    """
    def __init__(self, *args):
        super().__init__(CyLinkedList, args)
    
    def _check_index(self, index):
        if (-len(self.list) <= index < 0):
            return index + len(self.list)
        elif (0 <= index < len(self.list)):
            return index
        else:
            raise IndexError(
                f"`index` must be in [0, {len(self.list)}),"
                f" got {index}."
            )

class SingleCircularLinkedList(BaseLinkedList):
    """
    Single circular linked list of python objects:

    ... -> ``begin`` -> ... -> ``end`` -> ``begin`` -> ...

    requires less memory then Double linked memory,
    but have slower indexing.

    Parameters
    ----------
    args : Any arguments
        python objects to insert with initialization
    """
    def __init__(self, *args):
        super().__init__(CyCircularLinkedList, args)

    def _check_index(self, index):
        if index < 0:
            return index - len(self.list) * (index // len(self.list))
        else:
            return index

class DoubleLinkedList(BaseLinkedList):
    """
    Double linked list of python objects:

    ``begin`` <-> ... <-> ``end``

    requires more memory than Single linked list,
    but have faster indexing.

    Parameters
    ----------
    args : Any arguments
        python objects to insert with initialization
    """
    def __init__(self, *args):
        super().__init__(CyDoubleLinkedList, args)

    def _check_index(self, index):
        if (-len(self.list) <= index < 0):
            return index + len(self.list)
        elif (0 <= index < len(self.list)):
            return index
        else:
            raise IndexError(
                f"`index` must be in [0, {len(self.list)}),"
                f" got {index}."
            )

class DoubleCircularLinkedList(BaseLinkedList):
    """
    Double circular linked list of python objects:

    ... <-> ``begin`` <-> ... <-> ``end`` <-> ``begin`` <-> ...

    requires more memory than Single linked list,
    but have faster indexing.

    Parameters
    ----------
    args : Any arguments
        python objects to insert with initialization
    """
    def __init__(self, *args):
        super().__init__(CyDoubleCircularLinkedList, args)
    
    def _check_index(self, index):
        if index < 0:
            return index - len(self.list) * (index // len(self.list))
        else:
            return index