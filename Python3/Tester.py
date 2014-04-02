from BinarySearchTree import BinarySearchTree
from AVLTree import AVLTree
from Set import Set

#bst = BinarySearchTree()
#bst.insertAll(toInsert)
#print(bst.toString('preorder'))

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
