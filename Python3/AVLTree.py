from Node import Node
from BinarySearchTree import BinarySearchTree
from Exceptions import BoundaryViolation

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
