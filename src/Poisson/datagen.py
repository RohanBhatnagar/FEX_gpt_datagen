import random
import json
import torch
import function as func
import argparse
from computational_tree import BinaryTree
import torch.nn as nn
import numpy as np
import sympy as sp
from utils.logger import Logger
import utils.parser

x, y = sp.symbols('x y')  # Define symbols used in your functions

parser = argparse.ArgumentParser(description='NAS')

parser.add_argument('--tree', default='depth3', type=str)
parser.add_argument('--num', default=100, type=int)

args = parser.parse_args()

unary = func.unary_functions
binary = func.binary_functions
unary_functions_str = func.unary_functions_str
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
            tree.action = action
        else:
            action = action
            tree.key = binary[action]
            tree.action = action
        count = count + 1
        inorder(tree.rightChild, actions)

# forms final syms function from a computational tree
def sp_function(tree):
    if tree is None:
        return None
    elif tree.rightChild is None and tree.leftChild is None:
        return tree.key(x, 2)
    elif tree.rightChild is None: 
        return tree.key(sp_function(tree.leftChild), 2) #random number for 5
    else: 
        return tree.key(sp_function(tree.leftChild), sp_function(tree.rightChild)) #random number for 5

# prints a computational binary tree
def print_fmla(tree):
    if tree is None:
        return ""
    if tree.leftChild is None and tree.rightChild is None:
        return func.unary_functions_str[tree.action].format('2','x')
    elif tree.rightChild is None:
        left_postfix = print_fmla(tree.leftChild) 
        return func.unary_functions_str[tree.action].format('2',left_postfix)
    else:
        left_postfix = print_fmla(tree.leftChild) 
        right_postfix = print_fmla(tree.rightChild) 
        return func.binary_functions_str[tree.action].format(left_postfix,right_postfix) #[tree.key.__name__ if hasattr(tree.key, '__name__') else str(tree.key)]

def get_function(actions):
    global count
    count = 0
    computation_tree = basic_tree()
    inorder(computation_tree, actions)
    count = 0
    return computation_tree
 
def negative_laplacian(f):
    f_xx = sp.diff(f, x, x)
    neg_laplace = f_xx # adjust as per symbols, may have several variables 
    return -1 * neg_laplace

def generate_data(num_fns):
    Parser = utils.parser.Parser()
    functions = []
    for i in range(num_fns):
        actions = []
        for j in range(0, len(structure_choice)):
            actions.append(torch.LongTensor([torch.randint(0, structure_choice[j], (1, 1))]))
        computational_tree = get_function(actions)
        functions.append((computational_tree))
    
    data = []
    seen_entries = set()
    for idx, fun in enumerate(functions):
        f = sp_function(fun)
        neg_lap_f = negative_laplacian(f)
        soln_operators = Parser.get_postfix_from_str(str(f))
        f_operators = Parser.get_postfix_from_str(str(neg_lap_f))
        print(f, neg_lap_f)
        entry = {"F_Operators": f_operators, "Solution_Operators": soln_operators}
        entry_tuple = (tuple(f_operators), tuple(soln_operators))  # Convert to tuple for hashing
        if entry_tuple not in seen_entries:
            seen_entries.add(entry_tuple)
            data.append(entry)
    
    with open('dataset.jsonl', 'w') as outfile:
        for entry in data:
            json.dump(entry, outfile)
            outfile.write('\n')

if __name__ == '__main__':
    generate_data(args.num)
    print("main")
