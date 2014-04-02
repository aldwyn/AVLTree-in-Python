from AVLTree import AVLTree

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
