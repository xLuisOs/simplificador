from tree import Node

def parse_expression(expr):
    expr = expr.replace(" ", "")
    return parse_or(expr)

def parse_or(expr):
    parts = split_outside(expr, '+')
    if len(parts) > 1:
        node = Node('+', parse_or(parts[0]), parse_or(parts[1]))
        return node
    return parse_and(expr)

def parse_and(expr):
    parts = split_outside(expr, '*')
    if len(parts) > 1:
        node = Node('*', parse_and(parts[0]), parse_and(parts[1]))
        return node
    return parse_not(expr)

def parse_not(expr):
    if expr.endswith("'"):
        return Node("'", parse_not(expr[:-1]))
    return parse_parentheses(expr)

def parse_parentheses(expr):
    if expr.startswith("(") and expr.endswith(")") and is_balanced(expr[1:-1]):
        return parse_expression(expr[1:-1])
    return Node(expr)

def split_outside(expr, symbol):
    level = 0
    parts = []
    last_index = 0
    for i, c in enumerate(expr):
        if c == "(":
            level += 1
        elif c == ")":
            level -= 1
        elif c == symbol and level == 0:
            parts.append(expr[last_index:i])
            last_index = i + 1
    parts.append(expr[last_index:])
    return parts

def is_balanced(expr):
    level = 0
    for c in expr:
        if c == "(":
            level += 1
        elif c == ")":
            level -= 1
            if level < 0:
                return False
    return level == 0
