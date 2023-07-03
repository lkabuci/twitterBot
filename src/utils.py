import os


def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")
