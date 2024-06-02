import numpy as np
import torch
from torch import sin, cos, exp
import math
import sympy as sp

class Functions:
    def __init__(self, dimension):
        self.dimension = dimension
        self._generate_functions()
    
    def _generate_functions(self):
        self.symbols = sp.symbols(f'x:{self.dimension}')
        print(self.symbols)
        c1 = sp.symbols('c1')
        
        self.unary_functions = []
        
        for symbol in self.symbols: 
            self.unary_functions.extend(
                [sp.Lambda((symbol, c1), 0),
                sp.Lambda((symbol, c1), c1),
                sp.Lambda((symbol, c1), c1 * symbol), 
                sp.Lambda((symbol, c1), c1 * (symbol) ** 2),
                sp.Lambda((symbol, c1), c1 * (symbol) ** 3),
                sp.Lambda((symbol, c1), c1 * (symbol) ** 4),
                sp.Lambda((symbol, c1), c1 * sp.exp(symbol)),
                sp.Lambda((symbol, c1), c1 * sp.sin(symbol)),
                sp.Lambda((symbol, c1), c1 * sp.cos(symbol))]
            )
            

        x, y = sp.symbols('x y')
        self.binary_functions = [
            sp.Lambda((x, y), x + y),
            sp.Lambda((x, y), x * y),
            sp.Lambda((x, y), x - y)
        ]

        self.unary_functions_str = [
            '({}*(0))',
            '({}*(1))',
            '({}*{})',
            '({}*({})**2)',
            '({}*({})**3)',
            '({}*({})**4)',
            '({}*exp({}))',
            '({}*sin({}))',
            '({}*cos({}))',
        ]

        self.unary_functions_str_leaf = [
            '(0)',
            '(1)',
            '({})',
            '(({})**2)',
            '(({})**3)',
            '(({})**4)',
            '(exp({}))',
            '(sin({}))',
            '(cos({}))',
        ]

        self.binary_functions_str = [
            '(({})+({}))',
            '(({})*({}))',
            '(({})-({}))'
        ]

        self.binary_functions_str_readable = [
            '(+)',
            '(*)',
            '(-)'
        ]

        self.unary_map = {f: desc for f, desc in zip(self.unary_functions, self.unary_functions_str)}
        self.binary_map = {f: desc for f, desc in zip(self.binary_functions, self.binary_functions_str)}
        self.unary_leaf_map = {f: desc for f, desc in zip(self.unary_functions, self.unary_functions_str_leaf)}

        self.function_map = {**self.unary_map, **self.binary_map}

    def get_unary_functions(self):
        return self.unary_functions

    def get_binary_functions(self):
        return self.binary_functions

    def get_unary_functions_str(self): 
        return self.unary_functions_str

    def get_unary_functions_str_leaf(self):
        return self.unary_functions_str_leaf

    def get_binary_functions_str(self):
        return self.binary_functions_str

    def get_function_map(self):
        return self.function_map

    def get_unary_leaf_map(self):
        return self.unary_leaf_map

    def get_symbols(self):
        return self.symbols