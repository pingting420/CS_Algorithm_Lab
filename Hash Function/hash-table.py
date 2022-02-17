class Doublelinkedlist: # use slot to sovle the hash collision,
    class Node:
        def __init__(self, key=None,value=1) -> None:
            self.key = key
            self.value = value
            self.prev = None
            self.next = None
        
        def __str__(self) -> str:
            return str((self.key,self.value))

    def __init__(self) -> None:
        self.NIL = self.Node()
        self.NIL.prev = self.NIL
        self.NIL.next = self.NIL
    
    def __len__(self) -> int:
        x = self.NIL.next
        len = 0
        while x != self.NIL:
            x = x.next
            len += 1
        return len

    def search(self, k) -> Node:
        x = self.NIL.next
        while x!= self.NIL and x.key != k:
            x = x.next
        if x == self.NIL:
            return None
        else:
            return x
    
    def NodeInsert(self, x: Node) -> None:
        x.next = self.NIL.next
        self.NIL.next.prev = x
        self.NIL.next = x
        x.prev = self.NIL
    
    def insert(self, k): 
        x = self.search(k)
        if x== None:
            self.NodeInsert(Doublelinkedlist.Node(key=k,value=1))
        else:
            x.value += 1

    def NodeDelete(self, x: Node) -> None:
        x.prev.next = x.next
        x.next.prev = x.prev

    def remove(self, k)-> None:
        x = self.search(k)
        if x != None:
            x.value -= 1
            if x.value == 0:
                self.NodeDelete(x)

    def __str__(self):
        x = self.NIL.next
        y = []
        while x != self.NIL:
            y.append(str(x))
            x = x.next
        return str(y)

class HashTable:
    def __init__(self, slots=3) -> None: #define the slots number of 701, can slove the situation two words has same hash value
        self.slots = slots
        self.table = [None] * slots
    
    def hash(self,k): #This is hash function
        key = k[:5]
        key = key[::-1] #use the first 5 character to compute a value 
        base=1
        h = 0
        for i in key:
            h += (ord(i) - ord('a')+1)*base 
            base *= 47 #use the 47 rule 
        return abs(h % self.slots) #use the value to calculate the model of the value, will solve the hash collision
    
    def insert(self, key, value): #Insert
        h = self.hash(key)
        x = self.table[h]
        if x == None:
            self.table[h] = Doublelinkedlist()
        y = self.table[h].search(key)
        if y == None:
            self.table[h].NodeInsert(Doublelinkedlist.Node(key,value))
        else:
            y.value += value
    
    def list_all_keys(self):
        for x in self.table:
            if x != None and len(x) != 0:
                print(str(x))

    def find(self, key): #find
        h = self.hash(key)
        x = self.table[h]
        if x==None:
            return None
        else:
            return x.search(key)
    
    def increase(self, key): #Increase
        h = self.hash(key)
        x = self.table[h]
        if x == None:
            self.table[h] = Doublelinkedlist()
        self.table[h].insert(key)
    
    def delete(self, key): #delete
        h = self.hash(key)
        x = self.table[h]
        if x!=None:
            y = self.table[h].search(key)
            self.table[h].NodeDelete(y)

def main():
    with open('hashsamples.txt', 'r') as f:
        text = f.read()
    
    outtab = ' '*18
    trantab = str.maketrans('\'\"-[*#]:,!.?;_()@/',outtab)
    text = text.translate(trantab)
    words = []    
    for word in text.lower().split():
        if word.isalpha():
            words.append(word)

    H = HashTable()
    for w in words:
        H.insert(w,1)
    #H.insert('Pingting',2)
    #H.list_all_keys()
    #x = H.find('Pingting')
    #print(x)
    #H.increase('Pingting')
    #x = H.find('Pingting')
    #print(x)
    #H.delete('Pingting') 
    #x = H.find('Pingting')
    #print(x)
    H.list_all_keys() #print


if __name__ == '__main__':
    main()



