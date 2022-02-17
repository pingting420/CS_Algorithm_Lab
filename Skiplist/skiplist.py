from random import randint

class Node:  
    def __init__(self, height = 0, elem = None):
        self.elem = elem
        self.next = [None]*height
    
    def __repr__(self) -> str:
        return str(self.elem)

class SkipList:

    def __init__(self):
        self.head = Node()
        self.len = 0
        self.maxHeight = 0

    def __len__(self):
        return self.len

    #Lookup*********************** 
    def find(self, elem, update = None): 
        if update == None: #The situation that you know the update and know the value small than the elem which want to find
            update = self.updateList(elem)
        if len(update) > 0: # This list has element 
            item = update[0].next[0]      #use lowest level to check if exists
            if item != None and item.elem == elem:
                return item
        return None
    
    def contains(self, elem, update = None):
        return self.find(elem, update) != None

    def randomHeight(self):  #random function returns the height of inserted elem
        height = 1

        while randint(1, 2) != 1:
            height += 1
        
        if height>5: #set the maximum height of 5
            return 5
        else:
            return height

    def updateList(self, elem):       #The function will return the number which small than the insert value              
        '''
        find the largest node whose key less than elem
        '''
        update = [None]*self.maxHeight
        x = self.head
        for i in reversed(range(self.maxHeight)): #maxheight is the height of the skiplist
            while x.next[i] != None and x.next[i].elem < elem: #to find the value for every level
                x = x.next[i]
            update[i] = x
        return update
        
    #Insert ************************
    def insert(self, elem): #set the height randomly, to call the updatelist, find the elem smaller than elem for each level, and then insert

        _node = Node(self.randomHeight(), elem) #call the randomHeight function and return the level need to be created

        self.maxHeight = max(self.maxHeight, len(_node.next))  #set max height
        while len(self.head.next) < len(_node.next):     #increase len(head.next) to maxheight
            self.head.next.append(None)

        update = self.updateList(elem)            #find the largest node whose key less than elem, for the every level    
        if self.find(elem, update) == None:
            for i in range(len(_node.next)):   #call the insert for every level
                _node.next[i] = update[i].next[i]
                update[i].next[i] = _node
            self.len += 1  #the number of list

    #Remove******************************
    def remove(self, elem):
        update = self.updateList(elem) #find the location of element less than elem want to remove for every level, and than delete.
        x = self.find(elem, update)
        if x != None:                  #If has, to implement the delete for the link for every level
            for i in reversed(range(len(x.next))):
                update[i].next[i] = x.next[i]
                if self.head.next[i] == None: #IF there is not any head, then decrease the height.
                    self.maxHeight -= 1
            self.len -= 1            
                
    def printList(self): #Print the list
        for i in range(len(self.head.next)-1, -1, -1): 
            x = self.head
            while x.next[i] != None:
                print(x.next[i].elem, end=' ')
                x = x.next[i]
            print()


def main():
    L = SkipList()
    commands = ['INSERT 20', 'INSERT 40', 'INSERT 10', 'INSERT 20', 'INSERT 5',
    'INSERT 80', 'DELETE 20', 'INSERT 100', 'INSERT 20', 'INSERT 30', 'DELETE 5',
    'INSERT 50', 'LOOKUP 80']

    for c in commands:
        args = c.upper().split()
        command = args[0]
        param = int(args[1])
        if command=='INSERT':
            L.insert(param)
            print('{}{} {}{}'.format('*-'*20,command,param,'*-'*20))
            L.printList()
        if command=='DELETE':
            L.remove(param)
            print('{}{} {}{}'.format('*-'*20,command,param,'*-'*20))
            L.printList()
        if command=='LOOKUP':
            x = L.find(param)
            print('{}{} {}{}'.format('*-'*20,command,param,'*-'*20))
            print(x)
    print('{}THANK YOU{}'.format('*-'*20,'*-'*20))  

if __name__ == '__main__':
    main()
