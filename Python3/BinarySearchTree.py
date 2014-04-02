from Node import Node
from BinaryTree import BinaryTree
from Exceptions import BoundaryViolation

class BinarySearchTree(BinaryTree):
    def __init__(self):
        super().__init__()
        super().addRoot(None)
        self.lastTransact = None

    def lastTransact(self):
        return self.lastTransact

    def left(self, pos):
        tmpParent = super().checkPosition(pos)
        if tmpParent.left is None:
            raise BoundaryViolation('No left child')
        return tmpParent.left

    def right(self, pos):
        tmpParent = super().checkPosition(pos)
        if tmpParent.right is None:
            raise BoundaryViolation('No right child')
        return tmpParent.right

    def treeSearch(self, key, pos):
        if not super().isInternal(pos):
            return pos
        else:
            if key < pos.e:
                return self.treeSearch(key, self.left(pos))
            elif key > pos.e:
                return self.treeSearch(key, self.right(pos))
            return pos

    def insertAtExternal(self, pos, e):
        super().insertAtExternal(pos, None, None)
        super().replace(pos, e)
        return e
        
    def insert(self, key):
        super().checkPosition(key)
        toInsert = self.treeSearch(key, super().root())
        while super().isInternal(toInsert):
            toInsert = self.treeSearch(key, self.left(toInsert))
        self.lastTransact = toInsert
        return self.insertAtExternal(toInsert, key)

    def insertAll(self, keylist):
        for keybit in keylist:
            if keybit is not None:
                self.insert(keybit)

    def remove(self, pos):
        super().checkPosition(pos)
        if not super().isInternal(self.left(pos)):
            toRemove = self.left(pos)
        elif not super().isInternal(self.right(pos)):
            toRemove = self.right(pos)
        else:
            toSwap = pos
            toRemove = self.right(toSwap)
            while super().isInternal(toRemove):
                toRemove = self.left(toRemove)
            super().replace(toSwap, super().parentOf(toRemove).e)
        self.lastTransact = super().sibling(toRemove)
        super().removeAboveExternal(toRemove)
        return toRemove

    def find(self, key):
        currPos = self.treeSearch(key, super().root())
        self.lastTransact = currPos
        if super().isInternal(currPos):
            return currPos
        return None

    def restructure(self, x):
        y = super().checkPosition(x.parent)
        z = super().checkPosition(y.parent)
        xLeft, yLeft =  x is y.left, y is z.left
        xx, yy, zz = x, y, z
        if xLeft and yLeft:
            a, b, c = xx, yy, zz
            t1, t2, t3, t4 = a.left, a.right, b.right, c.right
        elif not xLeft and yLeft:
            a, b, c = yy, xx, zz
            t1, t2, t3, t4 = a.left, b.left, b.right, c.right
        elif xLeft and not yLeft:
            a, b, c = zz, xx, yy
            t1, t2, t3, t4 = a.left, b.left, b.right, c.right
        else:
            a, b, c = zz, yy, xx
            t1, t2, t3, t4 = a.left, b.left, c.left, c.right
        if super().isRoot(z):
            super().setRoot(b)
            b.parent = None
        else:
            zParent = z.parent
            b.parent = zParent
            if z is zParent.left:
                zParent.left = b
            else:
                zParent.right = b
        b.left, a.parent = a, b
        b.right, c.parent = c, b
        a.left, t1.parent = t1, a
        a.right, t2.parent = t2, a
        c.left, t3.parent = t3, c
        c.right, t4.parent = t4, c
        return b
