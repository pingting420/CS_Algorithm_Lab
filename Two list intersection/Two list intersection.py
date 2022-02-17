class Node(object):
    def __init__(self, item):
        self.item = item
        self.next = None

class Singlelinkedlist:
    def __init__(self):
        self._head = None
    def length(self):
        cur = self._head
        count = 0
        while cur is not None:
            count += 1
            cur = cur.next
        return count
    def append(self, node:Node):
        if self._head is None:
            self._head = node
        else:
            cur = self._head
            while cur.next is not None:
                cur = cur.next
            cur.next = node
        return
    
    def show(self):
        cur = self._head
        while cur is not None:
            print(cur.item)
            cur = cur.next
        return
    
class Solution:
    def find_first_common_node(self, l1:Singlelinkedlist, l2:Singlelinkedlist) -> Node:
        len1 = l1.length()
        len2 = l2.length()
        offset = len1 - len2 if len1 >= len2 else len2 - len1
        
        cur1 = l1._head
        cur2 = l2._head
        while offset > 0:
            if len1 >= len2:
                cur1 = cur1.next
            else:
                cur2 = cur2.next
            offset -= 1
        while cur1 != cur2:
            cur1 = cur1.next
            cur2 = cur2.next
        return cur1

###create two list, which are 1,2,3,4,5,10,11,12', '6,7,8,10,11,12'.They share common element from node10.
def construct_demo_lists():
    l1 = Singlelinkedlist()
    l2 = Singlelinkedlist()
    for i in range(1, 6):
        node = Node(i)
        l1.append(node)
    for i in range(6, 9):
        node = Node(i)
        l2.append(node)
    l3 = Singlelinkedlist()
    for i in range(10,13):
        node = Node(i)
        l3.append(node)
    l1.append(l3._head)
    l2.append(l3._head)
    return l1, l2

if __name__ == '__main__':
    l1, l2 = construct_demo_lists()
    ##use method I created, to find first common element.
    print(Solution().find_first_common_node(l1, l2).item)