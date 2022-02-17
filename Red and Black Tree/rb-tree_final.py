'''
five feature for the RB tree:
1. the node is black or red
2. the root is black
3. every leaf( NIL) is black
4. every child node for the red node is black
5. all of the path from every node to the leaf node have the same number of black node
'''
class RBTree:
    class Node:
        def __init__(self, key=None,color='RED',left=None,right=None,p=None) -> None:
            self.key = key # five feature of the rb-tree
            self.color = color
            self.left = left
            self.right = right
            self.p = p
        
        def __str__(self): #inside function , will print the tree as the format you want
            return str({'key':self.key, 'color':self.color})
        
        def __repr__(self):
            return {'key':self.key, 'color':self.color}
    
    def __init__(self) -> None:
        self.NIL = None #NIL node, every child node and the subnode of the root, NIL.color = black
        self.root = None # the root of the tree
    
    def RBTree_Left_Rotate(self, x:Node):
        '''
            y           <--left                x
          x    c                            a     y
        a   b           -->right                b   c  #because y>x, a<x, b>x, c>y
        '''
        if x.right==self.NIL:  #if x.right=NIL(no y), return
            return
        y = x.right            #set y
        #operation as follow
        x.right = y.left       #set b to x.right, next step should set the x is the parent of b
        if y.left != self.NIL:    #turn y's left subtree into x's right subtree
            y.left.p = x      #make sure x is the parent of b
        ##replace x with y
        y.p = x.p                #link x's parent to y
        if x.p == self.NIL:       #if x is root, set y to root
            self.root = y
        elif x == x.p.left:       #if x is left node, then y is left node too
            x.p.left = y
        else:
            x.p.right = y        #if x is right node, then y is right node too
        # set y.lest = x
        y.left = x              #put x on y's left
        x.p = y                 #set x.parent of y
     
    def RBTree_Right_Rotate(self, x:Node):
        '''
            x           <--left                y
          y    c                            a     x
        a   b           -->right                b   c 
        '''
        if x.left==self.NIL:          #if no y, return
            return
        y = x.left                     #set y
        x.left = y.right
        if y.right != self.NIL:        #turn y's right subtree into x's left subtree
            y.right.p = x
        y.p = x.p                     #link x's parent to y
        if x.p == self.NIL:           #if x is root, set y to root
            self.root = y
        elif x == x.p.right:          #if x is right node, then y is right node too
            x.p.right = y
        else:                         #if x is left node, then y is left node too
            x.p.left = y
        y.right = x                   #put x on y's right
        x.p = y
    
    def __RBTree_Insert_Fixup(self, z:Node):                    
        while z != self.root and z.p.color == 'RED': #if the z.p.color is red, not increase the black height, but break the rule of the red node children all black.
            if z.p == z.p.p.left:                # if z.p is left node
                y = z.p.p.right                                 #y is z's uncle node(z.p.p.right)
                if y != self.NIL and y.color == 'RED':         #case 1: z, z.p, z.p.p.right are all red
                    z.p.color = 'BLACK'                        #set z.p, z.p.p.right be black
                    y.color = 'BLACK'
                    z.p.p.color = 'RED'
                    z = z.p.p
                else:                                   #case 2: z's uncle node is black and z is right node
                    if z == z.p.right:                  #if z is right node
                        z = z.p
                        self.RBTree_Left_Rotate(z)      
                    z.p.color = 'BLACK'               #case 3: z's uncle node is black and z is left node, set the z.p to black
                    z.p.p.color = 'RED'                
                    self.RBTree_Right_Rotate(z.p.p)
            ####if z.p is right node, repeat the code
            else:
                y = z.p.p.left                     #if z.p is right node
                if y and y.color == 'RED':
                    z.p.color = 'BLACK'
                    y.color = 'BLACK'
                    z.p.p.color = 'RED'
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self.RBTree_Right_Rotate(z)
                    z.p.color = 'BLACK'
                    z.p.p.color = 'RED'
                    self.RBTree_Left_Rotate(z.p.p)
        self.root.color='BLACK'

    def RBTree_Insert(self, z:Node) -> None: 
        #first to find the location for the new node as the binary tree feature
        y = self.NIL              #set y to NIL
        x = self.root             #set x to root
        while x != self.NIL:      #find z's position in terms of size, find until the leaf
            y = x
            if z.key < x.key: #z<x, insert into x.left
                x = x.left
            else:
                x = x.right
        z.p = y                  #z's parent is y
        ##### set the child of y is z
        if y == self.NIL:          #if y is NIL, z is root
            self.root = z
        elif z.key < y.key:        #if z.k<y.k, z is y's left child
            y.left = z
        else:                      #if z.k>=y.k, z is y's right child
            y.right = z
        ###
        z.left = self.NIL          #set y's child and color
        z.right = self.NIL        
        z.color = 'RED' #inorder to maintain the feature of rbtree, set the color as red
        self.__RBTree_Insert_Fixup(z)       #call __RBTree_INSERT_Fixup to restore properties

    def __RBTree_Transplant(self, u:Node, v:Node) -> None:
        if u.p == self.NIL:   # v is the node to replace u
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        if v != self.NIL:
            v.p = u.p      #set the parent 
    
    def __RBTree_Delete_Fixup(self, x:Node):
        while x != self.root and x.color == 'BLACK':    #when x = black need into the loop, and we don't know if x is the left or right    
            if x == x.p.left:        #x is the left child
                w = x.p.right
                if w.color == 'RED':
                    w.color = 'BLACK'                      #case 1: x's unlce node is red
                    x.p.color = 'RED'                
                    self.RBTree_Left_Rotate(x.p)
                    w = x.p.right
                if w.left.color == 'BLACK' and w.right.color == 'BLACK':    #case 2: x's unlce node is black and both childs are black
                    w.color = 'RED'
                    x = x.p
                elif w.right.color == 'BLACK':  #case 3: w is black and only right is black
                    w.left.color = 'BLACK'
                    w.color = 'RED'
                    self.RBTree_Right_Rotate(w)    
                    w = x.p.right
                w.color = x.p.color            #case 4: w is black and w.right is red
                x.p.color = 'BLACK'
                w.right.color = 'BLACK'
                self.RBTree_Left_Rotate(x.p)
                x = self.root
            else:
                w = x.p.left    #x is the right child
                if w.color == 'RED':
                    w.color = 'BLACK'
                    x.p.color = 'RED'
                    self.RBTree_Right_Rotate(x.p)
                    w = x.p.left
                if w.right.color == 'BLACK' and w.left.color == 'BLACK':
                    w.color = 'RED'
                    x = x.p
                elif w.left.color == 'BLACK':
                    w.right.color = 'BLACK'
                    w.color = 'RED'
                    self.RBTree_Left_Rotate(w)
                    w = x.p.left
                w.color = x.p.color
                x.p.color = 'BLACK'
                w.left.color = 'BLACK'
                self.RBTree_Right_Rotate(x.p)
                x = self.root
        x.color = 'BLACK'
    
    def RBTree_Delete(self, z:Node) -> None:
        ## y = z situation
        y = z
        y_original_color = y.color            
        if z.left == self.NIL:                        #if z.left=NIL, delete z, replace z with z.right
            x = z.right
            self.__RBTree_Transplant(z,z.right)       
        elif z.right == self.NIL:                     #if z.right=NIL, delete z, replace z with z.left
            x = z.left
            self.__RBTree_Transplant(z,z.left)
        # use y to replace z in below
        else:
            y = self.RBTree_Minimum(z.right)         #if z has left and right childs, y is successor node
            y_original_color = y.color
            x = y.right               
            
            if y.p == z and x != self.NIL:            #if y is z's right child
                x.p = y                     
            else:
                self.__RBTree_Transplant(y,y.right)     #if y is not z's right child, use y.right to replace y
                if z.right != self.NIL:                  #we replace y by its own right child x
                    y.right = z.right                    
                    y.right.p = y                      #set y to be r's parent
            self.__RBTree_Transplant(z,y)              #replace y and z
            #set the location of y
            y.left = z.left                           #use y.left to replace z.left
            y.left.p = y                       
            y.color = z.color
        # only when y = black need to fix the color
        ###y need to maintain the color of z, the original color of y already missed. so we need to fix the color of the y.right, because the y.left can maintain the feature.
        if y_original_color == 'BLACK':              #We only need to fix the situatiom when y is black, because the height of y is changed
            self.__RBTree_Delete_Fixup(x)              #fixup x's color 

    def RBTree_Minimum(self, x:Node) -> Node:      
        if x == self.NIL:
            x = self.root
        if x == None:
            return None
        while x.left != self.NIL:
            x = x.left
        return x
    
    def RBTree_Maximum(self, x:Node) -> Node:    #find the minimum of x  
        if x == self.NIL:
            x = self.root
        if x == None:
            return None
        while x.right != self.NIL:
            x = x.right
        return x

    def RBTree_Search(self, x:Node, k:object) -> Node: 
        while x != self.NIL and k != x.key:
            if k < x.key:
                x = x.left
            else:
                x = x.right
        return x
    
    def Inorder_Tree_Walk(self, x:Node):  #traversal 
        if x != self.NIL:
            self.Inorder_Tree_Walk(x.left)
            y = {}
            y['key'] = x.key
            y['color'] = x.color
            y['height'] = self.RBTree_Height(x)
            print(str(y))
            self.Inorder_Tree_Walk(x.right)
    
    def insert(self,k:object):
        self.RBTree_Insert(RBTree.Node(k))

    def delete(self,k:object):
        x = self.RBTree_Search(self.root, k)
        if x != None:
            self.RBTree_Delete(x)
    
    def RBTree_Successor(self,x): 
        if x.right != self.NIL: #x has right child
            return self.RBTree_Minimum(x.right)
        y = x.p
        while y != self.NIL and x == y.right: # the loop will stop when x = y.left, then can find the successor of x
            x = y 
            y = y.p
        return y
    
    def RBTree_Predecessor(self,x):
        if x.left != self.NIL:
            return self.RBTree_Maximum(x.left) #the opposite of successor
        y = x.p
        while y != self.NIL and x == y.left:
            x = y
            y = y.p
        return y
    
    def RBTree_Height(self,x):
        height = 0
        while x.left != self.NIL:
            x = x.left
            if x.color == 'BLACK':
                height += 1
        height += 1
        return height
    
    def sort(self): #like the inorder of traversal 
        if self.root!=None:
            print('ok')
            s = []
            res = []
            cur = self.root
            while cur != None or len(s) != 0:
                while cur != None:
                    s.append(cur)
                    cur = cur.left
                cur = s.pop()
                res.append(cur.key)
                cur = cur.right
            return res

    def min(self)-> object:
        x = self.RBTree_Minimum(self.root)
        if x == None:
            return None
        else:
            return x.key

    def max(self) -> object:
        x = self.RBTree_Maximum(self.root)
        if x == None:
            return None
        else:
            return x.key
            
def main():
    in_numbers = [5,7,19,60,58,36,24,12,6,97,48,99,33,44,55,54,32,
    24,17,16,45,63,132,549,222,111,197,179,64,138,158,346,246,721,1,
    25,37,39,47,102,101,678,36,97,83,78,46,147,129,203,206,227]
    rbtree = RBTree()
    for n in in_numbers:
        rbtree.insert(n)
    print('The new RB-Tree is:')
    rbtree.Inorder_Tree_Walk(rbtree.root)
    print('The black-height is:{}'.format(rbtree.RBTree_Height(rbtree.root)))
    '''
    interactive command: INSERT, SORT, SEARCH
    '''
    '''
    INSERT operation
    '''
    print('{}INSERT{}'.format('*-'*20,'*-'*20))
    rbtree.insert(15)
    print('After Insert {}, the RB-Tree becomes:'.format(15))
    rbtree.Inorder_Tree_Walk(rbtree.root)
    print('The black-height is:{}'.format(rbtree.RBTree_Height(rbtree.root)))
    '''
    SEARCH operation
    '''
    print('{}SEARCH{}'.format('*-'*20,'*-'*20))
    x = rbtree.RBTree_Search(rbtree.root, 60)
    print('If search 60, the result is:')
    print(x)
    print('The black-height is:{}'.format(rbtree.RBTree_Height(rbtree.root)))
    x = rbtree.RBTree_Search(rbtree.root, 210)
    print('If search 210, the result is:')
    print(x)
    print('The black-height is:{}'.format(rbtree.RBTree_Height(rbtree.root)))
    '''
    SORT operation
    '''
    print('{}SORT{}'.format('*-'*20,'*-'*20))
    x = rbtree.sort()
    if x!= None:
        print('The sorted numbers:', x)
    print('The black-height is:{}'.format(rbtree.RBTree_Height(rbtree.root)))
    '''
    SUCCESSOR operation
    '''
    print('{}SUCCESSOR{}'.format('*-'*20,'*-'*20))
    x = rbtree.RBTree_Search(rbtree.root,158)
    y = rbtree.RBTree_Successor(x)
    print('The Successor Node of 158 is:', y)
    print('The black-height is:{}'.format(rbtree.RBTree_Height(rbtree.root)))
    '''
    PREDECESSOR operation
    '''
    print('{}PREDECESSOR{}'.format('*-'*20,'*-'*20))
    x = rbtree.RBTree_Search(rbtree.root,158)
    y = rbtree.RBTree_Predecessor(x)
    print('The Predecessor Node of 158 is:', y)
    print('The black-height is:{}'.format(rbtree.RBTree_Height(rbtree.root)))
    '''
    MAX operation
    '''
    print('{}MAX{}'.format('*-'*20,'*-'*20))
    x=rbtree.max()
    print(x)
    print('The Max is:', x)
    print('The black-height is:{}'.format(rbtree.RBTree_Height(rbtree.root)))
    '''
    MIN operation
    '''
    print('{}MIN{}'.format('*-'*20,'*-'*20))
    x=rbtree.min()
    print(x)
    print('The Min is:', x)
    print('The black-height is:{}'.format(rbtree.RBTree_Height(rbtree.root)))
    '''
    DELETE operation
    '''
    print('{}DELETE{}'.format('*-'*20,'*-'*20))
    rbtree.delete(158)
    rbtree.Inorder_Tree_Walk(rbtree.root)
    print('The black-height is:{}'.format(rbtree.RBTree_Height(rbtree.root)))
    '''
    LEFT ROTATION operation
    '''
    print('{}LEFT-ROTATION{}'.format('*-'*20,'*-'*20))
    x = rbtree.RBTree_Search(rbtree.root,78)
    print(x)
    rbtree.RBTree_Left_Rotate(x)
    rbtree.Inorder_Tree_Walk(rbtree.root)
    print('The black-height is:{}'.format(rbtree.RBTree_Height(rbtree.root)))
    '''
    RIGHT ROTATION operation
    '''
    print('{}RIGHT-ROTATION{}'.format('*-'*20,'*-'*20))
    x = rbtree.RBTree_Search(rbtree.root,346)
    print(x)
    rbtree.RBTree_Right_Rotate(x)
    rbtree.Inorder_Tree_Walk(rbtree.root)
    print('The black-height is:{}'.format(rbtree.RBTree_Height(rbtree.root)))

    print('{}THANK YOU{}'.format('*-'*20,'*-'*20))

if __name__ == '__main__':
    main()


