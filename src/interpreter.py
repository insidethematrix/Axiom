# ============================================
# Axiom Language - Tree-Walking Interpreter
# ============================================
# Walks the AST produced by the Parser and executes each node.
# Uses a dictionary as the variable environment (symbol table).

from ast_nodes import (
    NumberNode, IdentifierNode, BinOpNode, UnaryOpNode,
    VarDeclNode, AssignNode, DisplayNode,
    IfNode, WhileNode, ConditionNode, ProgramNode
)


class Interpreter:
    def __init__(self):
        self.environment = {}   # variable storage: {"x": 10, "y": 3.5, ...}

    # --------------------------------------------------
    # Main entry point
    # --------------------------------------------------

    def run(self, program_node):
        """Execute a ProgramNode (list of statements)."""
        for statement in program_node.statements:
            self.execute(statement)

    # --------------------------------------------------
    # Statement dispatcher
    # --------------------------------------------------

    def execute(self, node):
        """Dispatch to the correct handler based on node type."""
        if isinstance(node, VarDeclNode):
            return self.execute_var_decl(node)
        elif isinstance(node, AssignNode):
            return self.execute_assign(node)
        elif isinstance(node, DisplayNode):
            return self.execute_display(node)
        elif isinstance(node, IfNode):
            return self.execute_if(node)
        elif isinstance(node, WhileNode):
            return self.execute_while(node)
        else:
            raise RuntimeError(f"Unknown statement type: {type(node).__name__}")

    # --------------------------------------------------
    # Expression evaluator
    # --------------------------------------------------

    def evaluate(self, node):
        """Evaluate an expression node and return its numeric value."""
        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, IdentifierNode):
            if node.name in self.environment:
                return self.environment[node.name]
            else:
                raise RuntimeError(f"Undefined variable: '{node.name}'")

        if isinstance(node, BinOpNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            if node.op == "+":
                return left + right
            elif node.op == "-":
                return left - right
            elif node.op == "*":
                return left * right
            elif node.op == "/":
                if right == 0:
                    raise RuntimeError("Division by zero")
                return left / right
            elif node.op == "^":
                return left ** right
            else:
                raise RuntimeError(f"Unknown operator: '{node.op}'")

        if isinstance(node, UnaryOpNode):
            operand = self.evaluate(node.operand)
            if node.op == "-":
                return -operand
            else:
                raise RuntimeError(f"Unknown unary operator: '{node.op}'")

        if isinstance(node, ConditionNode):
            return self.evaluate_condition(node)

        raise RuntimeError(f"Unknown expression type: {type(node).__name__}")

    # --------------------------------------------------
    # Condition evaluator
    # --------------------------------------------------

    def evaluate_condition(self, node):
        """Evaluate a condition node and return True/False."""
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        if node.op == ">":
            return left > right
        elif node.op == "<":
            return left < right
        elif node.op == "==":
            return left == right
        elif node.op == "!=":
            return left != right
        elif node.op == ">=":
            return left >= right
        elif node.op == "<=":
            return left <= right
        else:
            raise RuntimeError(f"Unknown comparison operator: '{node.op}'")

    # --------------------------------------------------
    # Statement executors
    # --------------------------------------------------

    def execute_var_decl(self, node):
        """let x = expression;"""
        value = self.evaluate(node.value)
        self.environment[node.name] = value

    def execute_assign(self, node):
        """x = expression;"""
        if node.name not in self.environment:
            raise RuntimeError(
                f"Cannot assign to undeclared variable: '{node.name}'. "
                f"Use 'let {node.name} = ...' first."
            )
        value = self.evaluate(node.value)
        self.environment[node.name] = value

    def execute_display(self, node):
        """display(expression);"""
        value = self.evaluate(node.value)
        # Print integers without decimal point
        if isinstance(value, float) and value == int(value):
            print(int(value))
        else:
            print(value)

    def execute_if(self, node):
        """if condition then ... [else ...] end"""
        condition_result = self.evaluate(node.condition)

        if condition_result:
            for stmt in node.then_body:
                self.execute(stmt)
        elif node.else_body is not None:
            for stmt in node.else_body:
                self.execute(stmt)

    def execute_while(self, node):
        """while condition do ... end"""
        while self.evaluate(node.condition):
            for stmt in node.body:
                self.execute(stmt)
