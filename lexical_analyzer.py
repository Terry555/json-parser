

# Lexical Analysis
def tokenize(input_string):
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

                    i += 1
                token = '<"' + word + '", STRING>'
                print(string)
                print(i)
                print(string[i])

                while string[i] in [":", " "] and i<len(string)-1:
                    i += 1
                    if string[i] == ":":
                        token = '<"' + word + '", IDENTIFIER>'
                        break
                tokens.append(token)

            elif char == ":":
                tokens.append('<"' + char + '", OPERATOR>')
            elif char in "0123456789.":
                word = char
                while string[i] in "0123456789." and i<len(string)-1:
                    i += 1
                    word = word + string[i]
                tokens.append('<"' + word + '", NUMBER>')
            elif char == '[':
                tokens.append('<"[", OPENSQUAREBRACKET>')
            elif char == ']':
                tokens.append('<"]", CLOSEDSQUAREBRACKET>')
            elif char == "t" or char == "f" or char == "n":
                word = char
                while string[i] in "abcdefghijklmnopqrstuvwxyz" and i<len(string)-1:
                    i += 1
                    word = word + string[i]
                if word == "true" or word == "false":
                    tokens.append('<"' + word + '", BOOLEAN>')
                if word == "null":
                    tokens.append('<"' + word + '", NULL>')
            elif char == "}" or string[i] == "}":
                tokens.append('<"' + string[i] + '", CLOSEDCURLYBRACKET>')
            elif char == " " or char == "\n":
                i += 1
                continue
            else:
                print("Token not found: " + char)
                return
            i += 1
        if input_string.index(string) != len(input_string)-1:
            tokens.append('<",", SEPARATOR>')

        #print(values)
    for token in tokens:
        print(token)



if __name__ == "__main__":
    input = '{"type": "basket","beans": 47,"apples": 7,"oranges": null,"brand": "ConvertSimple","ratio": false, "descriptors": ["clean", "fresh", "juicy", "delicious" ]}'
    #print(input)
    tokenize(input)