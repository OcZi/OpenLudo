import random
from datetime import datetime

import database
import pdf
from game_utils import *
from screen_utils import *
from term_utils import title


def show_table(players: dict[str, int]):
    clear()
    screen_spaces()
    gprint("- Ludo Divertido -")
    lines = []
    for i in range(20, -1, -1):  # Tabla del 1 al 20
        if i == 0:
            line = f"  INICIO. "
        else:
            line = f"  {i}. "

        line_player = ""
        for player, position in players.items():
            if position != i:
                continue

            if len(line_player) > 0:
                line_player += "- "
            line_player += f"{player} "

        line += line_player
        if i in bonuses:
            line += "(BONUS) "
        if i == 20:
            line += "(META) "
        lines.append(line)
    gprint_list(lines, lambda index, text: text)
    gprint("-------------------")


def selected_random_move() -> int:
    while True:
        gprint("- Movimientos -")
        moves = dado_moves[:]
        moves.append("Rendirse [!]")
        gprint_list(moves)

        num = input_option(3, True)

        # Rendirse !?
        if num == 3:
            return -1
        return random_move(num)


def random_move(move_type: int) -> int:
    if move_type == 0:  # Fuerte
        return random.randint(4, 6)
    elif move_type == 1:  # Normal
        return random.randint(1, 6)
    else:  # Debil
        return random.randint(1, 3)


def welcome():
    screen_spaces()
    gprint_art(" -  LUDO  -")
    gprint()
    # Imprime todas las opciones

    gprint_list(options,
                lambda i, func_option: f"{i + 1}. {func_option.__name__.capitalize()}")
    gprint(" ")


def start():
    if database.user == ():
        clear()
        register()
        clear()

    """
    while True:
        gprint("")
        gprint("   -   Tipo de juego   -")
        gprint_list(["PvP", "CPU"])
        gprint("")
        cpu = input_option(2) == 2
        break
    gprint("")
    """

    screen_spaces()
    player_name1 = database.user[1]
    player_name2 = "CPU"

    players = {
        # Orden de entrada:
        # nombre : entrada
        player_name1: 0,
        player_name2: 0
    }

    movements = []
    count_turns = 1
    # 0 = turn for player 1
    # 1 = turn for player 2
    turn_for = 0
    while True:
        gprint("")
        show_table(players)
        gprint("")
        gprint(f"Turno {count_turns}:")
        count_turns += 1
        pause()

        winner = turn_game(players, turn_for, movements)

        if winner is not None:
            pause()
            break
        else:
            # Switch turns
            turn_for = switch_turn(turn_for)

    if winner != "CPU":
        # Siempre será el primer jugador ahora
        database.update_user_wins()
        database.update_user_moves(movements[-5:])
        database.update_user()

    screen_spaces()
    gprint_art(f"{winner} Winner!")
    pause()


def turn_game(players: dict[str, int], turn_for: int, movements: list) -> str:
    # Literal python necesita convertir los valores y llaves a list
    # para poder acceder a ellos por index
    list_players = list(players.keys())
    player = list_players[turn_for]

    gprint("")
    gprint(f"Turno de {player}:")

    moves = 6
    bonus = False

    winner = None
    while moves == 6 or bonus:
        bonus = False
        gprint("")
        if player == "CPU":
            moves = random_move(random.randint(0, len(dado_moves) - 1))
        else:
            moves = selected_random_move()

        if moves == -1:
            winner = list_players[switch_turn(turn_for)]
            surrender()
            break

        gprint("")
        show_table(players)
        gprint("")
        gprint(f"{player} obtuvo el valor de {moves}!")
        movements.append(moves)

        players[player] += moves
        if players[player] == meta:
            winner = player
            break
        elif players[player] > meta:
            """
            Retroceder al player si sobrepasa meta
            Ejemplo: 
                Valores: positions[pos_index] = 21, meta = 20

                Debe retroceder a 19:
                    meta - (positions[pos_index] - meta)
                =   20 - (21 - 20) # la distancia entre player y meta
                =   20 - 1
                =   19
            """
            players[player] = meta - (players[player] - meta)

        # Me olvide de esto pipipi
        player2 = list_players[switch_turn(turn_for)]
        if players[player] == players[player2]:
            gprint(f"{player} ha devuelto a {player2} al inicio!")
            players[player2] = 0

        if players[player] in bonuses:
            bonus = True
            gprint(f"CASILLA BONUS EN {players[player]}!")
        if moves == 6:
            gprint("No pierde turno!")
        pause()
    return winner


def switch_turn(turn: int):
    return (turn + 1) % 2


def surrender():
    clear()
    screen_spaces()
    gprint("Se ha rendido!")
    gprint()
    message = surrender_messages[random.randint(0, len(surrender_messages) - 1)]
    gprint(message)


def record():
    clear()
    screen_spaces()
    gprint("- Records -")
    gprint_list(["Top ganadores", "Ganadores (mensuales)", "Regresar"])
    num = input_option(2)
    clear()
    screen_spaces()
    if num == 1:
        top_ganadores()
    elif num == 2:
        ganadores_mensuales()


def top_ganadores():
    gprint("- Top jugadores -")
    items = sorted(list(database.database.items())[:], key=lambda item: sum(item[1][3]), reverse=True)

    gprint_list(items, lambda i, data: f"{i + 1}. {data[1][0]}: {data[1][3]}")
    pause()


def ganadores_mensuales():
    gprint("- Ganadores mensuales -")
    items = sorted(list(database.database.items())[:], key=lambda item: to_timestamp(item[1][1]), reverse=True)

    gprint_list(items, lambda i, data: f"{i + 1} {data[1][0]}: {data[1][1]}")
    pause()


def to_timestamp(date: str):
    split = date.split("/")
    mm = split[1]
    return datetime(2000, int(mm), 1).timestamp()


def register():
    screen_spaces()
    gprint(" - Registrate - ")
    term_utils.switch_cursor()
    while len(name := ginput("Nombre: ")) == 0:
        continue
    while not database.is_valid_email(email := ginput("Correo electrónico: ")):
        continue
    while not database.is_valid_date(date := ginput("Fecha: ")):
        continue

    term_utils.switch_cursor()
    database.set_user(email, name, date)


def info():
    screen_spaces()
    gprint("- Búsqueda de jugadores -")
    gprint_list(["Buscar un jugador", "Regresar"])

    num = input_option(1)
    if num != 1:
        return

    clear()
    screen_spaces()
    gprint("- Datos -")
    while not database.is_valid_email(email := ginput("Correo del jugador: ")):
        continue

    if (user := database.get_user(email)) is None:
        gprint("No se ha encontrado al usuario con dicho correo!")
        pause()
        info()
        return

    clear()
    screen_spaces()
    gprint(f"- Información de {email} - ")
    gprint_list(user, text_for_data)
    gprint()
    convert_pdf = ginput("Convertir a pdf? :").lower()
    if convert_pdf in ["si", "true"]:
        lines = []
        for i in range(len(user)):
            lines.append(text_for_data(i, user[i]))
        pdf.lines_to_pdf(lines, email.replace(".", "_") + ".pdf")
    pause()


def text_for_data(i, data):
    if i == 0:
        return f"Nombre: {data}"
    elif i == 1:
        return f"Fecha: {data}"
    elif i == 2:
        return f"Victorias: {data}"
    elif i == 3:
        line = ""
        for move in data:
            if len(line) > 0:
                line += "-"
            line += str(move)
        return f"Movimientos: {line}"


def end():
    database.save()
    term_utils.close()
    exit(0)


options = [start, record, end, info]

# TODO: EMPIEZA AQUI!!!
# Bucle del programa para mantenerlo vivo

title("LUDO DIVERTIDO")

database.load()
term_utils.init()

while True:
    clear()
    welcome()
    selected = input_option(len(options), True)

    option = options[selected]
    clear()
    option()
    gprint()
    clear()
