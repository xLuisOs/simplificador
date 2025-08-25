class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value 
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.value)
    
def to_string(node):
    if node is None:
        return ""
    if node.value == "'":
        return to_string(node.left) + "'"
    if node.left and node.right:
        return f"({to_string(node.left)}{node.value}{to_string(node.right)})"
    return node.value

def extract_factors(node):
    if node.value == '*':
        return extract_factors(node.left) + extract_factors(node.right)
    return [to_string(node)]

def extract_terms(node):
    if node.value == '+':
        return extract_terms(node.left) + extract_terms(node.right)
    return [to_string(node)]

def build_product(factors):
    if not factors:
        return Node('1')
    node = Node(factors[0])
    for f in factors[1:]:
        node = Node('*', node, Node(f))
    return node

def build_sum(terms):
    if not terms:
        return Node('0')
    node = Node(terms[0])
    for t in terms[1:]:
        node = Node('+', node, Node(t))
    return node

