import asyncio
import cursor
import os

reset = '\033[0m'

loop = asyncio.get_event_loop()

frame_buffer = {}
fps_delay = 0.02


def title(text: str):
    os.system(f"Title {text}")


def clear_frame():
    frame_buffer.clear()


def set_char(x, y, letter):
    if y not in frame_buffer:
        frame_buffer[y] = {}
    frame_buffer[y][x] = letter


async def print_frame_buffer():
    await print_frame(frame_buffer, delay=fps_delay)


async def print_frame(characters: dict[int, dict[int, str]], delay: float = 0.01):
    terminal = os.get_terminal_size()

    for row in range(terminal.lines):
        line = ""
        for column in range(terminal.columns - 1):
            if (dict_x := characters.get(row)) is not None and (letter := dict_x.get(column)) is not None:
                line += letter
            else:
                line += " "
        print(line)
    await asyncio.sleep(delay)
    print(f'\033[{os.get_terminal_size().lines}\033[2K', end='')


def terminal_size():
    return os.get_terminal_size()


def column_size():
    return terminal_size().columns


def row_size():
    return terminal_size().lines


async def printing():
    frame = 0
    while frame < column_size():
        set_char(frame, row_size() // 2, "XD")
        if frame > 0:
            set_char(frame - 1, row_size() // 2, " ")
        frame += 1
        await print_frame_buffer()


def run_async(func):
    loop.run_until_complete(func)


def init():
    cursor.hide()


def close():
    loop.close()
    cursor.show()


title("LUDO DIVERTIDO")
init()
run_async(printing())
close()