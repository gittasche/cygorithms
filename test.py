from cygorithms.linked_list.linked_list import (
    SingleLinkedList,
    SingleCircularLinkedList,
    DoubleLinkedList,
    DoubleCircularLinkedList
)

from cygorithms.arrays import Stack
# from cygorithms.arrays.c_array import ArrayStack
# from cygorithms.trees.cy_trees import BinarySearchTree, BinaryTreeTraversal

from cygorithms.trees import BinarySearchTree, BinaryTreeTraversal

from cygorithms.arrays import OneDArray, DynamicOneDArray
from cygorithms.arrays import selection_sort, merge_sort

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
    # arr = OneDArray(int, 3, [1, 2, 3])
    # arr[1] = 0
    # print(arr)
    # l1 = {"a": 1}
    # l2 = {"b": 2}
    # l3 = {"c": 3}
    # arr = OneDArray(dict, 3, [l1, l2, l3])
    # l0 = {"d": 0}
    # arr[1] = l0
    # print(arr)
    # arr = DynamicOneDArray(int, 1, [1])
    # arr.delete(0)
    # print(arr)
    # arr = DynamicOneDArray(int, 5, [3, 2, 4, 5, 1])
    # print(arr)
    # st = Stack(int, [1, 2, 3])
    # st.push(4)
    # print(st.pop())
    # print(st.pop())
    # print(st.pop())
    # print(st.pop())
    # print(st.is_empty())
    # st = Stack(int, 0, [])
    # print(st.is_empty())
    bst = BinarySearchTree()
    bst.insert(2)
    bst.insert(4)
    bst.insert(3)
    bst.insert(5)
    bst.insert(0)
    bst.insert(1)
    bst.insert(-1)
    
    btt = BinaryTreeTraversal(bst)
    print(btt.depth_first_search(order="post_order"))
    # bt.insert(2)
    # bt.insert(-1)
    # bt.insert(3)
    # bt.insert(0)
    # # bt.delete(2)
    # btt = BinaryTreeTraversal(bt)
    # print(btt.depth_first_search(order="post_order"))