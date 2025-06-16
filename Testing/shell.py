import readline
import basic
import os

_ = readline  # mark as used to silence Pyright

def clear_screen():
    """Clears the terminal screen based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')


def is_clear_command(text):
    """
    Returns True if the user input is a command to clear the screen.

    Args:
        text (str): The user input string.

    Returns:
        bool: True if input is "clear" (case-insensitive), else False.
    """
    return text.lower() == "clear" or text.lower() == "cl"


def is_assignment(text):
    """
    Detects if the input is a variable assignment, e.g., 'var x = 3'.

    Args:
        text (str): The input string.

    Returns:
        bool: True if it's an assignment statement.
    """
    return text.strip().lower().startswith("var ")


def is_falsey_literal(text):
    """
    Returns True if the user input is "0" or "false" (case-insensitive).

    Args:
        text (str): The user input string.

    Returns:
        bool: True if input is considered falsy.
    """
    return text == "0" or text.lower() == "false"


def is_literal_number(text):
    """
    Returns True if the input is a standalone numeric literal (e.g., "2", "3.14").

    Args:
        text (str): The input string.

    Returns:
        bool: True if the input is a raw number literal.
    """
    try:
        float(text)
        return True
    except ValueError:
        return False


def is_number_zero(value):
    """
    Determines whether a given value is a Number object representing 0/null.

    Args:
        value: An object that may be a Number type with a 'value' attribute.

    Returns:
        bool: True if value is of type "Number" and its value is 0.
    """

    value_attr = getattr(value, "value", None)
    return type(value).__name__ == "Number" and value_attr == 0


def filter_non_null_elements(elements):
    """
    Filters out elements that are Number objects with value 0.

    Args:
        elements (list): List of objects, possibly Number instances.

    Returns:
        list: Filtered list excluding Number.null (value 0).
    """
    return [element for element in elements if not is_number_zero(element)]


def handle_result(result):
    """
    Processes the result of evaluation and prints appropriate output.

    - If result is a list of elements, filters and prints.
    - If result is a Number zero, does nothing.
    - Otherwise, prints the result.

    Args:
        result: Result object returned by the `basic.run` function.
    """
    if hasattr(result, "elements"):
        non_null = filter_non_null_elements(result.elements)
        print_elements(non_null)
    elif not is_number_zero(result):
        print(repr(result))


def print_elements(elements):
    """
    Prints filtered elements based on length:

    - One element: prints directly.
    - More than one: prints the list.

    Args:
        elements (list): Filtered list of non-null elements.
    """
    if len(elements) == 1:
        print(repr(elements[0]))
    elif elements:
        print(repr(elements))


def run_shell():
    """
    Runs the interactive BASIC shell.

    - Handles clear screen and falsy literals.
    - Suppresses output for assignment expressions.
    - Evaluates input using `basic.run`.
    - Gracefully exits on Ctrl+C or EOF.
    """
    while True:
        try:
            text = input('Shell > ').strip()
            if not text:
                continue
            if is_clear_command(text):
                clear_screen()
                continue
            if is_falsey_literal(text):
                print(0)
                continue

            result, error = basic.run('<stdin>', text)

            if error:
                print(error.as_string())
            elif result:
                if is_assignment(text) or is_literal_number(text):
                    continue
                handle_result(result)

        except (KeyboardInterrupt, EOFError):
            print("\nShell terminated.")
            break


if __name__ == "__main__":
    run_shell()
