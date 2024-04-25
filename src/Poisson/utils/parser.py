import re 

# add operators as fn complexity & depth increases 
tokens = [
    '(',
    ')',
    'const',
    'X',
    '^2',
    '^3',
    '^4',
    'SIN',
    'COS',
    'EXP',
    '+',
    '-',
    '*'
]

class Parser(object):
    def __init__(self, function_str): 
        self.function_str = function_str 
    
    def make_infix(self):
        operator_list = [] 
        self.function_str = re.sub(r'x\*\*2', ',X,^2,', self.function_str)
        self.function_str = re.sub(r'x\*\*3', ',X,^3,', self.function_str)
        self.function_str = re.sub(r'x\*\*4', ',X,^4,', self.function_str)
        self.function_str = re.sub(r'exp', ',EXP,', self.function_str)
        self.function_str = re.sub(r'sin', ',SIN,', self.function_str)
        self.function_str = re.sub(r'cos', ',COS,', self.function_str)

        self.function_str = re.sub(r'x', ',X,', self.function_str)
        self.function_str = re.sub(r'\*', ',*,', self.function_str)
        self.function_str = re.sub(r'\+', ',+,', self.function_str)
        self.function_str = re.sub(r'\-', ',-,', self.function_str)
        self.function_str = re.sub(r'\(', ',(,', self.function_str)
        self.function_str = re.sub(r'\)', ',),', self.function_str)

        operator_list = self.function_str.split(',')
        operator_list = [operator.replace(' ', '') for operator in operator_list]
        operator_list = [operator for operator in operator_list if operator != '']
        const_pattern = re.compile(r'(\d+)')
        operator_list = ['const' if const_pattern.match(operator) else operator for operator in operator_list]

        return operator_list

    def make_postfix(self): 
        print("need ot make postfix")

if __name__ == '__main__':
    parser = Parser('-2*(-sin(x) + cos(x))')
    print(parser.make_infix())