import os

# Lexical Analysis
def tokenize(input_string, print_output=True):
    tokens = []
    input_string = input_string.split(",")
    for string in input_string:
        i = 0
        while i < len(string):
            char = string[i]
            if char == "{":
                tokens.append('<"' + char + '", OPENCURLYBRACKET>')
            elif char == "'" or char == '"':
                word = ""
                i += 1 
                while string[i] != char:
                    word = word + string[i]
                    if string[i] == "\\":
                        if string[i+1] == "\\" or string[i+1] == '"':
                            word = word + string[i] + string[i+1]
                            if i + 2 < len(string):
                                i += 2
                                continue
                            else:
                                break
                        else:
                            word = word + string[i]
                            i += 1
                            continue
                    i += 1
                    if i == len(string):
                        if print_output:
                            print("Token not found: " + '"' + word)
                            print("\n")
                        return
                token = '<"' + word + '", STRING>'
                tokens.append(token)
            elif char == ":":
                tokens.append('<"' + char + '", OPERATOR>')
            elif char in "0123456789.":
                word = char
                decimals = 0
                if char == ".":
                    decimals += 1
                while string[i] in "0123456789." and i<len(string)-1:
                    i += 1
                    if string[i] in "0123456789.":
                        word = word + string[i]
                    if string[i] == ".":
                        decimals += 1
                if decimals > 1 :
                    if print_output:
                        print("Token not found: " + word)
                        print("\n")
                    return
                tokens.append('<"' + word + '", NUMBER>')
                if string[i] not in "0123456789.":
                    i -= 1
            elif char == '[':
                tokens.append('<"[", OPENSQUAREBRACKET>')
            elif char == ']':
                tokens.append('<"]", CLOSEDSQUAREBRACKET>')
            elif char == "t" or char == "f" or char == "n":
                word = char
                while string[i] in "abcdefghijklmnopqrstuvwxyz" and i<len(string)-1:
                    i += 1
                    if string[i] not in [" ", "\n"]:
                        word = word + string[i]
                if word == "true" or word == "false":
                    tokens.append('<"' + word + '", BOOLEAN>')
                elif word == "null":
                    tokens.append('<"' + word + '", NULL>')
                else:
                    if print_output:
                        print("Token not found: " + word)
                        print("\n")
                    return
            elif char == "}" or string[i] == "}":
                tokens.append('<"' + string[i] + '", CLOSEDCURLYBRACKET>')
            elif char == " " or char == "\n":
                i += 1
                continue
            else:
                if print_output:
                    print("Token not found: " + char)
                    print("\n")
                return
            i += 1
        if input_string.index(string) != len(input_string)-1:
            tokens.append('<",", SEPARATOR>')

        #print(values)
    if print_output:
        for token in tokens:
            print(token)
        print("\n")
    return tokens



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
                tokens = tokenize(data)
