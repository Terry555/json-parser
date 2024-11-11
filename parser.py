class ASTNode:
    """Base class for all AST nodes."""
    pass

class ObjectNode(ASTNode):
    """Represents a JSON object."""
    def __init__(self, items=None):
        self.items = items or []

class ArrayNode(ASTNode):
    """Represents a JSON array."""
    def __init__(self, elements=None):
        self.elements = elements or []

class PairNode(ASTNode):
    """Represents a key-value pair in an object."""
    def __init__(self, key, value):
        self.key = key
        self.value = value

class ValueNode(ASTNode):
    """Represents a simple value (string, number, boolean, or null)."""
    def __init__(self, value):
        self.value = value

# Token types
LBRACE = 'LBRACE'
RBRACE = 'RBRACE'
LBRACKET = 'LBRACKET'
RBRACKET = 'RBRACKET'
STRING = 'STRING'
NUMBER = 'NUMBER'
BOOLEAN = 'BOOLEAN'
NULL = 'NULL'
COLON = 'COLON'
COMMA = 'COMMA'
EOF = 'EOF'

# Parser class that builds the AST from the token stream
class JSONParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        """Get the current token."""
        return self.tokens[self.pos]

    def eat(self, token_type):
        """Consume the current token if it matches the expected type."""
        if self.current_token()[0] == token_type:
            self.pos += 1
        else:
            raise SyntaxError(f"Expected {token_type}, but found {self.current_token()[0]}")

    def parse(self):
        """Parse the token stream and build the AST."""
        return self.s()

    def s(self):
        """S → {} | [] | {A} | [D]"""
        token_type = self.current_token()[0]
        if token_type == LBRACE:
            self.eat(LBRACE)
            if self.current_token()[0] == RBRACE:
                self.eat(RBRACE)
                return ObjectNode()
            else:
                obj = ObjectNode(self.a())
                self.eat(RBRACE)
                return obj
        elif token_type == LBRACKET:
            self.eat(LBRACKET)
            if self.current_token()[0] == RBRACKET:
                self.eat(RBRACKET)
                return ArrayNode()
            else:
                arr = ArrayNode(self.d())
                self.eat(RBRACKET)
                return arr
        else:
            raise SyntaxError(f"Unexpected token {self.current_token()[0]}")

    def a(self):
        """A → <STRING>:B | <STRING>:B, A"""
        pairs = [self.pair()]
        while self.current_token()[0] == COMMA:
            self.eat(COMMA)
            pairs.append(self.pair())
        return pairs

    def pair(self):
        """<STRING>:B"""
        key = self.current_token()[1]  # Assuming the token is (STRING, value)
        self.eat(STRING)
        self.eat(COLON)
        value = self.b()
        return PairNode(key, value)

    def b(self):
        """B → S | C"""
        if self.current_token()[0] == LBRACE or self.current_token()[0] == LBRACKET:
            return self.s()
        else:
            return self.c()

    def c(self):
        """C → <STRING> | <NUMBER> | <BOOLEAN> | <NULL>"""
        token_type = self.current_token()[0]
        if token_type == STRING:
            value = self.current_token()[1]
            self.eat(STRING)
            return ValueNode(value)
        elif token_type == NUMBER:
            value = self.current_token()[1]
            self.eat(NUMBER)
            return ValueNode(value)
        elif token_type == BOOLEAN:
            value = self.current_token()[1]
            self.eat(BOOLEAN)
            return ValueNode(value)
        elif token_type == NULL:
            self.eat(NULL)
            return ValueNode(None)
        else:
            raise SyntaxError(f"Unexpected token {self.current_token()[0]}")

    def d(self):
        """D → B,D | B"""
        elements = [self.b()]
        while self.current_token()[0] == COMMA:
            self.eat(COMMA)
            elements.append(self.b())
        return elements

# Example usage:
# Assume tokens are passed as a list of tuples (token_type, token_value)

tokens = [
    (LBRACE, '{'),
    (STRING, "name"), (COLON, ':'), (STRING, "John"),
    (COMMA, ','),
    (STRING, "age"), (COLON, ':'), (NUMBER, 30),
    (RBRACE, '}'),
    (EOF, None)
]

parser = JSONParser(tokens)
ast = parser.parse()

# The AST is now built. You can traverse it or evaluate it as needed.
print(ast)
