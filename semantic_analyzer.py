import os
import lexical_analyzer as lex
import syntactic_analyzer as syn

def assign_meaning(tree):
    if type(tree) == syn.ObjectNode:
        print("hi")
        for item in tree.items:
            if type(item) == syn.PairNode:
                print(item.key, ":", item.value)

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
                    parser = syn.JSONParser(tokens)
                    ast = parser.parse(tokens, print_output=False)

                    if type(ast) == str:
                        print("Input failed syntactic analysis. Semantic analysis not performed.")
                    else:
                        assign_meaning(ast)
                print("\n")