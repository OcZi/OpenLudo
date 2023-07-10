dado_moves = ["fuerte", "normal", "debil"]

bonuses = [14, 8]

meta = 20


def input_option(length: int, index: bool = False):
    num = 0
    arg_input = ""
    while len(arg_input) == 0:
        arg_input = input("   :")
        if arg_input.isnumeric():
            if 1 <= (num := int(arg_input)) <= length:
                break
    if index:
        num -= 1
    return num
