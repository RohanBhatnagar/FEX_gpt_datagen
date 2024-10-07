import torch
from function import Functions
import argparse
from computational_tree import BinaryTree
import sympy as sp
from utils.logger import Logger
import utils.parser
import json

parser = argparse.ArgumentParser(description='NAS')

parser.add_argument('--tree', default='depth2', type=str)
parser.add_argument('--num', default=100, type=int)
parser.add_argument('--dim', default=3, type=int)
parser.add_argument('--bc', default='Dirichlet', type=str)
parser.add_argument('--function', default='Poisson', type=str)
# domain is assumed to be a [0,1] square, cube, etc.
boundary = [0, 1]
conditions = ['Dirichlet', 'Neumann', 'Cauchy']

args = parser.parse_args()

func = Functions(args.dim, "Heat")

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
            tree.action = action
        else:
            action = action
            tree.key = binary[action]
            tree.action = action
        count = count + 1
        inorder(tree.rightChild, actions)


def sp_function(tree):
    if tree is None:
        return None
    elif tree.rightChild is None and tree.leftChild is None:
        return tree.key(tree.key.args[0][0], 2)
    elif tree.rightChild is None:
        return tree.key(sp_function(tree.leftChild), 2)
    else:
        return tree.key(sp_function(tree.leftChild), sp_function(tree.rightChild))

# prints a computational binary tree


def print_fmla(tree):
    if tree is None:
        return ""
    if tree.leftChild is None and tree.rightChild is None:
        return func.unary_functions_str[tree.action].format('2', 'x')
    elif tree.rightChild is None:
        left_postfix = print_fmla(tree.leftChild)
        return func.unary_functions_str[tree.action].format('2', left_postfix)
    else:
        left_postfix = print_fmla(tree.leftChild)
        right_postfix = print_fmla(tree.rightChild)
        return func.binary_functions_str[tree.action].format(left_postfix, right_postfix)


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
            subs = {sym: bound if sym == symbol else sp.Symbol(
                sym.name) for sym in symbols}
            f = f.subs(E, 1)
            bc[f'{symbol}={bound}'] = simplify_constants(f.subs(subs))
    return bc


def calculate_neumann(f):
    bc = {}
    for symbol in symbols:
        for bound in boundary:
            derivative = sp.diff(f, symbol)
            subs = {sym: bound if sym == symbol else sp.Symbol(
                sym.name) for sym in symbols}
            bc[f'{symbol}={bound}'] = simplify_constants(derivative.subs(subs))
    return bc


def calculate_cauchy(f):
    dirichlet_bc = calculate_dirichlet(f)
    neumann_bc = calculate_neumann(f)
    bc = {key: (str(dirichlet_bc[key]), str(neumann_bc[key]))
          for key in dirichlet_bc}
    return bc


def simplify_constants(expr):
    def truncate(val):
        return round(val)
    expr = expr.subs(sp.E, truncate(sp.N(sp.E)))
    expr = expr.subs(sp.pi, truncate(sp.N(sp.pi)))
    expr = expr.subs(sp.sin(1), truncate(sp.N(sp.sin(1))))
    expr = expr.subs(sp.cos(1), truncate(sp.N(sp.cos(1))))

    return expr


def generate_data(num):
    Parser = utils.parser.Parser()
    seen_entries = set()

    max_len = 0
    longest_entry = None

    with open(f'data/{args.function}_{args.dim}dim_{args.num}.jsonl', 'w') as outfile:
        data_count = 0
        while data_count < num:
            actions = []
            for j in range(0, len(structure_choice)):
                actions.append(torch.LongTensor(
                    [torch.randint(0, structure_choice[j], (1, 1))]))
            computational_tree = get_function(actions)

            f = sp_function(computational_tree)

            if args.function == "Poisson":
                rhs = negative_laplacian(f)

            elif args.function == "Heat":
                time_symbol = sp.symbols('t')
                time_derivative = sp.diff(f, time_symbol)  # du/dt
                neg_lap_f = negative_laplacian(f)
                # Heat equation: du/dt - Laplacian(u) = 0
                rhs = time_derivative - neg_lap_f

            elif args.function == "Wave":
                print("Wave equation")

            elif args.function == "Schrodinger":
                print("Schrodinger")

            else:
                print("Function type not recognized.")

            soln_operators = Parser.get_postfix_from_str(str(f))  # lhs
            f_operators = Parser.get_postfix_from_str(str(rhs))  # rhs

            condition_type = conditions[torch.randint(0, 2, (1, 1))]
            if condition_type == 'Dirichlet':
                bc = calculate_dirichlet(f)
            elif condition_type == 'Neumann':
                bc = calculate_neumann(f)
            elif condition_type == 'Cauchy':
                bc = calculate_cauchy(f)

            # exclude bd condition for now, too long
            # tokenized_bc = [condition_type]
            # for key, values in bc.items():
            #     tokenized_bc.append(key)
            #     tokenized_bc.extend(Parser.get_postfix_from_str(str(values)))

            entry = {"Function Type": args.function,
                     "RHS": str(rhs), "true_solution": str(f)}
            # entry_tuple = (tuple(f_operators), tuple(soln_operators), tuple(tokenized_bc))
            entry_tuple = (tuple(f_operators), tuple(soln_operators))

            if entry_tuple not in seen_entries:
                seen_entries.add(entry_tuple)
                json.dump(entry, outfile)
                outfile.write('\n')
                data_count += 1

                # Track the longest entry
                entry_len = len(entry["RHS"]) + len(entry["true_solution"])
                if entry_len > max_len:
                    max_len = entry_len
                    longest_entry = entry

                if data_count % 10 == 0:
                    print(f'{data_count}/{num}')

    print(f'{args.num} samples generated for {args.function}\nMax Length was {max_len}\nLongest entry was {longest_entry}')


if __name__ == '__main__':
    generate_data(args.num)
