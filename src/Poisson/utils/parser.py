import re 

# add operators as fn complexity & depth increases 
tokens = [
    '(',
    ')',
    'const',
    r'\x\d+',
    r'\^\d+',
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
    r'\^\d+': '3'
}

class Parser(object):
    # wrap trig functions and exp in parentheses to handle raising them to a power
    def wrap_operators(self, list): 
        idx = 0 
        while idx < len(list): 
            if list[idx] in ['SIN', 'COS', 'EXP']:
                paren_counter = 0
                list.insert(idx, '(')
                idx += 1
                idx2 = idx
                while idx2 < len(list): 
                    if list[idx2] == '(': 
                        paren_counter += 1
                    elif list[idx2] == ')':
                        paren_counter -= 1
                        if paren_counter == 0: 
                            list.insert(idx2, ')')
                            break
                    idx2 += 1
            idx += 1
        return list

    # return infix list given a function str    
    def make_infix(self, function_str):
        operator_list = [] 
        # order of operations here matters, adding extra commas to separate constants
        function_str = re.sub(r'\*\*(\d+)', r',^\1,', function_str)
        function_str = re.sub(r'exp', ',EXP,', function_str)
        function_str = re.sub(r'sin', ',SIN,', function_str)
        function_str = re.sub(r'cos', ',COS,', function_str)
        function_str = re.sub(r'x(\d+)', r',x\1,', function_str)
        function_str = re.sub(r'\*', ',*,', function_str)
        function_str = re.sub(r'\+', ',+,', function_str)
        function_str = function_str.replace(' - ', 'MINUS')
        function_str = function_str.replace('-','')
        function_str = function_str.replace('MINUS', ',-,')
        function_str = re.sub(r'\(', ',(,', function_str)
        function_str = re.sub(r'\)', ',),', function_str)

        operator_list = function_str.split(',')
        operator_list = [operator.replace(' ', '') for operator in operator_list]
        operator_list = [operator for operator in operator_list if operator != '']

        # Replace numbers with 'const' token
        const_pattern = re.compile(r'^-?\d+(\.\d+)?$|^\d*/\d*$')
        
        operator_list = ['const' if const_pattern.match(token) else token for token in operator_list]
        # print("operator list", operator_list)

        return self.wrap_operators(operator_list)

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
                return None  # Return None if stack is empty

            def peek(self):
                if not self.is_empty():
                    return self.items[-1]
                return None  # Return None if stack is empty
            
            def print(self):
                print("stack: ")
                for el in self.items:
                    print(el + ',', end='')

            def size(self):
                return len(self.items)
        
        operators = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}  # Example operator precedence
        operator_list = []
        stack = Stack()
        
        for idx, token in enumerate(infix_list):
            if token == '(':
                stack.push(token)
            elif token == ')':
                while stack.peek() is not None and stack.peek() != '(':
                    operator_list.append(stack.pop())
                stack.pop()  # Remove '(' from stack
            elif token in operators.keys():
                while stack.peek() is not None and stack.peek() in operators and operators[stack.peek()] >= operators[token]:
                    operator_list.append(stack.pop())
                stack.push(token)
            else:
                operator_list.append(token)
            
            if idx == len(infix_list) - 1:
                while not stack.is_empty():
                    operator_list.append(stack.pop())
        
        return operator_list

    def get_postfix_from_str(self, function_str): 
        infix_list = self.make_infix(function_str)
        return self.make_postfix(infix_list)
                    
if __name__ == '__main__':
    parser = Parser()
    infix_list = parser.make_infix('-4*cos(-6*x-2*x**2)**2')
    print(infix_list)
    postfix = parser.make_postfix(infix_list)
    print(postfix)

