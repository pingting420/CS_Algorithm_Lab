'''

'''


class BinomialHeapNode:
    def __init__(self, key=None, degree=None, p=None, child=None, sibling=None) -> None:
        self.key = key
        self.degree = degree
        self.p = p
        self.child = child
        self.sibling = sibling

    def __str__(self)->str:
        return str(self.key)
    
    def __repr__(self):
        return self.key

class BinomialHeap:
    def __init__(self) -> None:
        self.head = None
    
    def BINOMIAL_HEAP_MINIMUM(self):
        y = None
        x = self.head
        min = float('Inf')
        while x != None:
            if x.key < min:
                min = x.key
                y = x
            x = x.sibling
        return y
    
    def BINOMIAL_LINK(y:BinomialHeapNode,z:BinomialHeapNode):
        y.p = z
        y.sibling = z.child
        z.child = y
        z.degree += 1
    
    def BINOMIAL_HEAP_UNION(H1, H2):
        H = BinomialHeap()
        H.head = BinomialHeap.BINOMIAL_HEAP_MERGE(H1,H2)
        del H1, H2
        if H.head == None:
            return H
        prev_x = None
        x = H.head
        next_x = x.sibling
        while next_x != None:
            if (x.degree != next_x.degree) or (next_x.sibling!=None and next_x.sibling.degree == x.degree):
                prev_x = x
                x = next_x
            else:
                if x.key <= next_x.key:
                    x.sibling = next_x.sibling
                    BinomialHeap.BINOMIAL_LINK(next_x, x)
                else:
                    if prev_x == None:
                        H.head = next_x
                    else:
                        prev_x.sibling = next_x
                    BinomialHeap.BINOMIAL_LINK(x, next_x)
                    x = next_x
            next_x = x.sibling
        return H

    def BINOMIAL_HEAP_MERGE(H1,H2):
        x1 = H1.head
        x2 = H2.head
        if x1 == None:
            return H2.head
        if x2 == None:
            return H1.head
        y = BinomialHeapNode()
        mark = y
        while x1 != None and x2 != None:
            if x2.degree < x1.degree:
                y.sibling = x2
                x2 = x2.sibling
            else:
                y.sibling = x1
                x1 = x1.sibling
            y = y.sibling
        while x1 != None:
            y.sibling = x1
            x1 = x1.sibling
            y = y.sibling
        while x2 != None:
            y.sibling = x2
            x2 = x2.sibling
            y = y.sibling
        return mark.sibling

    def BINOMIAL_HEAP_INSERT(self, x:BinomialHeapNode):
        H1 = BinomialHeap()
        x.p = None
        x.child = None
        x.sibling = None
        x.degree = 0
        H1.head = x
        self.head = BinomialHeap.BINOMIAL_HEAP_UNION(self, H1).head

    
    def BINOMIAL_HEAP_EXTRACT_MIN(self):
        p = self.head
        x = None
        x_prev = None
        p_prev = None
        if p is None:
            return p
        x = p
        w = p.key
        p_prev = p
        p = p.sibling
        while p != None:
            if p.key < w:
                x_prev = p_prev
                x = p
                w = p.key
            p_prev = p
            p = p.sibling
        if x == self.head:
            self.head = x.sibling
        elif x.sibling == None:
            x_prev.sibling = None
        else:
            x_prev.sibling = x.sibling
        child_x = x.child
        if child_x != None:
            H1 = BinomialHeap()
            child_x.p = None
            H1.head = child_x
            p = child_x.sibling
            child_x.sibling = None
            while p != None:
                p_prev = p
                p = p.sibling
                p_prev.sibling = H1.head
                H1.head = p_prev
                p_prev.p = None
            self.head = BinomialHeap.BINOMIAL_HEAP_UNION(self,H1).head

    def BINOMIAL_HEAP_DECREASE_KEY(self, x:BinomialHeapNode, key):
        if key > x.key:
            raise ValueError('new key is greater than current key')
        x.key = key
        y = x
        p = x.p
        while p!=None and y.key < p.key:
            y.key = p.key
            p.key = key
            y = p
            p = y.p
    
    def BINOMIAL_HEAP_DELETE(self, x:BinomialHeapNode):
        self.BINOMIAL_HEAP_DECREASE_KEY(x, -2147483648)
        self.BINOMIAL_HEAP_EXTRACT_MIN()
    


def test():
    print('BinomialHeapNode and BinomialHeap Test')

    print('MAKE_HEAP')
    H = BinomialHeap()
    print(H.head)

    print('INSERT')
    node1 = BinomialHeapNode(key = 1)
    node2 = BinomialHeapNode(key = 2)
    node3 = BinomialHeapNode(key = 3)
    H.BINOMIAL_HEAP_INSERT(node1)
    H.BINOMIAL_HEAP_INSERT(node2)
    H.BINOMIAL_HEAP_INSERT(node3)
    print(H.head)

    print('MINIMUM')
    print(H.BINOMIAL_HEAP_MINIMUM())

    print('EXTRACT_MIN')
    H.BINOMIAL_HEAP_EXTRACT_MIN()
    print(H.head)

    print('UNION')
    H1 = BinomialHeap()
    node1 = BinomialHeapNode(key = 4)
    node2 = BinomialHeapNode(key = 5)
    node3 = BinomialHeapNode(key = 6)
    H1.BINOMIAL_HEAP_INSERT(node1)
    H1.BINOMIAL_HEAP_INSERT(node2)
    H1.BINOMIAL_HEAP_INSERT(node3)
    H2 = BinomialHeap.BINOMIAL_HEAP_UNION(H,H1)
    print(H2.head)

    print('DECREASEKEY')
    H2.BINOMIAL_HEAP_DECREASE_KEY(node3, 0)
    print(H2.head)

    print('DELETE')
    H2.BINOMIAL_HEAP_DELETE(node3)
    print(H2.head)




if __name__ == '__main__':
    test()
else:
    pass