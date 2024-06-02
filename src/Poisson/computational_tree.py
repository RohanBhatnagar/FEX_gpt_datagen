import numpy as np
from function import Functions
import sympy as sp

func = Functions(3)

symbols = func.get_symbols()
unary = func.get_unary_functions()
binary = func.get_binary_functions()
unary_functions_str = func.get_unary_functions_str()
binary_functions_str = func.get_binary_functions_str()

class BinaryTree(object):
    def __init__(self,item,is_unary=True):
        self.action=0
        self.key=item
        self.is_unary=is_unary
        self.leftChild=None
        self.rightChild=None
    def insertLeft(self,item, is_unary=True):
        if self.leftChild==None:
            self.leftChild=BinaryTree(item, is_unary)
        else:
            t=BinaryTree(item)
            t.leftChild=self.leftChild
            self.leftChild=t
    def insertRight(self,item, is_unary=True):
        if self.rightChild==None:
            self.rightChild=BinaryTree(item, is_unary)
        else:
            t=BinaryTree(item)
            t.rightChild=self.rightChild
            self.rightChild=t

def compute_by_tree(tree, x):
    ''' judge whether a emtpy tree, if yes, that means the leaves and call the unary operation '''
    if tree.leftChild == None and tree.rightChild == None:
        return tree.key(x, 3)
    elif tree.leftChild == None and tree.rightChild is not None:
        return tree.key(compute_by_tree(tree.rightChild, x))
    elif tree.leftChild is not None and tree.rightChild == None:
        return tree.key(compute_by_tree(tree.leftChild, x))
    else:
        return tree.key(compute_by_tree(tree.leftChild, x), compute_by_tree(tree.rightChild, x))

def inorder(tree, actions):
    global count
    if tree:
        inorder(tree.leftChild, actions)
        action = actions[count].item()
        if tree.is_unary:
            action = action
            tree.key = unary[action]
            print(count, action, func.unary_functions_str[action])
        else:
            action = action
            tree.key = binary[action]
            print(count, action, func.binary_functions_str[action])
        count = count + 1
        inorder(tree.rightChild, actions)

count = 0
def inorder_w_idx(tree):
    global count
    if tree:
        inorder_w_idx(tree.leftChild)
        print(tree.key, count)
        count = count + 1
        inorder_w_idx(tree.rightChild)

def basic_tree():
    tree = BinaryTree('', False)
    tree.insertLeft('', False)
    tree.leftChild.insertLeft('', True)
    tree.leftChild.insertRight('', True)
    tree.insertRight('', False)
    tree.rightChild.insertLeft('', True)
    tree.rightChild.insertRight('', True)
    return tree

def get_function(actions):
    global count
    count = 0
    computation_tree = basic_tree()
    inorder(computation_tree, actions)
    count = 0
    return computation_tree

def inorder_test(tree, actions):
    global count
    if tree:
        inorder(tree.leftChild, actions)
        action = actions[count].item()
        print(action)
        if tree.is_unary:
            action = action
            tree.key = unary[action]
            print(count, action, func.unary_functions_str[action])
        else:
            action = action
            tree.key = binary[action]
            print(count, action, func.binary_functions_str[action])
        count = count + 1
        inorder(tree.rightChild, actions)


def generate_postfix(tree):
    """
    Generate the postfix notation of the binary expression tree.

    Args:
    tree (BinaryTree): The root of the binary expression tree.

    Returns:
    list: A list of tokens in postfix order.
    """
    if tree is None:
        return []
    
    left_postfix = generate_postfix(tree.leftChild)
    right_postfix = generate_postfix(tree.rightChild)
    
    if tree.is_unary:
        return left_postfix + right_postfix + [tree.key.__name__ if hasattr(tree.key, '__name__') else str(tree.key)]
    else:
        return left_postfix + right_postfix + [tree.key.__name__ if hasattr(tree.key, '__name__') else str(tree.key)]

if __name__ =='__main__':
    # tree = BinaryTree(np.add)
    # tree.insertLeft(np.multiply)
    # tree.leftChild.insertLeft(np.cos)
    # tree.leftChild.insertRight(np.sin)
    # tree.insertRight(np.sin)
    # print(compute_by_tree(tree, 30)) # np.sin(30)*np.cos(30)+np.sin(30)
    # inorder(tree)
    # inorder_w_idx(tree)
    # import torch
    # bs_action = [torch.LongTensor([10]), torch.LongTensor([2]),torch.LongTensor([9]),torch.LongTensor([1]),torch.LongTensor([0]),torch.LongTensor([2]),torch.LongTensor([6])]
    # actions = []
    # for i in range(0,7):
    #     actions.append(torch.LongTensor([torch.randint(0,3,(1,1))]))
    
    # function = lambda x: compute_by_tree(get_function(actions), x)
    # x = torch.FloatTensor([[-1], [1]])

    # count = 0
    # tr = basic_tree()
    # inorder_test(tr, actions)
    # f = binary[0](unary[2](x, 5), unary[4](x, 90))
    # print(f)
    # df = sp.diff(f, x)
    # print(df)

    count = 0

