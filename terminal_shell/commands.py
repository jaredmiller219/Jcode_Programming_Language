import os
from terminal_shell import helpers


def handle_help():
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


def handle_save():
    filename = input("Enter filename to save: ")
    print("Enter your content. Type 'eof' on a new line to finish.")
    lines = helpers.collect_multiline_input()
    helpers.write_to_file(filename, "\n".join(lines))
    print(f"File '{filename}' saved successfully!")


def handle_load():
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


def handle_edit(filename: str):
    filepath = helpers.resolve_filename(filename)
    if not os.path.exists(filepath):
        print(f"File '{filepath}' does not exist. Cannot edit.")
        return

    content = helpers.read_file_content(filepath)
    app = helpers.build_editor_app(filepath, content)
    result = app.run()
    print(result)


def handle_cd(path: str):
    if not path or path == '.':
        # print(f"Current directory: {os.getcwd()}")
        print("Please provide a valid path")
        return
    try:
        os.chdir(os.path.expanduser(path))
        print(f"Changed directory to {os.getcwd()}")
    except Exception as e:
        print(f"Error: {e}")


def handle_ls(path: str):
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
            print(f"{helpers.closed_folder_icon} {folder_label} (empty)")

    except FileNotFoundError:
        print(f"Directory '{path}' not found.")
    except NotADirectoryError:
        print(f"'{path}' is not a directory.")
    except PermissionError:
        print(f"Permission denied to access '{path}'.")
    except Exception as error:
        print(f"Error listing files: {error}")


def handle_cat(filename: str):
    if not filename:
        print("No filename provided.")
        return
    try:
        with open(os.path.expanduser(filename), "r") as f:
            print(f.read())
    except Exception as e:
        print(f"Error reading file: {e}")


def handle_rm(filename: str):
    if not filename:
        print("No filename provided.")
        return
    try:
        os.remove(os.path.expanduser(filename))
        print(f"File '{filename}' removed.")
    except Exception as e:
        print(f"Error: {e}")


def handle_runfile(filename: str):
    if not filename:
        filename = input("Enter Python script filename to run: ")
    try:
        with open(os.path.expanduser(filename), "r") as f:
            code = f.read()
        exec(code, {})
    except Exception as e:
        print(f"Error running file: {e}")


def handle_run():
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


def handle_pwd():
    print(os.getcwd())



def handle_mkdir(folder_name: str):
    """
    Creates a new directory with the specified name.
    
    Args:
        folder_name (str, optional): Name of the directory to create.
    """
    if not folder_name:
        print("No folder name provided.")
        return
    
    try:
        path = os.path.expanduser(folder_name)
        os.makedirs(path, exist_ok=False)
        print(f"Directory '{folder_name}' created.")
    except FileExistsError:
        print(f"Directory '{folder_name}' already exists.")
    except Exception as e:
        print(f"Error creating directory: {e}")


def handle_exit():
    print("Ending current session.")


def handle_unknown(command: str):
    print(f"Unknown command: {command}")
