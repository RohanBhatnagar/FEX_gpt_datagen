from computational_tree import BinaryTree
import function as func

unary = func.unary_functions
binary = func.binary_functions
unary_functions_str = func.unary_functions_str
unary_functions_str_leaf = func.unary_functions_str_leaf
binary_functions_str = func.binary_functions_str

tree = BinaryTree(binary[1], False)

tree.insertLeft(unary[5], True)
tree.leftChild.insertLeft(binary[2], False)
tree.leftChild.leftChild.insertLeft('', True)
tree.leftChild.leftChild.insertRight('', True)

tree.insertRight('', True)
tree.rightChild.insertLeft('', False)
tree.rightChild.leftChild.insertLeft('', True)
tree.rightChild.leftChild.insertRight('', True)
