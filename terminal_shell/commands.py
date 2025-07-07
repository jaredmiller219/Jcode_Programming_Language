import os
from helpers import (
    open_folder_icon, closed_folder_icon,
    collect_multiline_input, write_to_file,
    resolve_filename, read_file_content, build_editor_app,
)

def handle_help() -> None:
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

def handle_save() -> None:
    filename = input("Enter filename to save: ")
    print("Enter your content. Type 'eof' on a new line to finish.")
    lines = collect_multiline_input()
    write_to_file(filename, "\n".join(lines))
    print(f"File '{filename}' saved successfully!")

def handle_load() -> None:
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

def handle_edit(filename: str = None) -> None:
    filepath = resolve_filename(filename)
    if not os.path.exists(filepath):
        print(f"File '{filepath}' does not exist. Cannot edit.")
        return

    content = read_file_content(filepath)
    app = build_editor_app(filepath, content)
    result = app.run()
    print(result)

def handle_cd(path: str = None) -> None:
    if not path:
        print(f"Current directory: {os.getcwd()}")
        return
    try:
        os.chdir(os.path.expanduser(path))
        print(f"Changed directory to {os.getcwd()}")
    except Exception as e:
        print(f"Error: {e}")

def handle_ls(path: str = None) -> None:
    try:
        target_directory = os.path.expanduser(path) if path else os.getcwd()
        all_entries = os.listdir(target_directory)
        visible_entries = [f for f in all_entries if not f.startswith('.')]

        directories = [d for d in visible_entries if os.path.isdir(os.path.join(target_directory, d))]
        files = [f for f in visible_entries if os.path.isfile(os.path.join(target_directory, f))]

        folder_label = os.path.basename(target_directory) or target_directory
        if path is None and not os.path.isabs(folder_label):
            folder_label = f"./{folder_label}"

        combined_entries = directories + files

        if combined_entries:
            print("==============================")
            print(f"Directory: {folder_label}")
            print("==============================")
            max_len = max(len(name) for name in combined_entries) + 2
            columns = 3
            for i, name in enumerate(combined_entries, 1):
                print(f"{name:<{max_len}}", end="")
                if i % columns == 0:
                    print()
            if len(combined_entries) % columns != 0:
                print()
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
    if not filename:
        print("No filename provided.")
        return
    try:
        with open(os.path.expanduser(filename), "r") as f:
            print(f.read())
    except Exception as e:
        print(f"Error reading file: {e}")

def handle_rm(filename: str = None) -> None:
    if not filename:
        print("No filename provided.")
        return
    try:
        os.remove(os.path.expanduser(filename))
        print(f"File '{filename}' removed.")
    except Exception as e:
        print(f"Error: {e}")

def handle_runfile(filename: str = None) -> None:
    if not filename:
        filename = input("Enter Python script filename to run: ")
    try:
        with open(os.path.expanduser(filename), "r") as f:
            code = f.read()
        exec(code, {})
    except Exception as e:
        print(f"Error running file: {e}")

def handle_run() -> None:
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

def handle_pwd() -> None:
    print(os.getcwd())

def handle_exit() -> None:
    print("Ending current session.")

def handle_unknown(command: str) -> None:
    print(f"Unknown command: {command}")
