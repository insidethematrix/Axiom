# ============================================
# Axiom Language - Recursive Descent Parser
# ============================================
# Converts a list of tokens (from the Lexer) into an AST.
# Each grammar rule maps directly to a method.
#
# Grammar mapping:
#   program    -> parse_program()
#   statement  -> parse_statement()
#   condition  -> parse_condition()
#   expression -> parse_expression()
#   term       -> parse_term()
#   factor     -> parse_factor()
#   atom       -> parse_atom()

from lexer import TokenType
from ast_nodes import (
    NumberNode, IdentifierNode, BinOpNode, UnaryOpNode,
    VarDeclNode, AssignNode, DisplayNode,
    IfNode, WhileNode, ConditionNode, ProgramNode
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0]

    # --------------------------------------------------
    # Helper methods
    # --------------------------------------------------

    def advance(self):
        """Move to the next token."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]

    def expect(self, token_type):
        """Consume the current token if it matches, otherwise raise an error."""
        if self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        else:
            raise SyntaxError(
                f"Expected {token_type.value}, "
                f"but got {self.current_token.type.value} "
                f"('{self.current_token.lexeme}')"
            )

    # --------------------------------------------------
    # program = {statement};
    # --------------------------------------------------

    def parse_program(self):
        """Entry point: parse all statements until EOF."""
        statements = []
        while self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            statements.append(stmt)
        return ProgramNode(statements)

    # --------------------------------------------------
    # statement = (variable_declaration | assignment | display_statement) ";"
    #           | if_statement
    #           | while_statement;
    # --------------------------------------------------

    def parse_statement(self):
        token = self.current_token

        # --- let declaration ---
        if token.type == TokenType.LET:
            stmt = self.parse_variable_declaration()
            self.expect(TokenType.SEMICOLON)
            return stmt

        # --- if statement (no semicolon needed) ---
        if token.type == TokenType.IF:
            return self.parse_if_statement()

        # --- while statement (no semicolon needed) ---
        if token.type == TokenType.WHILE:
            return self.parse_while_statement()

        # --- display statement ---
        if token.type == TokenType.DISPLAY:
            stmt = self.parse_display_statement()
            self.expect(TokenType.SEMICOLON)
            return stmt

        # --- assignment (identifier = expression) ---
        if token.type == TokenType.IDENTIFIER:
            stmt = self.parse_assignment()
            self.expect(TokenType.SEMICOLON)
            return stmt

        raise SyntaxError(
            f"Unexpected token: {token.type.value} ('{token.lexeme}')"
        )

    # --------------------------------------------------
    # variable_declaration = "let" identifier "=" expression;
    # --------------------------------------------------

    def parse_variable_declaration(self):
        self.expect(TokenType.LET)
        name_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        return VarDeclNode(name_token.lexeme, value)

    # --------------------------------------------------
    # assignment = identifier "=" expression;
    # --------------------------------------------------

    def parse_assignment(self):
        name_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        return AssignNode(name_token.lexeme, value)

    # --------------------------------------------------
    # display_statement = "display" "(" expression ")";
    # --------------------------------------------------

    def parse_display_statement(self):
        self.expect(TokenType.DISPLAY)
        self.expect(TokenType.LPAREN)
        value = self.parse_expression()
        self.expect(TokenType.RPAREN)
        return DisplayNode(value)

    # --------------------------------------------------
    # if_statement = "if" condition "then" {statement}
    #                ["else" {statement}] "end";
    # --------------------------------------------------

    def parse_if_statement(self):
        self.expect(TokenType.IF)
        condition = self.parse_condition()
        self.expect(TokenType.THEN)

        # Parse then-body: collect statements until ELSE or END
        then_body = []
        while self.current_token.type not in (TokenType.ELSE, TokenType.END):
            then_body.append(self.parse_statement())

        # Optional else-body
        else_body = None
        if self.current_token.type == TokenType.ELSE:
            self.advance()  # consume 'else'
            else_body = []
            while self.current_token.type != TokenType.END:
                else_body.append(self.parse_statement())

        self.expect(TokenType.END)
        return IfNode(condition, then_body, else_body)

    # --------------------------------------------------
    # while_statement = "while" condition "do" {statement} "end";
    # --------------------------------------------------

    def parse_while_statement(self):
        self.expect(TokenType.WHILE)
        condition = self.parse_condition()
        self.expect(TokenType.DO)

        body = []
        while self.current_token.type != TokenType.END:
            body.append(self.parse_statement())

        self.expect(TokenType.END)
        return WhileNode(condition, body)

    # --------------------------------------------------
    # condition = expression (">" | "<" | "==" | "!=" | ">=" | "<=") expression;
    # --------------------------------------------------

    COMPARISON_OPS = {
        TokenType.GREATER, TokenType.LESS,
        TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL,
        TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL
    }

    def parse_condition(self):
        left = self.parse_expression()

        if self.current_token.type in self.COMPARISON_OPS:
            op = self.current_token
            self.advance()
            right = self.parse_expression()
            return ConditionNode(left, op.lexeme, right)

        raise SyntaxError(
            f"Expected comparison operator, "
            f"got {self.current_token.type.value} ('{self.current_token.lexeme}')"
        )

    # --------------------------------------------------
    # expression = term {("+" | "-") term};
    # --------------------------------------------------

    def parse_expression(self):
        node = self.parse_term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token
            self.advance()
            right = self.parse_term()
            node = BinOpNode(node, op.lexeme, right)

        return node

    # --------------------------------------------------
    # term = factor {("*" | "/") factor};
    # --------------------------------------------------

    def parse_term(self):
        node = self.parse_factor()

        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            op = self.current_token
            self.advance()
            right = self.parse_factor()
            node = BinOpNode(node, op.lexeme, right)

        return node

    # --------------------------------------------------
    # factor = atom ["^" factor];    (right-associative)
    # --------------------------------------------------

    def parse_factor(self):
        node = self.parse_atom()

        if self.current_token.type == TokenType.POWER:
            op = self.current_token
            self.advance()
            right = self.parse_factor()  # recursive for right-associativity
            node = BinOpNode(node, op.lexeme, right)

        return node

    # --------------------------------------------------
    # atom = ["-"] (number | identifier | "(" expression ")");
    # --------------------------------------------------

    def parse_atom(self):
        # Unary minus
        if self.current_token.type == TokenType.MINUS:
            op = self.current_token
            self.advance()
            operand = self.parse_atom()
            return UnaryOpNode(op.lexeme, operand)

        # Number literal
        if self.current_token.type == TokenType.NUMBER:
            token = self.current_token
            self.advance()
            value = float(token.lexeme) if "." in token.lexeme else int(token.lexeme)
            return NumberNode(value)

        # Identifier (variable reference)
        if self.current_token.type == TokenType.IDENTIFIER:
            token = self.current_token
            self.advance()
            return IdentifierNode(token.lexeme)

        # Parenthesized expression
        if self.current_token.type == TokenType.LPAREN:
            self.advance()  # consume '('
            node = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return node

        raise SyntaxError(
            f"Unexpected token in expression: "
            f"{self.current_token.type.value} ('{self.current_token.lexeme}')"
        )
