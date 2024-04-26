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
# listed with precedence
operators = {
    '+': '1',
    '-': '1',
    '*': '2',
    'SIN': '2',
    'COS': '2',
    'EXP': '2',
}

class Parser(object):
    def __init__(self, function_str): 
        self.function_str = function_str 
    
    def make_infix(self):
        operator_list = [] 
        # order of operations here matters, adding extra commas to separate constants
        self.function_str = re.sub(r'\*\*2', ',^2,', self.function_str)
        self.function_str = re.sub(r'\*\*3', ',^3,', self.function_str)
        self.function_str = re.sub(r'\*\*4', ',^4,', self.function_str)
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

    def make_postfix(self, infix_list): 
        class Stack:
            def __init__(self):
                self.items = []

            def is_empty(self):
                return len(self.items) == 0

            def push(self, item):
                self.items.append(item)

            def pop(self):
                if not self.is_empty():
                    return self.items.pop()
                else:
                    raise IndexError("pop from an empty stack")

            def peek(self):
                if not self.is_empty():
                    return self.items[-1]
                else:
                    raise IndexError("peek from an empty stack")
            
            def print(self): 
                print("stack: ")
                for el in self.items: 
                    print(el + ',', end='')

            def size(self):
                return len(self.items)         
        operator_list = [] 
        stack = Stack()
        for idx, token in enumerate(infix_list):
            if token == '(':
                stack.push(token)
            elif token == ')':
                while stack.peek() != '(': 
                    operator_list.append(stack.pop())
                stack.pop()
            elif token in operators.keys(): 
                try: 
                    # remove operators with higher or equal precendence from stack 
                    while stack.peek() in operators and float(operators[stack.peek()]) >= float(operators[token]):
                        operator_list.append(stack.pop())
                    stack.push(token)
                except IndexError: 
                    stack.push(token)
            else: 
                # if operand, append to list 
                operator_list.append(token) 
            if idx == len(infix_list) - 1:
                while not stack.is_empty():
                    operator_list.append(stack.pop())
        return operator_list
            
if __name__ == '__main__':
    parser = Parser('-4*sin(x+x**2)**3')
    infix_list = parser.make_infix()
    print(infix_list)
    postfix = parser.make_postfix(infix_list)
    print(postfix)

    # x x 2 ** + sin 3 ** -4 *