# JSON-Parser

This is designed to take JSON files and parse them into tokens. 

## Table of Contents
- [Team Members](#team-members)
- [Features](#features)
- [Token Types](#token-types)
- [Grammar](#grammar)
- [Installation](#installation)

# Team Members

- Larry Davis lrd2139@columbia.edu
- Terry Foley tf2512@columbia.edu

## Features

- This is the beginning stages of what will be a JSON parser. As of now, the files "lexical_analyzer.py" and "syntactic_analyzer.py" accept any number of .json files as arguments, and will tokenize each file. The "lexical_analyzer.py" file will output each token according to the categories below, if all tokens are found to be valid. If it encounters an invalid token, it will display the sequence of characters that was unrecognized. The "syntactic_analyzer.py" file will output the proper Abstract Syntax Tree (AST) if a set of valid tokens is recognized by the grammar below. Otherwise, it will not produce an AST and instead display the token on which it halted and which token(s) it was expecting.

## Token Types

- String: '"' ( '\\' . | ~[\\"] )* '"'

![Number](images/string.png)
  
- Number: [0-9]+ ( '.' [0-9]* )? | '.' [0-9]+
  
![Number](images/number.png)
  
- Boolean: (true | false)
  
![Boolean](images/boolean.png)
  
- Null: null
  
![Null](images/null.png)
  
- Operator: ':'
  
![Operator](images/operator.png)
  
- Separator: (\, | \{ | \} | \[ | \])
  
![Separator](images/separator.png)
  
<!-- Identifiers will become the keys in key/value pairs in JS and Python, which will likely have
their own set of rules (eg. not starting with a number), but for this initial step we will treat all Identifiers
as Strings -->
<!-- - Example Identifier: '"' (^[A-Za-z_$][A-Za-z0-9_$]*$)|(^['"][^'"]*['"]$) '"' -->

## Grammar

S → {} | [] | {A} | [C]  
A → \<STRING\>:B | \<STRING\>:B, A  
B → S | \<STRING\> | \<NUMBER\> | \<BOOLEAN\> | \<NULL\>  
C → B,C | B

Terminals: '{', '}', '[', ']', ':', ',', '\<STRING\>', '\<NUMBER\>', '\<BOOLEAN\>', '\<NULL\>'  
'{': Opens a new JSON Object.  
'}': Closes a JSON Object.  
'[': Opens a new JSON Array.  
']': Closes a JSON Array.  
':': An operator that assigns string keys to datatype values.  
',': A separator that separates data types, key-value pairs, JSON Objects, or JSON Arrays.  
'\<STRING\>': A data type that represents a string.  
'\<NUMBER\>': A data type that represents a number of integer or decimal value.  
'\<BOOLEAN\>': A data type that represents a boolean value, represented by "True" or "False".  
'\<NULL\>': A data type that represents JSON's "null" value.  
  
Nonterminals: S, A, B, C  
S: Allows for a new JSON Object or Array.  
A: Ensures that the rules for a JSON Object are followed.  
B: Allows JSON Objects and Arrays to be populated with data types or new JSON Objects and Arrays.  
C: Ensures that the rules for a JSON Array are followed.  


## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:Terry555/json-parser.git
   If the user does not have python installed, detailed steps for installation are included in the shell script file "run_script.sh". 
2. Run the file "lexical_analyzer.py", which will output tokens and token types. 
3. Run the file "syntactic_analyzer.py", which will output an abstract syntax tree. 
