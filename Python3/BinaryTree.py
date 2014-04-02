from Node import Node
from Exceptions import BoundaryViolation, InvalidPosition, NonEmptyTree

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
