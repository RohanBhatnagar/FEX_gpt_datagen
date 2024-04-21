import random

from regex import F
import torch
import function as func
import argparse
from computational_tree import BinaryTree
import torch.nn as nn 
import numpy as np
import sympy as sp

x, y= sp.symbols('x y')  # Define symbols used in your functions

parser = argparse.ArgumentParser(description='NAS')

parser.add_argument('--tree', default='depth2', type=str)
parser.add_argument('--num', default=10, type=int)

args = parser.parse_args()

unary = func.unary_functions
binary = func.binary_functions
binary_functions_str_readable = func.binary_functions_str_readable
unary_functions_str = func.unary_functions_str
unary_functions_str_readable = func.unary_functions_str_readable
unary_functions_str_leaf = func.unary_functions_str_leaf
binary_functions_str = func.binary_functions_str

if args.tree == 'depth2':
    def basic_tree():
        tree = BinaryTree('', False)

        tree.insertLeft('', True)
        tree.leftChild.insertLeft('', False)
        tree.leftChild.leftChild.insertLeft('', True)
        tree.leftChild.leftChild.insertRight('', True)

        tree.insertRight('', True)
        tree.rightChild.insertLeft('', False)
        tree.rightChild.leftChild.insertLeft('', True)
        tree.rightChild.leftChild.insertRight('', True)
        return tree

elif args.tree == 'depth1':
    def basic_tree():

        tree = BinaryTree('', False)
        tree.insertLeft('', True)
        tree.insertRight('', True)

        return tree

elif args.tree == 'depth2_rml':
    def basic_tree():
        tree = BinaryTree('', False)

        tree.insertLeft('', True)
        tree.leftChild.insertLeft('', True)

        tree.insertRight('', True)
        tree.rightChild.insertLeft('', True)

        return tree

elif args.tree == 'depth2_rmu':
    print('**************************rmu**************************')
    def basic_tree():
        tree = BinaryTree('', False)

        tree.insertLeft('', True)
        tree.leftChild.insertLeft('', False)
        tree.leftChild.leftChild.insertLeft('', True)
        tree.leftChild.leftChild.insertRight('', True)

        tree.insertRight('', False)
        tree.rightChild.insertLeft('', True)
        tree.rightChild.insertRight('', True)

        return tree

elif args.tree == 'depth2_rmu2':
    print('**************************rmu2**************************')
    def basic_tree():
        tree = BinaryTree('', False)

        tree.insertLeft('', True)
        tree.leftChild.insertLeft('', False)
        tree.leftChild.leftChild.insertLeft('', True)
        tree.leftChild.leftChild.insertRight('', True)

        tree.insertRight('', True)
        # tree.rightChild.insertLeft('', True)
        # tree.rightChild.insertRight('', True)

        return tree

elif args.tree == 'depth3':
    def basic_tree():
        tree = BinaryTree('', False)

        tree.insertLeft('', True)
        tree.leftChild.insertLeft('', False)
        tree.leftChild.leftChild.insertLeft('', True)
        tree.leftChild.leftChild.leftChild.insertLeft('', False)
        tree.leftChild.leftChild.leftChild.leftChild.insertLeft('', True)
        tree.leftChild.leftChild.leftChild.leftChild.insertRight('', True)

        tree.leftChild.leftChild.insertRight('', True)
        tree.leftChild.leftChild.rightChild.insertLeft('', False)
        tree.leftChild.leftChild.rightChild.leftChild.insertLeft('', True)
        tree.leftChild.leftChild.rightChild.leftChild.insertRight('', True)

        tree.insertRight('', True)
        tree.rightChild.insertLeft('', False)
        tree.rightChild.leftChild.insertLeft('', True)
        tree.rightChild.leftChild.leftChild.insertLeft('', False)
        tree.rightChild.leftChild.leftChild.leftChild.insertLeft('', True)
        tree.rightChild.leftChild.leftChild.leftChild.insertRight('', True)

        tree.rightChild.leftChild.insertRight('', True)
        tree.rightChild.leftChild.rightChild.insertLeft('', False)
        tree.rightChild.leftChild.rightChild.leftChild.insertLeft('', True)
        tree.rightChild.leftChild.rightChild.leftChild.insertRight('', True)
        return tree

structure = []
leaves_index = []
leaves = 0
count = 0

def inorder_structure(tree):
    global structure, leaves, count, leaves_index
    if tree:
        inorder_structure(tree.leftChild)
        structure.append(tree.is_unary)
        if tree.leftChild is None and tree.rightChild is None:
            leaves = leaves + 1
            leaves_index.append(count)
        count = count + 1
        inorder_structure(tree.rightChild)

inorder_structure(basic_tree())
print('leaves index:', leaves_index)
print('tree structure:', structure, 'leaves num:', leaves)

structure_choice = []
for is_unary in structure:
    if is_unary == True:
        structure_choice.append(len(unary))
    else:
        structure_choice.append(len(binary))
print('tree structure choices', structure_choice)

def inorder(tree, actions):
    global count
    if tree:
        inorder(tree.leftChild, actions)
        action = actions[count].item()
        if tree.is_unary:
            action = action
            tree.key = unary[action]
            tree.action=action
            print(count, action, func.unary_functions_str[action])
        else:
            action = action
            tree.key = binary[action]
            tree.action = action
            print(count, action, func.binary_functions_str[action])
        count = count + 1
        inorder(tree.rightChild, actions)


def sp_function(tree):
    if tree is None: 
        return ""
    if tree.leftChild is None and tree.rightChild is None: 
        return tree.key

def print_fmla(tree):
    """
    Prettyprints fmla for a tree.

    Args:
    tree (BinaryTree): The root of the binary expression tree.

    Returns:
    list: A list of tokens in postfix order.
    """
    if tree is None:
        return ""
    if tree.leftChild is None and tree.rightChild is None:
        return func.unary_leaf_map[tree.key].format('x')
    elif tree.rightChild is None:
        left_postfix = print_fmla(tree.leftChild) 
        return func.function_map[tree.key].format('?',left_postfix,'?')
    else:
        left_postfix = print_fmla(tree.leftChild) 
        right_postfix = print_fmla(tree.rightChild) 
        return func.function_map[tree.key].format(left_postfix,right_postfix) #[tree.key.__name__ if hasattr(tree.key, '__name__') else str(tree.key)]

def get_function(actions):
    global count
    count = 0
    computation_tree = basic_tree()
    inorder(computation_tree, actions)
    count = 0
    return computation_tree

def generate_data(num_fns):
    # write to a file later 
    functions = []
    for i in range(num_fns):
        actions = []
        for j in range(0, len(structure_choice)):
            actions.append(torch.LongTensor([torch.randint(0,structure_choice[j],(1,1))]))
        computational_tree = get_function(actions)
        functions.append(computational_tree)
    for idx, fun in enumerate(functions):
        print("Function: ", idx)
        print(print_fmla(fun))

if __name__ == '__main__':
    generate_data(10)
    print("main")