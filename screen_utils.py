import os


def pause():
    """
    Pause console screen for an input.
    :return: None
    """
    print("")
    input("Presiona ENTER para continuar.")
    clear()


def clear():
    """
    Clear console screen (adapted to windows/posix systems).
    :return: None
    """
    if os.name == "posix":
        command = "clear"
    else:
        command = "cls"
    os.system(command)
