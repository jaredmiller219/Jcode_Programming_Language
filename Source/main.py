#######################################
# RUN
#######################################

import sys
import os

from symbol_table import *
from values import *
from parser import *
from interpreter import *
from lexer import *

global_symbol_table = SymbolTable()

builtins = {
    "null":        Number.null,
    "false":       Number.false,
    "true":        Number.true,
    "math_pi":     Number.math_PI,
    "print":       BuiltInFunction.print,
    "print_ret":   BuiltInFunction.print_ret,
    "input":       BuiltInFunction.input,
    "input_int":   BuiltInFunction.input_int,
    "clear":       BuiltInFunction.clear,
    "cls":         BuiltInFunction.clear,
    "is_num":      BuiltInFunction.is_number,
    "is_str":      BuiltInFunction.is_string,
    "is_list":     BuiltInFunction.is_list,
    "is_fun":      BuiltInFunction.is_function,
    "append":      BuiltInFunction.append,
    "pop":         BuiltInFunction.pop,
    "extend":      BuiltInFunction.extend,
    "len":         BuiltInFunction.len,
    "run":         BuiltInFunction.run,
}

for name, value in builtins.items():
    global_symbol_table.set(name, value)

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.Tokenize()
    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = Interpreter().visit(ast.node, context)

    return result.value, result.error

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python3 {os.path.basename(__file__)} <file.jc>")
        sys.exit(1)

    filename = sys.argv[1]

    if not os.path.isfile(filename):
        print(f"File not found: {filename}")
        sys.exit(1)

    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    value, error = run(filename, text)

    if error:
        print(error.as_string() if hasattr(error, 'as_string') else str(error))
        sys.exit(1)

if __name__ == "__main__":
    main()
