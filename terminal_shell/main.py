import os
from helpers import just_cleared, open_folder_icon, closed_folder_icon, welcome_message
import commands

def handle_clear() -> None:
    global just_cleared
    os.system("cls" if os.name == "nt" else "clear")
    just_cleared = True

def shell_script() -> bool:
    global just_cleared

    if just_cleared:
        print(open_folder_icon + " " + os.getcwd())
        just_cleared = False
    else:
        print("\n" + open_folder_icon + " " + os.getcwd())

    user_input = input("JCode> ").strip()
    if not user_input:
        return True

    parts = user_input.split(maxsplit=1)
    command = parts[0].lower()
    argument = parts[1] if len(parts) > 1 else None

    commands_map = {
        "help": commands.handle_help,
        "exit": commands.handle_exit,
        "quit": commands.handle_exit,
        "qt": commands.handle_exit,
        "run": commands.handle_run,
        "save": commands.handle_save,
        "load": commands.handle_load,
        "list": commands.handle_ls,
        "ls": commands.handle_ls,
        "cd": commands.handle_cd,
        "pwd": commands.handle_pwd,
        "cat": commands.handle_cat,
        "ct": commands.handle_cat,
        "rm": commands.handle_rm,
        "edit": commands.handle_edit,
        "runfile": commands.handle_runfile,
    }

    if command in ["clear", "cl", "cls"]:
        handle_clear()
        return True

    if command in commands_map:
        func = commands_map[command]
        if command in ["list", "ls", "cd", "cat", "ct", "rm", "edit", "runfile"]:
            func(argument)
        else:
            func()
        if command in ["exit", "quit", "qt"]:
            return False
    else:
        commands.handle_unknown(command)

    return True

def main() -> None:
    welcome_message()
    try:
        while True:
            if not shell_script():
                break
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt: Exiting JCode Editor.")

if __name__ == "__main__":
    main()