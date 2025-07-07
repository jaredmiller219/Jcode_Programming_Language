import os
import pyfiglet

from prompt_toolkit import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import TextArea, Frame
from prompt_toolkit.key_binding import KeyBindings

just_cleared = False
open_folder_icon = "\U0001F4C2"
closed_folder_icon = "\U0001F4C1"


def print_art():
    art = pyfiglet.figlet_format("JCode Editor")
    print(art, end="")


def welcome_message():
    print_art()
    print("Welcome to the JCode Editor!")
    print('Tip: Type "help" to list available commands.\n')


def get_folder_icon(path: str) -> str:
    """
    Returns closed folder icon if the directory is empty, open icon otherwise.
    Hidden files are ignored.
    """
    try:
        all_entries = os.listdir(path)
        visible_entries = [f for f in all_entries if not f.startswith('.')]
        if visible_entries:
            return open_folder_icon
        else:
            return closed_folder_icon
    except Exception:
        # If can't access directory, default to closed
        return closed_folder_icon


def collect_multiline_input() -> list[str]:
    lines = []
    while True:
        line = input()
        if line.strip().lower() == "eof": break
        lines.append(line)
    return lines


def write_to_file(filename: str, content: str):
    try:
        with open(filename, "w") as file_to_write:
            file_to_write.write(content)
    except Exception as exception:
        print(f"Error saving file: {exception}")


def resolve_filename(filename: str) -> str:
    if not filename: filename = input("Enter filename to edit: ")
    return os.path.expanduser(filename)


def read_file_content(filepath: str) -> str:
    if os.path.exists(filepath):
        with open(filepath, "r") as file_to_read: return file_to_read.read()
    return ""


def build_editor_app(filepath: str, content: str) -> Application:
    text_area = TextArea(text=content, scrollbar=True, line_numbers=True)
    keybindings = KeyBindings()

    @keybindings.add("c-s")
    def save_and_exit(event):
        with open(filepath, "w") as f:
            f.write(text_area.text)
        event.app.exit(result="Saved")

    @keybindings.add("c-q")
    def quit_without_saving(event):
        event.app.exit(result="Quit without saving")

    frame = Frame(
        text_area,
        title=f"Editing: {os.path.basename(filepath)} (Ctrl+S to save, Ctrl+Q to quit)",
        style="class:frame",
    )
    layout = Layout(frame)
    return Application(layout=layout, key_bindings=keybindings, full_screen=True)
