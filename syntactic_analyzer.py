
'''#Syntactic Analyzer
def parse(tokens):
    types = []
    for token in tokens:
        space = token.index(' ')
        token_type = token[space+1:-1]
        types.append(token_type)

if __name__ == "__main__":
    tokens = ['<"{", OPENCURLYBRACKET>', '<"name", STRING>', '<":", OPERATOR>', '<"Alice", STRING>', '<",", SEPARATOR>', '<"age", STRING>', '<":", OPERATOR>', '<"30", NUMBER>', '<",", SEPARATOR>', '<"isStudent", STRING>', '<":", OPERATOR>', '<"false", BOOLEAN>', '<",", SEPARATOR>', '<"email", STRING>', '<":", OPERATOR>', '<"null", NULL>', '<"}", CLOSEDCURLYBRACKET>']
    parse(tokens)'''

class ASTNode:
    """Base class for all AST nodes."""
    pass

class ObjectNode(ASTNode):
    """Represents a JSON object."""
    def __init__(self, items=None):
        self.items = items or []

    def __repr__(self):
        return f"ObjectNode(items={self.items})"

    def print_tree(self, indent="", is_last=True):
        print(f"{indent}{{")
        for i, pair in enumerate(self.items):
            is_last_pair = (i == len(self.items) - 1)
            pair.print_tree(f"{indent}    ", is_last_pair)
        print(f"{indent}}}")

class ArrayNode(ASTNode):
    """Represents a JSON array."""
    def __init__(self, elements=None):
        self.elements = elements or []

    def __repr__(self):
        return f"ArrayNode(elements={self.elements})"

    def print_tree(self, indent="", is_last=True):
        print(f"{indent}[")
        for i, element in enumerate(self.elements):
            is_last_element = (i == len(self.elements) - 1)
            element.print_tree(f"{indent}    ", is_last_element)
        print(f"{indent}]")

class PairNode(ASTNode):
    """Represents a key-value pair in an object."""
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return f"PairNode(key={self.key}, value={self.value})"

    def print_tree(self, indent="", is_last=True):
        if is_last:
            symbol = "└──"
        else:
            symbol = "├──"
        print(f"{indent}{symbol} \"{self.key}\"")
        print(f"{indent}    :")
        self.value.print_tree(f"{indent}    ", True)

class ValueNode(ASTNode):
    """Represents a simple value (string, number, boolean, or null)."""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"ValueNode(value={self.value})"

    def print_tree(self, indent="", is_last=True):
        if is_last:
            symbol = "└──"
        else:
            symbol = "├──"
        print(f"{indent}{symbol} \"{self.value}\"")

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
        self.tokens = []
        for token in tokens:
            quote = token.index('"')
            space = token.index(' ')
            token_value = token[quote:space-2]
            token_type = token[space+1:-1]
            self.tokens.append((token_value, token_type))
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
        if token_type == "OPENCURLYBRACKET":
            self.eat(LBRACE)
            if self.current_token()[0] == "CLOSEDCURLYBRACKET":
                self.eat(RBRACE)
                return ObjectNode()
            else:
                obj = ObjectNode(self.a())
                self.eat(RBRACE)
                return obj
        elif token_type == "OPENSQUAREBRACKET":
            self.eat(LBRACKET)
            if self.current_token()[0] == "CLOSEDSQUAREBRACKET":
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
        token_type = self.current_token()[0]
        if self.current_token()[0] == "OPENCURLYBRACKET" or self.current_token()[0] == "OPENSQUAREBRACKET":
            return self.s()
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

# Print the tree structure
ast.print_tree()
