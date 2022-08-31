from cygorithms.linked_list.linked_list import (
    SingleLinkedList,
    SingleCircularLinkedList,
    DoubleLinkedList,
    DoubleCircularLinkedList
)

from cygorithms.arrays import OneDArray
from cygorithms.arrays import DynamicOneDArray

def degree_cache(degree):
    nums = {}
    def degree_wrapper(num):
        if num in nums:
            return nums[num]
        else:
            num_degree = degree(num)
            nums[num] = num_degree
            return num_degree
    return degree_wrapper

@degree_cache
def degree(num):
    return num**2

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
    # l = DoubleLinkedList([1, 2, 3], [1, 2], [1])
    # dl.addright([1, 2, 3]).addright([1, 2]).addright([1])
    # print(l.insert_after(2, [0, 0]).insert_after(2, [1, 1]))
    arr = OneDArray(int, 4, [1, 2, 3, 4])