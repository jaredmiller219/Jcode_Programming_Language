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
    interpreter = Interpreter()
    result = interpreter.visit(ast.node, context)

    if result.error:
        return None, result.error

    # Check if this is a .jcode file (not the REPL or a code snippet)
    is_jcode_file = fn.endswith('.jcode') or fn.endswith('.jc')

    # Check if there's a main function defined
    main_function = context.symbol_table.get('main')
    if main_function and isinstance(main_function, Function):
        # Execute the main function with no arguments
        result = main_function.execute([], Position(0, 0, 0, fn, text))
        return result.value, result.error
    elif is_jcode_file:
        # Return an error if no main function is found in a .jcode file
        return None, RuntimeError(
            Position(0, 0, 0, fn, text),
            Position(0, 0, 0, fn, text),
            "No 'main' function found. Every JCode program must have a 'main' function.",
            context
        )

    # For REPL or non-.jcode files, return the result without requiring a main function
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
