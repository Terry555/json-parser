import os
import lexical_analyzer as lex
import syntactic_analyzer as syn

def assign_meaning(node):
    new_structure = ""
    if type(node) == syn.ObjectNode:
        new_structure = {}
        for item in node.items:
            new_structure[assign_meaning(item.key)] = assign_meaning(item.value)
    if type(node) == syn.ArrayNode:
        new_structure = []
        for element in node.elements:
            new_structure.append(assign_meaning(element))
    if type(node) == syn.ValueNode:
        if node.type == "BOOLEAN":
            if node.value == 'false':
                return False
            if node.value == "true":
                return True
        if node.type == "NULL":
            return None
        if node.type == "NUMBER":
            if "." in node.value:
                return float(node.value)
            return int(node.value)
        if node.type == "STRING":
            value = node.value
            if '\\"' in value:
                value = value.replace('\\"', '"')
            if '\\n' in value:
                value = value.replace('\\n', '\n')
            if '\\r' in value:
                value = value.replace('\\r', '\r')
            if '\\t' in value:
                value = value.replace('\\t', '\t')
            if '\\f' in value:
                value = value.replace('\\f', '\f')
            if '\\b' in value:
                value = value.replace('\\b', '\b')
            while "\\\\" in value:
                value = value.replace("\\\\", "\\")
            return value
        
    if type(node) == str:
        value = node
        if '\\"' in value:
            value = value.replace('\\"', '"')
        if '\\n' in value:
            value = value.replace('\\n', '\n')
        if '\\r' in value:
            value = value.replace('\\r', '\r')
        if '\\t' in value:
            value = value.replace('\\t', '\t')
        if '\\f' in value:
            value = value.replace('\\f', '\f')
        if '\\b' in value:
            value = value.replace('\\b', '\b')
        while "\\\\" in value:
            value = value.replace("\\\\", "\\")
        return value
    return new_structure


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

                if tokens is None:
                    print("Input failed lexical analysis. Syntactical analysis not performed.")

                if tokens is not None:
                    parser = syn.JSONParser(tokens)
                    ast = parser.parse(tokens, print_output=False)

                    if type(ast) == str:
                        print("Input failed syntactic analysis. Semantic analysis not performed.")
                    else:
                        meaning = assign_meaning(ast)
                        print(meaning)
                        # Here we can see the result of this method.
                print("\n")