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
    '^2': '3',
    '^3': '3',
    '^4': '3',
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
        function_str = re.sub(r'\*\*2', ',^2,', function_str)
        function_str = re.sub(r'\*\*3', ',^3,', function_str)
        function_str = re.sub(r'\*\*4', ',^4,', function_str)
        function_str = re.sub(r'exp', ',EXP,', function_str)
        function_str = re.sub(r'sin', ',SIN,', function_str)
        function_str = re.sub(r'cos', ',COS,', function_str)
        function_str = re.sub(r'x', ',X,', function_str)
        function_str = re.sub(r'\*', ',*,', function_str)
        function_str = re.sub(r'\+', ',+,', function_str)
        function_str = re.sub(r'\-', ',-,', function_str)
        function_str = re.sub(r'\(', ',(,', function_str)
        function_str = re.sub(r'\)', ',),', function_str)
        # function_str = re.sub(r'(?<=\d)\-', ',-,', function_str)  # For subtraction
        # function_str = re.sub(r'(?<![\d\w])\-', ',-', function_str)  # For negative numbers

        operator_list = function_str.split(',')
        operator_list = [operator.replace(' ', '') for operator in operator_list]
        operator_list = [operator for operator in operator_list if operator != '']
        neg_const = re.compile(r'(-\d+)')
        # pos_const = re.compile(r'(\d+)')
        # operator_list = ['n_const' if neg_const.match(operator) else 'p_const' if pos_const.match(operator) else operator for operator in operator_list]
        for idx, token in enumerate(operator_list): 
            if token == '-':
                if idx == 0 and operator_list[idx + 1] == 'const':
                    operator_list[idx+1] = 'n_const'
                    operator_list[idx] = 'REMOVE'
                elif idx > 0 and operator_list[idx-1] == '(':
                    operator_list[idx+1] = 'n_const'
                    operator_list[idx] = 'REMOVE'   

        pos_const = re.compile(r'(\d+)')
        operator_list = ['n_const' if neg_const.match(operator) else 'p_const' if pos_const.match(operator) else operator for operator in operator_list]

        # function_str = re.sub(r'\*\*2', ',^2,', function_str)
        # function_str = re.sub(r'\*\*3', ',^3,', function_str)
        # function_str = re.sub(r'\*\*4', ',^4,', function_str)
        # function_str = re.sub(r'exp', ',EXP,', function_str)
        # function_str = re.sub(r'sin', ',SIN,', function_str)
        # function_str = re.sub(r'cos', ',COS,', function_str)
        # function_str = re.sub(r'x', ',X,', function_str)
        # function_str = re.sub(r'\*', ',*,', function_str)
        # function_str = re.sub(r'\+', ',+,', function_str)
        # function_str = re.sub(r'\(', ',(,', function_str)
        # function_str = re.sub(r'\)', ',),', function_str)
        
        # New regex to handle minus as unary (negative numbers) and binary (subtraction)
        # function_str = re.sub(r'(?<=\d)\-', ',-,', function_str)  # For subtraction
        # function_str = re.sub(r'(?<![\d\w])\-', ',-', function_str)  # For negative numbers

        # Unary negative at the start or after an open parenthesis
        # print(" BEFORE - : " + function_str )
        # function_str = re.sub(r'(?<=^)\-', ',-', function_str)
        # # Subtraction (or other uses of hyphen not matched by the previous pattern)
        # function_str = re.sub(r'(?<!^)\-', ',-,', function_str)

        # Split and filter empty strings
        # operator_list = [token for token in function_str.split(',') if token.strip()]

        # # Replace numbers with 'const' token
        # const_pattern = re.compile(r'^-?\d+(\.\d+)?$')  # Matches integers and decimals, negative or positive
        # operator_list = ['const' if const_pattern.match(token) else token for token in operator_list]

        return self.wrap_operators(operator_list)

    # generate postfix list, given infix list 
    # def make_postfix(self, infix_list): 
    #     class Stack:
    #         def __init__(self):
    #             self.items = []

    #         def is_empty(self):
    #             return len(self.items) == 0

    #         def push(self, item):
    #             self.items.append(item)

    #         def pop(self):
    #             if not self.is_empty():
    #                 return self.items.pop()
    #             else:
    #                 raise IndexError("pop from an empty stack")

    #         def peek(self):
    #             if not self.is_empty():
    #                 return self.items[-1]
    #             else:
    #                 raise IndexError("peek from an empty stack")
            
    #         def print(self): 
    #             print("stack: ")
    #             for el in self.items: 
    #                 print(el + ',', end='')

    #         def size(self):
    #             return len(self.items)         
    #     operator_list = [] 
    #     stack = Stack()
    #     for idx, token in enumerate(infix_list):
    #         if token == '(':
    #             stack.push(token)
    #         elif token == ')':
    #             while stack.peek() != '(': 
    #                 operator_list.append(stack.pop())
    #             stack.pop()
    #         elif token in operators.keys(): 
    #             try: 
    #                 # remove operators with higher or equal precendence from stack 
    #                 while stack.peek() in operators and float(operators[stack.peek()]) >= float(operators[token]):
    #                     operator_list.append(stack.pop())
    #                 stack.push(token)
    #             except IndexError: 
    #                 stack.push(token)
    #         else: 
    #             # if operand, append to list 
    #             operator_list.append(token) 
    #         if idx == len(infix_list) - 1:
    #             while not stack.is_empty():
    #                 operator_list.append(stack.pop())
    #     return operator_list
    
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

