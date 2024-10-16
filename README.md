# JSON-Parser

A brief description of JSON-Parser and its purpose.

## Table of Contents
- [Team Members](#teammembers)
- [Features](#features)
- [Token Types](#tokentypes)
- [Installation](#installation)

# Team Members

- Larry Davis lrd2139@columbia.edu
- Terry Foley tf2512@columbia.edu

## Features

- List the main features of your project.
- Highlight any important functionalities.

## Token Types

- Identifier: '"' [a-zA-Z_][a-zA-Z0-9]* '"'
- String: '"' ( '\\' . | ~[\\"] )* '"'
- Number: [0-9]+ ( '.' [0-9]+ )?
- Boolean: (true | false)
- Null: null
- Operator: ( [+\-*/%] | [<>=!]=? | (&&|\|\|) )
- Separator: (\, | \; | \{ | \} | \[ | \] | \( | \) )

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git