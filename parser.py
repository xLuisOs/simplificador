from tree import Node

def parse(expr):
    expr = expr.replace(" ", "")
    return parse_sum(expr)

def parse_sum(expr):
    bal = 0
    for i in range(len(expr)-1, -1, -1):
        c = expr[i]
        if c == ')': bal += 1
        elif c == '(': bal -= 1
        elif c == '+' and bal == 0:
            left = parse_sum(expr[:i])
            right = parse_product(expr[i+1:])
            return Node('+', left, right)
    return parse_product(expr)

def parse_product(expr):
    bal = 0
    for i in range(len(expr)-1, -1, -1):
        c = expr[i]
        if c == ')': bal += 1
        elif c == '(': bal -= 1
        elif c == '*' and bal == 0:
            left = parse_product(expr[:i])
            right = parse_unary(expr[i+1:])
            return Node('*', left, right)
    return parse_unary(expr)

def parse_unary(expr):
    if expr.startswith('(') and expr.endswith(')'):
        return parse(expr[1:-1])
    if expr.endswith("'"):
        node = parse_unary(expr[:-1])
        return Node("'", node)
    return Node(expr)
