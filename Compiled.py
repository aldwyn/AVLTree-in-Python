class Node:
    def __init__(self, e, parent, left, right):
        self.e, self.parent, self.left, self.right = e, parent, left, right

class BoundaryViolation(Exception):
    pass

class InvalidPosition(Exception):
    pass

class NonEmptyTree(Exception):
    pass

class BinaryTree:
    def __init__(self):
        self.root, self.size = None, 0

    def root(self):
        return self.checkPosition(self.root)

    def setRoot(self, root):
        self.root = root

    def createNode(self, e, parent, left, right):
        return Node(e, parent, left, right)

    def hasLeft(self, pos):
        return pos.left is not None

    def hasRight(self, pos):
        return pos.right is not None

    def isInternal(self, pos):
        self.checkPosition(pos)
        return self.hasLeft(pos) or self.hasRight(pos)

    def isRoot(self, pos):
        self.checkPosition(pos)
        return pos is self.root

    def parentOf(self, pos):
        tmpParent = self.checkPosition(pos)
        if tmpParent.parent is None:
            raise BoundaryViolation('No parent')
        return tmpParent.parent

    def addRoot(self, e):
        if self.size is not 0:
            raise NonEmptyTree('Tree already has a root')
        self.size = 1
        self.root = self.createNode(e, None, None, None)
        return self.root

    def insertLeft(self, pos, e):
        tmpParent = self.checkPosition(pos)
        if tmpParent.left is not None:
            raise InvalidPosition('Node already has a left child')
        tmpLeft = self.createNode(e, tmpParent, None, None)
        tmpParent.left = tmpLeft
        self.size += 1
        return tmpLeft

    def insertRight(self, pos, e):
        tmpParent = self.checkPosition(pos)
        if tmpParent.right is not None:
            raise InvalidPosition('Node already has a right child')
        tmpRight = self.createNode(e, tmpParent, None, None)
        tmpParent.right = tmpRight
        self.size += 1
        return tmpRight

    def insertAtExternal(self, pos, left, right):
        if self.isInternal(pos):
            raise InvalidPosition('Node is not external')
        self.insertLeft(pos, left)
        self.insertRight(pos, right)

    def removeAboveExternal(self, pos):
        if self.isInternal(pos):
            raise InvalidPosition('Node is not external')
        if self.isRoot(pos):
            self.__remove(pos)
        else:
            tmpParent = self.parentOf(pos)
            self.__remove(pos)
            self.__remove(tmpParent)

    def replace(self, pos, e):
        tmpParent = self.checkPosition(pos)
        tmpE = tmpParent.e
        tmpParent.e = e
        return tmpE

    def sibling(self, pos):
        tmpParent = self.checkPosition(pos)
        if tmpParent.parent is not None:
            if tmpParent.parent.left is tmpParent:
                sibling = tmpParent.parent.right
            else:
                sibling = tmpParent.parent.left
            if sibling is not None:
                return sibling
        else:
            raise InvalidPosition('No sibling')

    def __remove(self, pos):
        tmpParent = self.checkPosition(pos)
        if tmpParent.left is not None and tmpParent.right is not None:
            raise InvalidPosition('Cannot remove node with children')
        if tmpParent.left is not None:
            onlyChild = tmpParent.left
        elif tmpParent.right is not None:
            onlyChild = tmpParent.right
        else:
            onlyChild = None
        if tmpParent is self.root:
            if onlyChild is not None:
                onlyChild.parent = None
        else:
            posParent = tmpParent.parent
            if tmpParent is posParent.left:
                posParent.left = onlyChild
            else:
                posParent.right = onlyChild
            if onlyChild is not None:
                onlyChild.parent = posParent
        self.size -= 1
        return pos.e

    def preorder(self, initial, positions):
        positions.append(initial)
        if initial.left is not None:
            self.preorder(initial.left, positions)
        if initial.right is not None:
            self.preorder(initial.right, positions)

    def inorder(self, initial, positions):
        if initial.left is not None:
            self.preorder(initial.left, positions)
        positions.append(initial)
        if initial.right is not None:
            self.preorder(initial.right, positions)

    def postorder(self, initial, positions):
        if initial.left is not None:
            self.preorder(initial.left, positions)
        if initial.right is not None:
            self.preorder(initial.right, positions)
        positions.append(initial)

    def checkPosition(self, pos):
        if (pos is not None):
            return pos
        else:
            raise InvalidPosition('Position is non-existent')

    def toArray(self, opt):
        positions = []
        if self.size is not 0:
            if opt is 'preorder':
                self.preorder(self.root, positions)
            elif opt is 'inorder':
                self.inorder(self.root, positions)
            elif opt is 'postorder':
                self.postorder(self.root, positions)
            else:
                raise InvalidInput('Invalid input')
        return positions

    def toList(self, opt):
        tmpArray = []
        for nodebit in self.toArray(opt):
            tmpArray.append(nodebit.e)
        return list(tmpArray)

    def prettyToArray(self, opt):
        tmpArray = []
        for nodebit in self.toArray(opt):
            if nodebit.e is not None:
                tmpArray.append(nodebit.e)
        return list(tmpArray)

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

class AVLNode(Node):
    def __init__(self, e, parent, left, right):
        super().__init__(e, parent, left, right)
        self.height = 0
        if left is not None:
            self.height = max(self.height, 1+left.height)
        elif right is not None:
            self.height = max(self.height, 1+right.height)

class AVLTree(BinarySearchTree):
    def __init__(self):
        super().__init__()

    def createNode(self, e, parent, left, right):
        return AVLNode(e, parent, left, right)

    def isBalanced(self, pos):
        bfactor = pos.left.height - pos.right.height
        return -1 <= bfactor and bfactor <= 1

    def addHeight(self, pos):
        pos.height = 1 + max(pos.left.height, pos.right.height)

    def insert(self, key):
        toReturn = super().insert(key)
        self.rebalance(super().lastTransact())
        return toReturn

    def remove(self, pos):
        toReturn = super().remove(pos)
        if toReturn is not None:
            self.rebalance(super().lastTransact())
        return toReturn

    def rebalance(self, pos):
        if super().isInternal(pos):
            self.addHeight(pos)
        while not super().isRoot(pos):
            pos = pos.parent
            self.addHeight(pos)
            if not self.isBalanced(pos):
                tmpPos = self.tallerChild(self.tallerChild(pos))
                pos = super().restructure(tmpPos)
                self.addHeight(pos.left)
                self.addHeight(pos.right)
                self.addHeight(pos)

    def tallerChild(self, pos):
        if pos.left.height > pos.right.height:
            return pos.left
        elif pos.left.height < pos.right.height:
            return pos.right
        if super().isRoot(pos):
            return pos.left
        if pos is pos.parent.left:
            return pos.left
        else:
            return pos.right

class Set:
    def __init__(self):
        self.tmpIntersection = []
        self.tmpDifference = []
        
    def union(self, setA, setB):
        powerSet = AVLTree()
        self.unionTraversal(setA.root, powerSet)
        self.unionTraversal(setB.root, powerSet)
        return powerSet.prettyToArray('preorder')

    def intersection(self, setA, setB):
        powerSet = AVLTree()
        self.unionTraversal(setA.root, powerSet)
        self.interTraversal(setB.root, powerSet)
        return self.tmpIntersection

    def difference(self, setA, setB):
        powerSet = AVLTree()
        self.unionTraversal(setB.root, powerSet)
        self.diffTraversal(setA.root, powerSet)
        return self.tmpDifference

    def isSubset(self, setA, setB):
        if setA.size < setB.size:
            return False
        else:
            powerSet = AVLTree()
            self.unionTraversal(setA.root, powerSet)
            return self.isSubsetTraversal(setB.root, powerSet)

    def unionTraversal(self, initial, powerSet):
        if initial.e is not None and powerSet.find(initial.e) is None:
            powerSet.insert(initial.e)
        if initial.left is not None:
            self.unionTraversal(initial.left, powerSet)
        if initial.right is not None:
            self.unionTraversal(initial.right, powerSet)

    def interTraversal(self, initial, powerSet):
        if initial.e is not None and powerSet.find(initial.e) is not None:
            self.tmpIntersection.append(initial.e)
        if initial.left is not None:
            self.interTraversal(initial.left, powerSet)
        if initial.right is not None:
            self.interTraversal(initial.right, powerSet)

    def diffTraversal(self, initial, powerSet):
        if initial.e is not None and powerSet.find(initial.e) is None:
            self.tmpDifference.append(initial.e)
        if initial.left is not None:
            self.diffTraversal(initial.left, powerSet)
        if initial.right is not None:
            self.diffTraversal(initial.right, powerSet)

    def isSubsetTraversal(self, initial, powerSet):
        if initial.e is not None and powerSet.find(initial.e) is None:
            return False
        if initial.left is not None:
            self.interTraversal(initial.left, powerSet)
        if initial.right is not None:
            self.interTraversal(initial.right, powerSet)
        return True

if __name__ == '__main__':
    avl1 = AVLTree()
    avl1.insertAll([1, 2, 3, 4, 5, 6, 7, 8, 9])
    print(avl1.prettyToArray('preorder'))

    avl2 = AVLTree()
    avl2.insertAll([13, 24, 3, 45, 5, 6, 76, 8, 9])
    print(avl2.prettyToArray('preorder'))

    aSet = Set()
    print(aSet.union(avl1, avl2))
    print(aSet.intersection(avl1, avl2))
    print(aSet.difference(avl1, avl2))
    print(aSet.isSubset(avl1, avl2))
