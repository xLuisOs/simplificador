from tree import Node, to_string, extract_factors, extract_terms, build_product, build_sum
from parser import parse

def simplify_step(node, steps):
    if node is None:
        return node, False
    changed = False
    node.left, c1 = simplify_step(node.left, steps)
    node.right, c2 = simplify_step(node.right, steps)
    changed |= c1 or c2

    ##doble negacion
    if node.value == "'" and node.left.value == "'":
        steps.append(f"Doble negación: {to_string(node)} → {to_string(node.left.left)}")
        return node.left.left, True
    
    ##morgan
    if node.value == "'" and node.left:
        if node.left.value == '+':
            # (A + B)' → A'*B'
            new_node = Node('*', Node("'", node.left.left), Node("'", node.left.right))
            steps.append(f"De Morgan: {to_string(node)} → {to_string(new_node)}")
            return simplify_total(new_node, steps), True
        elif node.left.value == '*':
            # (A * B)' → A'+B'
            new_node = Node('+', Node("'", node.left.left), Node("'", node.left.right))
            steps.append(f"De Morgan: {to_string(node)} → {to_string(new_node)}")
            return simplify_total(new_node, steps), True
     
    ##identidad/anulacion
    if node.value == '+':
        if node.left.value == '0':
            steps.append(f"Identidad: {to_string(node)} → {to_string(node.right)}")
            return node.right, True
        if node.right.value == '0':
            steps.append(f"Identidad: {to_string(node)} → {to_string(node.left)}")
            return node.left, True
        if node.left.value == '1' or node.right.value == '1':
            steps.append(f"Anulación: {to_string(node)} → 1")
            return Node('1'), True
    if node.value == '*':
        if node.left.value == '1':
            steps.append(f"Identidad: {to_string(node)} → {to_string(node.right)}")
            return node.right, True
        if node.right.value == '1':
            steps.append(f"Identidad: {to_string(node)} → {to_string(node.left)}")
            return node.left, True
        if node.left.value == '0' or node.right.value == '0':
            steps.append(f"Anulación: {to_string(node)} → 0")
            return Node('0'), True
        
    ##idempotencia
    if node.value in ['+', '*'] and to_string(node.left) == to_string(node.right):
        steps.append(f"Idempotencia: {to_string(node)} → {to_string(node.left)}")
        return node.left, True
    
    if node.value == '+' and node.left and node.right and (
    to_string(node.left) + "'" == to_string(node.right) or
    to_string(node.right) + "'" == to_string(node.left)):
        steps.append(f"Complemento: {to_string(node)} → 1")
        return Node('1'), True
    if node.value == '*' and node.left and node.right and (
        to_string(node.left) + "'" == to_string(node.right) or
        to_string(node.right) + "'" == to_string(node.left)):
        steps.append(f"Complemento: {to_string(node)} → 0")
        return Node('0'), True

    
    ##absorcion
    if node.value == '+':
        if node.left.value == '*' and (to_string(node.left.left) == to_string(node.right) or to_string(node.left.right) == to_string(node.right)):
            steps.append(f"Absorción: {to_string(node)} → {to_string(node.right)}")
            return node.right, True
        if node.right.value == '*' and (to_string(node.right.left) == to_string(node.left) or to_string(node.right.right) == to_string(node.left)):
            steps.append(f"Absorción: {to_string(node)} → {to_string(node.left)}")
            return node.left, True
    if node.value == '*':
        if node.left.value == '+' and (to_string(node.left.left) == to_string(node.right) or to_string(node.left.right) == to_string(node.right)):
            steps.append(f"Absorción: {to_string(node)} → {to_string(node.right)}")
            return node.right, True
        if node.right.value == '+' and (to_string(node.right.left) == to_string(node.left) or to_string(node.right.right) == to_string(node.left)):
            steps.append(f"Absorción: {to_string(node)} → {to_string(node.left)}")
            return node.left, True
    
    ##distributiva
    if node.value == '*' and ((node.left.value == '+') or (node.right.value == '+')):
        if node.right.value == '+':
            new_node = Node('+', Node('*', node.left, node.right.left), Node('*', node.left, node.right.right))
        else:
            new_node = Node('+', Node('*', node.left.left, node.right), Node('*', node.left.right, node.right))
        steps.append(f"Distributiva: {to_string(node)} → {to_string(new_node)}")
        return simplify_total(new_node, steps), True

    return node, changed

def common_factor(node, steps):
    if node is None or node.value != '+':
        return node, False
    terms = extract_terms(node)
    if len(terms) < 2:
        return node, False
    term_factors = [set(extract_factors(parse(t))) for t in terms]
    common = set.intersection(*term_factors)
    if common:
        steps.append(f"Factor común: {to_string(node)} → {'*'.join(sorted(common))}*(" + '+'.join(['*'.join(sorted(f-common)) or '1' for f in term_factors]) + ")")
        new_terms = [build_product(sorted(f-common)) if f-common else Node('1') for f in term_factors]
        node_fact = build_product(sorted(list(common)))
        node_sum = build_sum([to_string(t) for t in new_terms])
        return Node('*', node_fact, node_sum), True
    return node, False

def simplify_total(node, steps):
    while True:
        node, change1 = simplify_step(node, steps)
        node, change2 = common_factor(node, steps)
        if not (change1 or change2):
            break
    return node

def optimize_tree(node):
    if node is None:
        return None
    node.left = optimize_tree(node.left)
    node.right = optimize_tree(node.right)
    if node.value == '+':
        terms = list(set(extract_terms(node)))
        terms.sort()
        return build_sum(terms)
    elif node.value == '*':
        factors = list(set(extract_factors(node)))
        factors.sort()
        return build_product(factors)
    return node