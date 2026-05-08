# ============================================
# Axiom Language - AST Node Definitions
# ============================================
# Each node represents a construct in the Axiom grammar.
# The parser builds a tree of these nodes from the token stream.


class NumberNode:
    """Represents a numeric literal (int or float)."""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumberNode({self.value})"


class IdentifierNode:
    """Represents a variable reference."""
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"IdentifierNode({self.name})"


class BinOpNode:
    """Represents a binary operation: left op right."""
    def __init__(self, left, op, right):
        self.left = left
        self.op = op        # Token (e.g. PLUS, MINUS, MULTIPLY ...)
        self.right = right

    def __repr__(self):
        return f"BinOpNode({self.left} {self.op} {self.right})"


class UnaryOpNode:
    """Represents a unary operation (e.g. -5)."""
    def __init__(self, op, operand):
        self.op = op        # Token (MINUS)
        self.operand = operand

    def __repr__(self):
        return f"UnaryOpNode({self.op} {self.operand})"


class VarDeclNode:
    """Represents: let x = expression"""
    def __init__(self, name, value):
        self.name = name    # string (identifier name)
        self.value = value  # expression node

    def __repr__(self):
        return f"VarDeclNode(let {self.name} = {self.value})"


class AssignNode:
    """Represents: x = expression"""
    def __init__(self, name, value):
        self.name = name    # string (identifier name)
        self.value = value  # expression node

    def __repr__(self):
        return f"AssignNode({self.name} = {self.value})"


class DisplayNode:
    """Represents: display(expression)"""
    def __init__(self, value):
        self.value = value  # expression node

    def __repr__(self):
        return f"DisplayNode({self.value})"


class IfNode:
    """Represents: if condition then {statements} [else {statements}] end"""
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition      # BinOpNode (comparison)
        self.then_body = then_body      # list of statement nodes
        self.else_body = else_body      # list of statement nodes or None

    def __repr__(self):
        return f"IfNode(if {self.condition} then ... else ...)"


class WhileNode:
    """Represents: while condition do {statements} end"""
    def __init__(self, condition, body):
        self.condition = condition      # BinOpNode (comparison)
        self.body = body                # list of statement nodes

    def __repr__(self):
        return f"WhileNode(while {self.condition} do ...)"


class ConditionNode:
    """Represents a comparison: left op right (>, <, ==, !=, >=, <=)."""
    def __init__(self, left, op, right):
        self.left = left
        self.op = op        # Token (comparison operator)
        self.right = right

    def __repr__(self):
        return f"ConditionNode({self.left} {self.op} {self.right})"


class ProgramNode:
    """Root node: holds a list of statements."""
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"ProgramNode({len(self.statements)} statements)"
