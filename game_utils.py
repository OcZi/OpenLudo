import math

from art import *
import term_utils

surrender_messages = ["Pipipi", "Nimodo", "Se asume", "Se repite progra con yarasca"]

dado_moves = ["fuerte", "normal", "debil"]

bonuses = [14, 8]

meta = 20


def input_option(length: int, index: bool = False):
    num = 0
    arg_input = ""
    while len(arg_input) == 0:
        arg_input = ginput("   :")
        if arg_input.isnumeric():
            if 1 <= (num := int(arg_input)) <= length:
                break
    if index:
        num -= 1
    return num


def spaces(num: int = 1):
    for i in range(num):
        print("")


def screen_spaces(num: float = 5):
    spaces(math.ceil(term_utils.row_size() / num))


def gprint(text: str = ""):
    print(gcenter(text))


def gprint_art(text: str = ""):
    spacing = " " * math.ceil(term_utils.column_size() / 3)
    art_text = text2art(spacing + text)
    print(art_text)


def gcenter(text: str):
    return text.center(term_utils.column_size())


def option_format(i, text):
    return f"{i + 1}. {text}"


def gprint_list(elements: list, to_str=option_format):
    lines = []
    text_length = 0
    for i in range(len(elements)):
        elem = elements[i]
        line_text = to_str(i, elem)
        if len(line_text) > text_length:
            text_length = len(line_text)
        lines.append(line_text)

    for text in lines:
        align_suffix = (" " * (text_length - len(text)))
        gprint(text + align_suffix)


def ginput(text):
    spacing = " " * math.ceil(term_utils.column_size() / 3)
    return input(spacing + text)
