import os
import pyfiglet

from prompt_toolkit import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import TextArea, Frame
from prompt_toolkit.key_binding import KeyBindings

###############################
# Global variables
###############################
just_cleared = False
open_folder_icon = "\U0001F4C2"
closed_folder_icon = "\U0001F4C1"

###############################
# Art & Welcome
###############################
def print_art() -> None:
    """
    Prints the ASCII art title using pyfiglet.
    """
    art = pyfiglet.figlet_format("JCode Editor")
    print(art, end="")

def welcome_message() -> None:
    """
    Displays the welcome banner and instructions.
    """
    print_art()
    print("Welcome to the JCode Editor!")
    print('Tip: Type "help" to list available commands.')

###############################
# Help and Screen Utilities
###############################

def handle_help() -> None:
    """
    Prints help instructions for the editor commands.
    """
    print("=" * 40)
    print("JCode Editor Help")
    print("=" * 40)
    print("Basic commands:")
    print("  help       Show this help message")
    print("  exit       Exit the editor")
    print("  clear      Clear the screen")
    print("  pwd        Show current directory")
    print("  ls [dir]   List files in a directory")
    print("  cd [dir]   Change directory")
    print("  cat FILE   Display contents of a file")
    print("  rm FILE    Remove a file")
    print()
    print("File operations:")
    print("  save       Save content to a new file")
    print("  load       Load and display a file")
    print("  edit FILE  Edit a file in full-screen editor")
    print()
    print("Python execution:")
    print("  run        Run one line of Python code")
    print("  runfile    Run a Python script from a file")
    print()
    print("Shortcuts:")
    print("  cl, cls    Clear the screen")
    print("  ct         Alias for cat")
    print("=" * 40)


def handle_clear():
    """
    Clears the terminal screen and sets the just_cleared flag.
    """
    global just_cleared
    os.system("cls" if os.name == "nt" else "clear")
    just_cleared = True

###############################
# File Handling
###############################

def handle_save() -> None:
    """
    Save user input to a new file.
    """
    filename = input("Enter filename to save: ")
    print("Enter your content. Type 'EOF' on a new line to finish.")

    lines = collect_multiline_input()
    write_to_file(filename, "\n".join(lines))
    print(f"File '{filename}' saved successfully!")

def collect_multiline_input() -> list[str]:
    """
    Collects multiple lines of user input until 'EOF' is entered.
    """
    lines = []
    while True:
        line = input()
        if line.strip() == "EOF":
            break
        lines.append(line)
    return lines

def write_to_file(filename: str, content: str) -> None:
    """
    Writes content to a specified file.
    """
    try:
        with open(filename, "w") as f:
            f.write(content)
    except Exception as e:
        print(f"Error saving file: {e}")

def handle_load() -> None:
    """
    Loads and displays a file's content.
    """
    filename = input("Enter filename to load: ")
    try:
        with open(filename, "r") as f:
            content = f.read()
        print("-" * 20)
        print(content)
        print("-" * 20)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"Error loading file: {e}")

###############################
# Full-Screen Editor
###############################

def handle_edit(filename: str = None) -> None:
    """
    Opens a full-screen editor for the specified file.
    """
    filepath = resolve_filename(filename)
    content = read_file_content(filepath)

    app = build_editor_app(filepath, content)
    result = app.run()
    print(result)

def resolve_filename(filename: str) -> str:
    """
    Resolves or prompts for a filename and returns expanded path.
    """
    if not filename:
        filename = input("Enter filename to edit: ")
    return os.path.expanduser(filename)

def read_file_content(filepath: str) -> str:
    """
    Reads file content if it exists, otherwise returns an empty string.
    """
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return f.read()
    return ""

def build_editor_app(filepath: str, content: str) -> Application:
    """
    Builds a prompt_toolkit Application for editing content.
    """
    text_area = TextArea(text=content, scrollbar=True, line_numbers=True)

    kb = KeyBindings()

    @kb.add("c-s")
    def save_and_exit(event):
        """
        Save and exit on Ctrl+S.
        """
        with open(filepath, "w") as f:
            f.write(text_area.text)
        event.app.exit(result="Saved")

    @kb.add("c-q")
    def quit_without_saving(event):
        """
        Quit without saving on Ctrl+Q.
        """
        event.app.exit(result="Quit without saving")

    frame = Frame(
        text_area,
        title=f"Editing: {os.path.basename(filepath)} (Ctrl+S to save, Ctrl+Q to quit)",
        style="class:frame",
    )

    layout = Layout(frame)
    return Application(layout=layout, key_bindings=kb, full_screen=True)

###############################
# Directory & File Commands
###############################

def handle_cd(path: str = None) -> None:
    """
    Changes the current working directory.
    """
    if not path:
        print(f"Current directory: {os.getcwd()}")
        return
    try:
        os.chdir(os.path.expanduser(path))
        print(f"Changed directory to {os.getcwd()}")
    except Exception as e:
        print(f"Error: {e}")

def handle_ls(path: str = None) -> None:
    """
    List non-hidden files in the specified directory or current working directory if none given.
    Prints directory label and files inside it in 3 columns.
    Shows a closed folder icon (Unicode) if the directory is empty.
    Hidden files (starting with '.') are excluded.
    Handles errors gracefully.
    
    Args:
        path (str, optional): Directory path to list files from. Defaults to None (current directory).
    """
    try:
        target_directory = os.path.expanduser(path) if path else os.getcwd()
        
        # Filter out hidden files and directories (those starting with '.')
        all_entries = os.listdir(target_directory)
        visible_entries = [f for f in all_entries if not f.startswith('.')]

        # Separate directories and files
        directories = [d for d in visible_entries if os.path.isdir(os.path.join(target_directory, d))]
        files = [f for f in visible_entries if os.path.isfile(os.path.join(target_directory, f))]

        folder_label = os.path.basename(target_directory)
        if not folder_label:
            folder_label = target_directory
        
        if path is None and not os.path.isabs(folder_label):
            folder_label = f"./{folder_label}"

        combined_entries = directories + files

        if combined_entries:
            print(f"Directory: {folder_label}")
            # Determine max width for column formatting
            max_len = max(len(name) for name in combined_entries) + 2  # padding
            columns = 3

            for i, name in enumerate(combined_entries, 1):
                print(f"{name:<{max_len}}", end="")
                if i % columns == 0:
                    print()  # new line every 3 entries
            if len(combined_entries) % columns != 0:
                print()  # ensure ending with newline
        else:
            print(f"{closed_folder_icon} {folder_label} (empty)")
    
    except FileNotFoundError:
        print(f"Directory '{path}' not found.")
    except NotADirectoryError:
        print(f"'{path}' is not a directory.")
    except PermissionError:
        print(f"Permission denied to access '{path}'.")
    except Exception as error:
        print(f"Error listing files: {error}")

def handle_cat(filename: str = None) -> None:
    """
    Displays contents of a file.
    """
    if not filename:
        print("No filename provided.")
        return
    try:
        with open(os.path.expanduser(filename), "r") as f:
            print(f.read())
    except Exception as e:
        print(f"Error reading file: {e}")

def handle_rm(filename: str = None) -> None:
    """
    Removes a specified file.
    """
    if not filename:
        print("No filename provided.")
        return
    try:
        os.remove(os.path.expanduser(filename))
        print(f"File '{filename}' removed.")
    except Exception as e:
        print(f"Error: {e}")

###############################
# Python Execution
###############################

def handle_runfile(filename: str = None) -> None:
    """
    Executes a Python script from a file.
    """
    if not filename:
        filename = input("Enter Python script filename to run: ")
    try:
        with open(os.path.expanduser(filename), "r") as f:
            code = f.read()
        exec(code, {})
    except Exception as e:
        print(f"Error running file: {e}")

def handle_run() -> None:
    """
    Executes a line of Python code input by the user.
    """
    code = input("Enter Python code to run: ")
    try:
        result = eval(code)
        print(f"Result: {result}")
    except SyntaxError:
        try:
            exec(code)
        except Exception as e:
            print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

###############################
# Other Utilities
###############################

def handle_pwd() -> None:
    """
    Prints the current working directory.
    """
    print(os.getcwd())

def handle_exit() -> None:
    """
    Prints exit message.
    """
    print("Ending current session.")

def handle_unknown(command: str) -> None:
    """
    Handles unknown commands.
    """
    print(f"Unknown command: {command}")

#############################
# Shell
###############################

def shell_script() -> bool:
    """
    Main shell loop handler.
    Returns False to exit, True to continue.
    """
    global just_cleared

    # Print newline only if screen was NOT just cleared
    if not just_cleared: print()  # normal newline before prompt
    else:
        just_cleared = False  # reset flag, skip newline once

    print(open_folder_icon + " " + os.getcwd())

    user_input = input("JCode> ").strip()
    if not user_input:
        return True

    parts = user_input.split(maxsplit=1)
    command = parts[0].lower()
    argument = parts[1] if len(parts) > 1 else None

    # Command-function mapping
    commands = {
        "help": handle_help,
        "exit": handle_exit,
        "quit": handle_exit,
        "qt": handle_exit,
        "run": handle_run,
        "save": handle_save,
        "load": handle_load,
        "list": handle_ls,
        "ls": handle_ls,
        "cd": handle_cd,
        "pwd": handle_pwd,
        "cat": handle_cat,
        "ct": handle_cat,
        "rm": handle_rm,
        "edit": handle_edit,
        "runfile": handle_runfile,
    }

    # Clear aliases
    if command in ["clear", "cl", "cls"]:
        handle_clear()
        return True

    # Handle known commands
    if command in commands:
        func = commands[command]
        # Commands that take an argument
        if command in ["list", "ls", "cd", "cat", "ct", "rm", "edit", "runfile"]:
            func(argument)
        else:
            func()
        # Check if exit was called
        if command in ["exit", "quit", "qt"]:
            return False
    else:
        handle_unknown(command)

    return True

#############################
# Main Entry Point
###############################

def main() -> None:
    """
    Main entry point for the application.
    Initializes the welcome message and starts the shell loop.
    """
    welcome_message()
    try:
        while True:
            should_continue = shell_script()
            if not should_continue:
                break
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt: Exiting JCode Editor.")

#############################
# Run the program
###############################

if __name__ == "__main__":
    main()