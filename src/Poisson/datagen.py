import torch
from function import Functions
import argparse
from computational_tree import BinaryTree
import numpy as np
import sympy as sp
from utils.logger import Logger
import utils.parser

parser = argparse.ArgumentParser(description='NAS')

parser.add_argument('--tree', default='depth3', type=str)
parser.add_argument('--num', default=5, type=int)
parser.add_argument('--dim', default=2, type=int)
parser.add_argument('--bc', default='Dirichlet', type=str)
parser.add_argument('--function', default='Poisson', type=str)
# domain is assumed to be a [0,1] square, cube, etc. 
boundary = [0, 1]

args = parser.parse_args()

func = Functions(args.dim)

unary = func.get_unary_functions()
binary = func.get_binary_functions()
symbols = func.get_symbols()

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
            # print('adding', unary[action])
            tree.action = action
        else:
            action = action
            tree.key = binary[action]
            # print('adding', binary[action])
            tree.action = action
        count = count + 1
        inorder(tree.rightChild, actions)

# forms final syms function from a computational tree
def sp_function(tree):
    if tree is None:
        return None
    elif tree.rightChild is None and tree.leftChild is None:
        return tree.key(tree.key.args[0][0], 2)
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
    laplacian = sum(sp.diff(f, var, var) for var in symbols)
    return -1 * laplacian

def calculate_dirichlet(f):
    E = sp.symbols('E')
    bc = {}
    # boundary defined above
    for symbol in symbols:
        for bound in boundary:
            subs = {sym: bound if sym == symbol else sp.Symbol(sym.name) for sym in symbols}
            f = f.subs(E, 1)
            bc[f'{symbol}={bound}'] = simplify_constants(f.subs(subs))
    return bc

def calculate_neumann(f):
    bc = {}
    for symbol in symbols:
        for bound in boundary:
            derivative = sp.diff(f, symbol)
            subs = {sym: bound if sym == symbol else sp.Symbol(sym.name) for sym in symbols}
            bc[f'{symbol}={bound}'] = simplify_constants(derivative.subs(subs))
    return bc

def calculate_cauchy(f):
    dirichlet_bc = calculate_dirichlet(f)
    neumann_bc = calculate_neumann(f)
    # bc = {key: (("Dirichlet: " + str(dirichlet_bc[key])), "Neumann: " + str(neumann_bc[key])) for key in dirichlet_bc}
    bc = {key: (str(dirichlet_bc[key]), str(neumann_bc[key])) for key in dirichlet_bc} # add labels for LLM input
    return bc

def simplify_constants(expr):
    # round to prepare for parser
    def truncate(val):
        return round(val)
    expr = expr.subs(sp.E, truncate(sp.N(sp.E)))
    expr = expr.subs(sp.pi, truncate(sp.N(sp.pi)))
    expr = expr.subs(sp.sin(1), truncate(sp.N(sp.sin(1))))
    expr = expr.subs(sp.cos(1), truncate(sp.N(sp.cos(1))))

    return expr

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

        # calculate boundary condition
        condition_type = args.bc
        if condition_type == 'Dirichlet':
            bc = calculate_dirichlet(neg_lap_f)
        elif condition_type == 'Neumann':
            bc = calculate_neumann(neg_lap_f)
        elif condition_type == 'Cauchy':
            bc = calculate_cauchy(neg_lap_f)

        # dict of tokenized boundary conditions
        tokenized_bc = {}
        for key, condition in bc.items(): 
            tokenized_condition = Parser.get_postfix_from_str(str(condition))
            tokenized_bc[key] = tokenized_condition

        print('function:', f, '\nnegative laplace:', neg_lap_f, '\n')
        print("tokenized bc: ", tokenized_bc)
        print()
        print()
        entry = {"F_Operators": f_operators, "Solution_Operators": soln_operators, args.bc: tokenized_bc }
        entry_tuple = ((args.function,) + tuple(f_operators), tuple(soln_operators), (args.bc,) + tuple(tokenized_bc))  
        if entry_tuple not in seen_entries:
            print(entry_tuple)
            seen_entries.add(entry_tuple)
            data.append(entry)
    
    # with open('dataset.jsonl', 'w') as outfile:
    #     for entry in data:
    #         json.dump(entry, outfile)
    #         outfile.write('\n')

if __name__ == '__main__':
    generate_data(args.num)
    print("main")
