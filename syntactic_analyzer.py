import os
import lexical_analyzer as lex

class ObjectNode():
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

class ArrayNode():
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


class PairNode():
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

class ValueNode():
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __repr__(self):
        return f"ValueNode(value={self.value})"

    def print_tree(self, indent="", is_last=True):
        if is_last:
            symbol = "└──"
        else:
            symbol = "├──"
        print(f"{indent}{symbol} \"{self.value}\"")

OPENCURLYBRACKET = 'OPENCURLYBRACKET'
CLOSEDCURLYBRACKET = 'CLOSEDCURLYBRACKET'
OPENSQUAREBRACKET = 'OPENSQUAREBRACKET'
CLOSEDSQUAREBRACKET = 'CLOSEDSQUAREBRACKET'
STRING = 'STRING'
NUMBER = 'NUMBER'
BOOLEAN = 'BOOLEAN'
NULL = 'NULL'
OPERATOR = 'OPERATOR'
SEPARATOR = 'SEPARATOR'

class JSONParser:
    def __init__(self, tokens):
        self.tokens = []
        for token in tokens:
            quote = token.index('"')
            space = token.rfind(" ")
            token_value = token[quote+1:space-2]
            token_type = token[space+1:-1]
            self.tokens.append((token_type, token_value))
        self.pos = 0
        self.message = ""

    def current_token(self):
        return self.tokens[self.pos]

    def eat(self, token_type):
        if self.current_token()[0] == token_type:
            self.pos += 1
        else:
            if self.message == "":
                self.message = "Invalid next token in sequence: " + str(self.current_token()[1]) + "\n" + \
                    "Expected " + str(token_type) + ", but found " + self.current_token()[0] + "\n" + \
                    "The given input is not a valid JSON file."

    def parse(self, tokens, print_output=True):
        ast = self.s()
        if self.pos != len(tokens):
            if self.message == "":
                self.message = "Invalid next token in sequence: " + str(self.current_token()[1]) + "\n" + \
                    "Expected $, but found " + self.current_token()[0] + "\n" + \
                    "The given input is not a valid JSON file."
        if self.message != "":
            if print_output:
                print(self.message)
            return self.message
        return ast

    def s(self):
        """S → {} | [] | {A} | [C]"""
        token_type = self.current_token()[0]
        if token_type == "OPENCURLYBRACKET":
            self.eat(OPENCURLYBRACKET)
            if self.current_token()[0] == "CLOSEDCURLYBRACKET":
                self.eat(CLOSEDCURLYBRACKET)
                return ObjectNode()
            else:
                obj = ObjectNode(self.a())
                self.eat(CLOSEDCURLYBRACKET)
                return obj
        elif token_type == "OPENSQUAREBRACKET":
            self.eat(OPENSQUAREBRACKET)
            if self.current_token()[0] == "CLOSEDSQUAREBRACKET":
                self.eat(CLOSEDSQUAREBRACKET)
                return ArrayNode()
            else:
                arr = ArrayNode(self.d())
                if self.current_token()[0] != 'CLOSEDSQUAREBRACKET':
                    if self.message == "":
                        self.message = "Invalid next token in sequence: " + str(self.current_token()[1]) + "\n" + \
                            "Expected CLOSEDSQUAREBRACKET, but found " + self.current_token()[0] + "\n" \
                            "The given input is not a valid JSON file."
                self.eat(CLOSEDSQUAREBRACKET)
                return arr
        else:
            if self.message == "":
                self.message = "Invalid next token in sequence: " + str(self.current_token()[1]) + "\n" + \
                    "Expected OPENCURLYBRACKET or OPENSQUAREBRACKET, but found " + self.current_token()[0] + "\n" + \
                    "The given input is not a valid JSON file."

    def a(self):
        """A → <STRING>:B | <STRING>:B, A"""
        pairs = [self.pair()]
        while self.current_token()[0] == "SEPARATOR":
            self.eat(SEPARATOR)
            if self.current_token()[0] != "STRING":
                if self.message == "":
                    self.message = "Invalid next token in sequence: " + str(self.current_token()[1]) + "\n" + \
                        "Expected STRING, but found " + self.current_token()[0] + "\n" + \
                        "The given input is not a valid JSON file."
            pairs.append(self.pair())

        if self.current_token()[0] not in ['CLOSEDCURLYBRACKET', 'SEPARATOR']:
            if self.message == "":
                self.message = "Invalid next token in sequence: " + str(self.current_token()[1]) + "\n" + \
                        "Expected SEPARATOR or CLOSEDCURLYBRACKET, but found " + self.current_token()[0] + "\n" + \
                        "The given input is not a valid JSON file."
        return pairs

    def pair(self):
        """<STRING>:B"""
        if self.current_token()[0] != STRING:
            if self.message == "":
                self.message = "Invalid next token in sequence: " + str(self.current_token()[1]) + "\n" + \
                    "Expected STRING, but found " + self.current_token()[0] + "\n" + \
                    "The given input is not a valid JSON file."
        key = self.current_token()[1]  # Assuming the token is (STRING, value)
        self.eat(STRING)
        if self.current_token()[0] != OPERATOR:
            if self.message == "":
                self.message = "Invalid next token in sequence: " + str(self.current_token()[1]) + "\n" + \
                    "Expected OPERATOR, but found " + self.current_token()[0] + "\n" + \
                    "The given input is not a valid JSON file."
        self.eat(OPERATOR)
        value = self.b()
        return PairNode(key, value)

    def b(self):
        """B → S | C"""
        token_type = self.current_token()[0]
        if self.current_token()[0] == "OPENCURLYBRACKET" or self.current_token()[0] == "OPENSQUAREBRACKET":
            return self.s()
        elif token_type == "STRING":
            value = self.current_token()[1]
            self.eat(STRING)
            return ValueNode(value, STRING)
        elif token_type == "NUMBER":
            value = self.current_token()[1]
            self.eat(NUMBER)
            return ValueNode(value, NUMBER)
        elif token_type == "BOOLEAN":
            value = self.current_token()[1]
            self.eat(BOOLEAN)
            return ValueNode(value, BOOLEAN)
        elif token_type == "NULL":
            self.eat(NULL)
            return ValueNode("null", NULL)
        else:
            if self.message == "":
                self.message = "Invalid next token in sequence: " + str(self.current_token()[1]) + "\n" + \
                    "Expected OPENCURLYBRACKET, OPENSQUAREBRACKET, STRING, NUMBER, BOOLEAN, or NULL, but found " + self.current_token()[0] + \
                    "The given input is not a valid JSON file."

    def d(self):
        # This was originally D but we consolidated the grammar, so it became C
        """C → B,C | B"""
        elements = [self.b()]
        while self.current_token()[0] == "SEPARATOR":
            self.eat(SEPARATOR)
            elements.append(self.b())
        return elements


if __name__ == "__main__":
    path = "./test_cases"
    file_num = 0
    print("Running JSON test cases in order: \n")

    files = sorted(
        [file for file in os.listdir(path) if file.endswith(".json")],
        key=lambda x: int(x.split('case')[-1].split('.')[0])
    )
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(path, file)
            file_num += 1
            print("Test " + str(file_num)+":")
            with open(file_path, 'r') as json_file:
                data = json_file.read()
                tokens = lex.tokenize(data, print_output=False)

                #print(tokens)

                if tokens is None:
                    print("Input failed lexical analysis. Syntactical analysis not performed.")

                if tokens is not None:
                    parser = JSONParser(tokens)
                    ast = parser.parse(tokens)

                    if type(ast) != str:
                        ast.print_tree()
                print("\n")
