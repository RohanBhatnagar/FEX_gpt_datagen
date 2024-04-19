import numpy as np
import torch
from torch import sin, cos, exp
import math

unary_functions = [lambda x: 0*x**2,
                   lambda x: 1+0*x**2,
                   lambda x: x+0*x**2,
                   lambda x: x**2,
                   lambda x: x**3,
                   lambda x: x**4,
                   torch.exp,
                   torch.sin,
                   torch.cos,
                   ]

binary_functions = [lambda x,y: x+y,
                    lambda x,y: x*y,
                    lambda x,y: x-y]


unary_functions_str = ['({}*(0)+{})',
                       '({}*(1)+{})',
                       # '5',
                       '({}*{}+{})',
                       # '-{}',
                       '({}*({})**2+{})',
                       '({}*({})**3+{})',
                       '({}*({})**4+{})',
                       # '({})**5',
                       '({}*exp({})+{})',
                       '({}*sin({})+{})',
                       '({}*cos({})+{})',]
                       # 'ref({})',
                       # 'exp(-({})**2/2)']

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
