import re
from typing import Dict, List, Union, Any

class Node:
    def __init__(self, node_type: str, value: Any = None):
        self.type = node_type
        self.value = value
        self.left = None
        self.right = None

    def to_dict(self) -> Dict[str, Any]:
        result = {"type": self.type, "value": self.value}
        if self.left:
            result["left"] = self.left.to_dict()
        if self.right:
            result["right"] = self.right.to_dict()
        return result

class RuleEngine:
    def __init__(self):
        self.operators = {'AND': all, 'OR': any}
        self.comparisons = {
            '=': lambda x, y: x == y,
            '!=': lambda x, y: x != y,
            '>': lambda x, y: x > y,
            '<': lambda x, y: x < y,
            '>=': lambda x, y: x >= y,
            '<=': lambda x, y: x <= y
        }

    def create_rule(self, rule_string: str) -> Node:
        tokens = re.findall(r'\(|\)|AND|OR|[\w\']+|[<>=!]+', rule_string)
        return self._parse_expression(tokens)

    def _parse_expression(self, tokens: List[str]) -> Union[Node, None]:
        if not tokens:
            return None

        stack = []
        for token in tokens:
            if token == '(':
                stack.append(token)
            elif token == ')':
                sub_expr = []
                while stack and stack[-1] != '(':
                    sub_expr.insert(0, stack.pop())
                if stack and stack[-1] == '(':
                    stack.pop()
                node = self._create_sub_tree(sub_expr)
                stack.append(node)
            else:
                stack.append(token)

        return self._create_sub_tree(stack)

    def _create_sub_tree(self, tokens: List[Union[str, Node]]) -> Node:
        if len(tokens) == 1:
            return tokens[0] if isinstance(tokens[0], Node) else Node('operand', tokens[0])

        for op in ['OR', 'AND']:
            if op in tokens:
                idx = tokens.index(op)
                node = Node('operator', op)
                node.left = self._create_sub_tree(tokens[:idx])
                node.right = self._create_sub_tree(tokens[idx+1:])
                return node

        # Handle comparison
        left, op, right = tokens
        node = Node('operator', op)
        node.left = Node('operand', left)
        node.right = Node('operand', right)
        return node

    def evaluate_rule(self, rule_ast: Dict[str, Any], data: Dict[str, Any]) -> bool:
        def evaluate_node(node):
            if node['type'] == 'operand':
                return self._get_value(node['value'], data)
            elif node['type'] == 'operator':
                if node['value'] in self.operators:
                    return self.operators[node['value']]([
                        evaluate_node(node['left']),
                        evaluate_node(node['right'])
                    ])
                else:
                    left_value = evaluate_node(node['left'])
                    right_value = evaluate_node(node['right'])
                    return self.comparisons[node['value']](left_value, right_value)
        
        return evaluate_node(rule_ast)

    def _get_value(self, value: str, data: Dict[str, Any]) -> Any:
        if value in data:
            return data[value]
        elif value.startswith("'") and value.endswith("'"):
            return value.strip("'")
        else:
            try:
                return int(value)
            except ValueError:
                try:
                    return float(value)
                except ValueError:
                    return value

    def get_ast_json(self, root: Node) -> Dict[str, Any]:
        return root.to_dict()

    def combine_rules(self, rule_strings: List[str]) -> Dict[str, Any]:
        if not rule_strings:
            raise ValueError("No rules to combine")
        
        rule_asts = [self.create_rule(rule_string) for rule_string in rule_strings]
        
        # Count the occurrences of AND and OR operators
        operator_count = {'AND': 0, 'OR': 0}
        for ast in rule_asts:
            self._count_operators(ast, operator_count)
        
        # Choose the most frequent operator as the root
        root_operator = 'AND' if operator_count['AND'] >= operator_count['OR'] else 'OR'
        
        combined_ast = Node('operator', root_operator)
        for ast in rule_asts:
            if combined_ast.left is None:
                combined_ast.left = ast
            elif combined_ast.right is None:
                combined_ast.right = ast
            else:
                new_node = Node('operator', root_operator)
                new_node.left = combined_ast
                new_node.right = ast
                combined_ast = new_node
        
        return self.get_ast_json(combined_ast)

    def _count_operators(self, node: Node, count: Dict[str, int]):
        if node.type == 'operator' and node.value in ['AND', 'OR']:
            count[node.value] += 1
            self._count_operators(node.left, count)
            self._count_operators(node.right, count)
def validate_rule_string(rule_string: str) -> bool:
    # Check for balanced parentheses
    if rule_string.count('(') != rule_string.count(')'):
        return False
    
    # Check for valid operators and comparisons
    valid_tokens = set(['AND', 'OR', '=', '!=', '>', '<', '>=', '<='])
    tokens = re.findall(r'\b\w+\b|[<>=!]+', rule_string)
    
    for i, token in enumerate(tokens):
        if token in valid_tokens:
            if i == 0 or i == len(tokens) - 1:
                return False
            if tokens[i-1] in valid_tokens or tokens[i+1] in valid_tokens:
                return False
    
    return True
# Example usage
if __name__ == "__main__":
    rule_engine = RuleEngine()
    rule_string = "((age > 30 AND department = 'Marketing')) OR (salary >20000 OR experience > 5)"
    
    # Create rule and get AST
    ast_root = rule_engine.create_rule(rule_string)
    ast_json = rule_engine.get_ast_json(ast_root)
    print("AST (JSON format):")
    print(ast_json)
    
    # Evaluate rule
    data = {
        "age": 35,
        "department": "Sales",
        "salary": 60000,
        "experience": 10
    }
    result = rule_engine.evaluate_rule(ast_root, data)
    print("\nEvaluation Result:", result)