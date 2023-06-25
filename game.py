import os
import random


def int_input():
    arg_input = ""
    while len(arg_input) == 0 or not arg_input.isnumeric():
        arg_input = input("   :")
    return int(arg_input) - 1


def pause():
    print("")
    input("Presiona ENTER para continuar.")
    clear()


def clear():
    if os.name == "posix":
        command = "clear"
    else:
        command = "cls"
    os.system(command)


dado_moves = ["fuerte", "normal", "debil"]
bonuses = [14, 8]
meta = 20


def show_table(players: dict[str, int]):
    print("- Ludo Divertido -")
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
        print(line)
    print("-------------------")


def selected_random_move() -> int:
    while True:
        print("- Movimientos -")
        for i, move in enumerate(dado_moves):
            print(f"   {i + 1}. {move}")
        print("")

        num = int_input()
        if num < 0 or num > 2:
            continue

        return random_move(num)


def random_move(move_type: int) -> int:
    if move_type == 0:  # Fuerte
        return random.randint(4, 6)
    elif move_type == 1:  # Normal
        return random.randint(1, 6)
    else:  # Debil
        return random.randint(1, 3)


def welcome():
    print("   -  LUDO  -")
    # Imprime todas las opciones menos welcome (opción oculta)
    length = len(options) - 1
    for i in range(length):
        function_option = options[i]
        print(f"   {i + 1}. {function_option.__name__.capitalize()}")
    print(" ")


def start():
    cpu = False
    while True:
        print("")
        print("   -   Tipo de juego   -")
        print("   1. PvP")
        print("   2. CPU")
        print("")
        option = int_input()  # input - 1
        if option < 0 or option > 1:
            continue

        cpu = option == 1
        break
    print("")

    player_name1 = input("Player 1: ")
    if cpu:
        player_name2 = "CPU"
    else:
        player_name2 = input("Player 2: ")

    players = {
        # Orden de entrada:
        # nombre : entrada
        player_name1: 0,
        player_name2: 0
    }

    count_turns = 1
    # 0 = turn for player 1
    # 1 = turn for player 2
    turn_for = 0
    while True:
        print("")
        show_table(players)
        print("")
        print(f"Turno {count_turns}:")
        count_turns += 1
        pause()

        winner = turn_game(players, turn_for)

        if winner is not None:
            pause()
            break
        else:
            # Switch turns
            turn_for = switch_turn(turn_for)

    if winner != "CPU":
        records.append(winner)
        size = len(records)
        if size > 10:
            records.pop(size - 1)

    print(f"{winner} Winner!")
    pause()


def turn_game(players: dict[str, int], turn_for: int) -> str:
    # Literal python necesita convertir los valores y llaves a list
    # para poder acceder a ellos por index
    list_players = list(players.keys())
    player = list_players[turn_for]

    print("")
    print(f"Turno de {player}:")

    moves = 6
    bonus = False

    winner = None
    while moves == 6 or bonus:
        bonus = False
        print("")
        if player == "CPU":
            moves = random_move(random.randint(0, len(dado_moves) - 1))
        else:
            moves = selected_random_move()

        print("")
        show_table(players)
        print("")
        print(f"{player} obtuvo el valor de {moves}!")

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
            print(f"{player} ha devuelto a {player2} al inicio!")
            players[player2] = 0

        if players[player] in bonuses:
            bonus = True
            print(f"CASILLA BONUS EN {players[player]}!")
        if moves == 6:
            print("No pierde turno!")
        pause()
    return winner


def switch_turn(turn: int):
    if turn == 0:
        return 1
    return 0


def record():
    print(" ")
    print("Records:")
    size = len(records)
    for count in range(10):
        if size == 0 or count > size - 1:
            player = "*"
        else:
            player = records[count]

        print(f"- {player}")
    pause()
    print(" ")


def end():
    exit(0)


options = [start, record, end, welcome]
records = ["Julio Yarasca"]

# TODO: EMPIEZA AQUI!!!
# Bucle del programa para mantenerlo vivo
while True:
    welcome()
    selected = int_input()

    option_size = len(options) - 1
    if selected < 0 or selected > option_size:
        continue

    function = options[selected]
    function()
    print()
