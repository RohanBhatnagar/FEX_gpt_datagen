import numpy as np
import torch
from torch import sin, cos, exp
import math
import sympy as sp

import sympy as sp

x, c1 = sp.symbols('x c1')  # Define symbols used in your functions

unary_functions = [
    sp.Lambda((x, c1), 0),               # Essentially 0
    sp.Lambda((x, c1), c1),    # Simplifies to just c1
    sp.Lambda((x, c1), c1*x),  # Simplifies to c1*x
    sp.Lambda((x, c1), c1*x**2),
    sp.Lambda((x, c1), c1*x**3),
    sp.Lambda((x, c1), c1*x**4),
    sp.Lambda((x, c1), c1*sp.exp(x)),
    sp.Lambda((x, c1), c1*sp.sin(x)),
    sp.Lambda((x, c1), c1*sp.cos(x))
]

x, y = sp.symbols('x y')
binary_functions = [
    sp.Lambda((x, y), x + y),
    sp.Lambda((x, y), x * y),
    sp.Lambda((x, y), x - y)
]

unary_functions_str = ['({}*(0))',
                       '({}*(1))',
                       # '5',
                       '({}*{})',
                       # '-{}',
                       '({}*({})**2)',
                       '({}*({})**3)',
                       '({}*({})**4)',
                       # '({})**5',
                       '({}*exp({}))',
                       '({}*sin({}))',
                       '({}*cos({}))',]
                       # 'ref({})',
                       # 'exp(-({})**2/2)'

unary_functions_str_leaf= ['(0)',
                           '(1)',
                           # '5',
                           '({})',
                           # '-{}',
                           '(({})**2)',
                           '(({})**3)',
                           '(({})**4)',
                           # '({})**5',
                           '(exp({}))',
                           '(sin({}))',
                           '(cos({}))',]


binary_functions_str = ['(({})+({}))',
                        '(({})*({}))',
                        '(({})-({}))']


binary_functions_str_readable = ['(+)',
                        '(+)',
                        '(-)']

unary_map = {f: desc for f, desc in zip(unary_functions, unary_functions_str)}
binary_map = {f: desc for f, desc in zip(binary_functions, binary_functions_str)}
unary_leaf_map = {f: desc for f, desc in zip(unary_functions, unary_functions_str_leaf)}

# Merge the two dictionaries into one
function_map = {**unary_map, **binary_map}