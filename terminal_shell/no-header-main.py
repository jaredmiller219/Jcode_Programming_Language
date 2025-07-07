import os
import sys
from helpers import * 
import commands


def handle_clear():
    global just_cleared
    os.system("cls" if os.name == "nt" else "clear")
    just_cleared = True


def shell_script() -> bool:
    global just_cleared

    current_dir = os.getcwd()
    folder_icon = get_folder_icon(current_dir)
    if just_cleared:
        print(folder_icon + " " + current_dir)
        just_cleared = False
    else: 
        print("\n" + folder_icon + " " + current_dir)

    user_input = input("JCode> ").strip()
    if not user_input: return True

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
        "mkdir": commands.handle_mkdir,
        "md": commands.handle_mkdir,
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
        if command in ["list", "ls", "cd", "mkdir", "md", \
             "cat", "ct", "rm", "edit", "runfile"]: func(argument)
        elif command in ["exit", "quit", "qt"]: return False
        else: func()
    else:
        commands.handle_unknown(command)
    return True


def main():
    try:
        while True:
            if not shell_script(): break
    except KeyboardInterrupt:
        # Move to start of line, clear line
        sys.stdout.write('\r\033[6C' + ' ' * 10 + '\r\033[6C')
        sys.stdout.flush()
        print("\nExiting JCode Editor.")


if __name__ == "__main__":
    handle_clear()
    main()
