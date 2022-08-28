# from cygorithms.linked_list.cy_linked_list import CyLinkedList, CyCircularLinkedList
# from cygorithms.linked_list.linked_list import LinkedList as pyLL

from cygorithms.linked_list.linked_list import (
    SingleLinkedList,
    SingleCircularLinkedList,
    DoubleLinkedList,
    DoubleCircularLinkedList
)

if __name__ == "__main__":
    # l = pyLL()
    # l.add([1, 2, 3])
    # l.add([4, 5])
    # l.add([1, 2])
    # print(l)
    # l = CyLinkedList()
    # l.addright([1, 2, 3]).addright([1, 2]).addleft([0, 0])
    # l.insert_after(0, [0, 0])
    # l.popleft()
    # print(l)
    # cl = CyCircularLinkedList()
    # cl.addright([1, 2, 3]).addleft([4, 5]).addleft([1, 2])
    # print(cl.insert_after(0, [0, 0]))
    # l = SingleLinkedList()
    # l.addright([1, 2, 3]).addright([1, 2]).addright([1])
    # print(l.insert_after(2, [0, 0]).popleft())
    # cl = SingleCircularLinkedList()
    # cl.addright(1).addright(2).addright(3)
    # print(cl.insert_after(2, 4).insert_after(3, 5).popleft().end.data)
    dl = DoubleCircularLinkedList([1, 2, 3], [1, 2], [1])
    # dl.addright([1, 2, 3]).addright([1, 2]).addright([1])
    print(dl.insert_after(5, [0, 0]).insert_after(6, [1, 1]).popright())