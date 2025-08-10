# Chloe Gabriella Kwie S10272750C

import random
from random import randint

# i changed it to a list so I can append and insert info when needed
player = {
    'x': 1,
    'y': 1,
    'copper': 0,
    'silver': 0,
    'gold': 0,
    'money': 0,
    'day': 0,
    'steps': 0,
    'turns': 20,
    'load': 0,
    'space': 10,
    'last_x': None,
    'last_y': None
}
map_struct = []
game_map = []
fog = []
pickaxe = ['1 (copper)']  # i needed a place to insert the pickaxe level
pickaxe_level = 1


MAP_WIDTH = 0
MAP_HEIGHT = 0
TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}
pickaxe_price = [50, 150]

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT


def load_map(filename, map_struct):
    global MAP_WIDTH
    global MAP_HEIGHT

    map_struct.clear()

    with open(filename, 'r') as map_file:
        for line in map_file:
            # Convert each line into list of characters
            row = list(line.rstrip('\n'))
            map_struct.append(row)

    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)


load_map("level1.txt", game_map)


def show_map(map_struct):
    for row in map_struct:
        print("".join(row))


# This function clears the fog of war at the 3x3 square around the player


def clear_fog(fog, player):
    x, y = player['x'], player['y']
    height = len(fog)
    width = len(fog[0])

    for ny in range(max(0, y - 1), min(height, y + 2)):  # nx/ ny = new x/ new y
        for nx in range(max(0, x - 1), min(width, x + 2)):
            # -1 for left right up down. 0 to avoid neg index +2 is endpoint
            fog[ny][nx] = True


def initialize_game(game_map, fog, player):
    # initialize map
    load_map("level1.txt", game_map)

    for row in game_map:
        fog.append([False] * len(row))
    # to unfog borders
    for x in range(len(fog[0])):
        fog[0][x] = True
    for x in range(len(fog[-1])):
        fog[-1][x] = True
    for y in range(len(fog)):
        fog[y][0] = True
    for y in range(len(fog)):
        fog[y][-1] = True

    player['x'] = 1
    player['y'] = 1
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['money'] = 0
    player['day'] = 0
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['load'] = 0
    player['space'] = 10

    clear_fog(fog, player)

# money money money


def sell_minerals(player, prices):
    print("\n--- Selling Minerals ---")
    total_earned = 0

    for mineral in ['copper', 'silver', 'gold']:
        amount = player.get(mineral, 0)
        if amount > 0:
            min_price, max_price = prices[mineral]
            # Choose a random price per unit within the range
            price_per_unit = random.randint(min_price, max_price)
            earned = amount * price_per_unit

            print(
                f"You sold {amount} {mineral} for {price_per_unit} GP each, earning {earned} GP.")

            total_earned += earned
            player[mineral] = 0  # reset player's mineral count after selling
        else:
            print(f"You have no {mineral} to sell.")
    player['money'] += total_earned
    print(f"Total GP earned: {total_earned}")
    print(f"Your total GP is now: {player['money']}")


# This function draws the entire map, covered by the fof (fog?)

def draw_map(game_map, fog, player):
    for y in range(len(game_map)):
        row = ""
        for x in range(len(game_map[0])):
            if player['x'] == x and player['y'] == y:
                row += "P"
            elif fog[y][x]:
                row += game_map[y][x]
            else:
                row += "?"
        print(row)
    return

# This function draws the 3x3 viewport


def draw_view(game_map, fog, player):
    x = player['x']
    y = player['y']

    print("+---+")
    for dy in [-1, 0, 1]:
        row = "|"
        for dx in [-1, 0, 1]:
            nx = x + dx
            ny = y + dy

            if 0 <= ny < len(game_map) and 0 <= nx < len(game_map[0]):
                if nx == x and ny == y:
                    row += "P"
                elif fog[ny][nx]:
                    row += game_map[ny][nx]
                else:
                    row += "?"
            else:
                row += "?"
        row += "|"
        print(row)
    print("+---+")


# This function checks if ore can be mined

def can_mine(ore_char, pickaxe_level):
    ore_requirements = {'C': 1, 'S': 2, 'G': 3}
    required_level = ore_requirements.get(ore_char, 0)
    return pickaxe_level >= required_level

# Teleportation


def use_portal_stone(player):
    if player['last_x'] is None and player['last_y'] is None:
        # Save current mine position
        player['last_x'] = player['x']
        player['last_y'] = player['y']
        # Teleport to town

    else:
        # Teleport back to saved mine position
        player['x'] = player['last_x']
        player['y'] = player['last_y']
        player['last_x'] = None
        player['last_y'] = None

# This fuction moves the player


def move_player(player, game_map, fog):
    print("*Funfact: You can always press I to check player Info!!")
    direction = input("Move (W/A/S/D)? Press Q to quit.").lower()
    x, y = player['x'], player['y']
    dx, dy = 0, 0

    if direction == 'w':
        dy = -1

    elif direction == 's':
        dy = 1

    elif direction == 'a':
        dx = -1

    elif direction == 'd':
        dx = 1

    elif direction == 'q':
        player['last_x'] = player['x']
        player['last_y'] = player['y']
        use_portal_stone(player)
        return "quit"

    elif direction == 'i':
        return "i"

    else:
        print("Invalid input. Use W/A/S/D to move.")
        return

    new_x = player['x'] + dx
    new_y = player['y'] + dy

    # Check if within map boundaries
    if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
        target_tile = game_map[new_y][new_x]
        if target_tile in ['-', '+', '|']:
            print("You bumped into a wall!")
            return

        pieces_obtained = {
            'copper': (1, 5),
            'silver': (1, 3),
            'gold': (1, 2)
        }

        if target_tile in ['C', 'S', 'G']:
            if can_mine(target_tile, pickaxe_level):  # check if can mine
                mineral = mineral_names[target_tile]
                min_pieces, max_pieces = pieces_obtained[mineral]
                amtofore = randint(min_pieces, max_pieces)
                if player["load"] < player["space"]:
                    player["load"] += amtofore
                    player[mineral] += amtofore
                    print(f"You mined {amtofore} {mineral}")

                    game_map[new_y][new_x] = ' '  # Remove ore after mining
                else:
                    print("You're bag is full!")
            else:
                print(
                    f"You cannot mine {mineral_names[target_tile]} yet. Upgrade your pickaxe!")
                return

        player['x'] = new_x
        player['y'] = new_y
        player['steps'] += 1
        player['turns'] -= 1
        clear_fog(fog, player)
        print("You moved.")
        print(f"You have {player['turns']} turns left.")
        if player['turns'] <= 0:
            print("You've fainted from exhaustion. Portal stone has been place and the rescue team brought you back to town.")
            game_map[player['y']][player['x']] = 'P'
            player['last_x'] = player['x']
            player['last_y'] = player['y']
            use_portal_stone(player)
            player['turns'] = TURNS_PER_DAY
            return "fainted"
    else:

        print("You can't move outside the map.")


def game_loop():
    while True:
        draw_map(game_map, fog, player)

        result = move_player(player, game_map, fog)  # W/A/S/D dx/dy movement
        if result == "quit":
            break

        if player['turns'] <= 0:
            print("Day ended!")
            player['day'] += 1
            player['turns'] = TURNS_PER_DAY

# This function saves the information for the player

# This function calculates the money


def money_counter():
    gp_gain = randint(*prices)
    player['money'] += gp_gain


def save_player_info():
    with open("savefile.txt", "w") as file:
        file.write(name + "\n")
        file.write(f"{player['x']},{player['y']}\n")
        file.write(str(pickaxe) + "\n")
        file.write(str(player['load']) + "\n")
        file.write(str(player['space']) + "\n")
        file.write(str(player['money']) + "\n")
        file.write(str(player['steps']) + "\n")
        file.write(str(player['turns']) + "\n")
        file.write(str(player['day']) + "\n")


# This loads the player information


def load_player_info():
    global name, pickaxe_level
    try:
        with open("savefile.txt", "r") as file:
            name = file.readline().strip()
            pos_line = file.readline().strip().split(",")
            if pos_line == '':
                print('Portal stone not set, using default (0,0)')
                player['x'] = 0
                player['y'] = 0
                player['x'] = int(pos_line[0])
                player['y'] = int(pos_line[1])
            pickaxe_str = file.readline().strip()
            pickaxe.append(pickaxe_str)
            player['load'] = int(file.readline().strip())
            player['space'] = int(file.readline().strip())
            player['money'] = int(file.readline().strip())
            player['steps'] = int(file.readline().strip())
            player['turns'] = int(file.readline().strip())
            player['day'] = int(file.readline().strip())
        return name, player, pickaxe
    except FileNotFoundError:
        print("No save file found.")  # so it doesnt crash if there isnt a file
        return None

# This function saves the game


def save_game(game_map, fog, player):
    with open("savefiles.txt", "w") as f:
        # Save player
        f.write(str(player['x']) + "\n")
        f.write(str(player['y']) + "\n")

        f.write("---MAP---\n")
        for row in game_map:
            f.write("".join(row) + "\n")

        f.write("---FOG---\n")
        for row in fog:
            f.write("".join("1" if cell else "0" for cell in row) + "\n")

    print("Game saved!")
    return

# This function loads the game


def load_game(game_map, fog, player):
    try:
        with open("savefiles.txt", "r") as f:
            lines = f.readlines()

        player.clear()
        game_map.clear()
        fog.clear()

        # First two lines are player x and y
        player['x'] = int(lines[0].strip())
        player['y'] = int(lines[1].strip())

        section = None
        for line in lines[2:]:
            line = line.strip()
            if line == "---MAP---":
                section = "map"
                continue
            elif line == "---FOG---":
                section = "fog"
                continue

            if section == "map":
                game_map.append(list(line))  # row of characters
            elif section == "fog":
                fog.append([c == "1" for c in line])  # 1 = true 0 = false

        print("Game loaded!")
        return True

    except FileNotFoundError:
        print("No save file found.")
        return False
    return


def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
#    print("(H)igh scores") #cher im too dumb for that
    print("(Q)uit")
    print("------------------")


def show_town_menu():
    print()  # provide spacing so it does not look so packed
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("(S)ell ore")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")


# -----------------------------------------------------------------------------------------------------------------

# display main menu PART 1


# --------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
# changed 1000 to 500 cause we only need 500 GP
print("How quickly can you get the 500 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")


def start_game():
    global name  # its inside a function and i need to use it outside this function, hence global
    name = ''  # for saving / loading to work
    while True:
        show_main_menu()
        player_choice = input("Your choice? ")
        # when player wants a new game
        if player_choice.lower() == 'n':
            name = input("Greetings, miner! What is your name? ")
            print(f"Pleased to meet you {name}. Welcome to Sundrop Town!")
            break
        # when player wants to load game
        elif player_choice.lower() == 'l':
            loaded = load_game(game_map, fog, player)
            if not loaded:  # load_game should return False if no file
                print("Data not found, please create a new game.")
            if loaded:
                load_player_info()
                print(f"Welcome back, {name}")
                break

    # when player wants to quit game
        elif player_choice.lower() == 'q':
            import sys  # google searched this..;w;
            print("Saving your progress...")
            save_game(game_map, fog, player)
            print("I hope you enjoyed your stay in Sundrop Town!")
            print("Good luck on finding your next job for retirement! :3")
            sys.exit()
        else:
            print("Invalid input. Please try again.")


exit_mine = False  # just so exit_mine exists and the system doesnt crash-
day = 1

while True:
    start_game()
    # display town menu PART 2
    steps = 0
    exit_mine = False
    while True:
        print(f"\n--- Day {day} ---")
        show_town_menu()
        if player['load'] != 0:
            player['load'] = 0
            print("Ore has been stored and player load has been set to 0")
            player['steps'] = 0
        town_choice = input("Your choice? ").lower()
        print('')

        # buy stuff
        if town_choice == 'b':
            PICKAXE_LEVELS = {  # A constant, so all caps for easier visibility
                1: {
                    "minerals": ["copper"],
                    "upgrade_cost": 50
                },
                2: {
                    "minerals": ["copper", "silver"],
                    "upgrade_cost": 150
                },
                3: {
                    "minerals": ["copper", "silver", "gold"],
                    "upgrade_cost": None  # No further upgrades
                }
            }
            while True:
                print("\n----------------------- Shop Menu -------------------------")
                if pickaxe_level < 3:  # for pickaxe shop text
                    next_level = pickaxe_level + 1
                    # searches for the "upgrade cost" value
                    upgrade_price = PICKAXE_LEVELS[pickaxe_level]["upgrade_cost"]
                    # -1 so that the mineral found will be the most recent one in the list
                    next_mineral = PICKAXE_LEVELS[next_level]["minerals"][-1]
                    print(
                        f"(P)ickaxe upgrade to Level {next_level} to mine {next_mineral} ore for {upgrade_price} GP")
                else:
                    print("Pickaxe is already at maximum level.")

                newstorage = player['space']+2

                print(
                    f"(B)ackpack upgrade to carry {newstorage} items for {newstorage*2} GP")  # idt theres a limit for the backpack so.. I didn't limit it
                print("(L)eave shop")
                print("-----------------------------------------------------------")
                print(f"GP: {player['money']}")
                print("-----------------------------------------------------------")

                choice = input("Your choice? ").lower()
                # just added space for easier visibility [personal choice]
                print()

                if choice == "m":
                    # cheat code for me to test... aha (easter egg~)
                    player['money'] += 100

                if choice == "p":
                    if pickaxe_level >= 3:
                        print("Your pickaxe is already at the maximum level.")
                        continue

                    upgrade_cost = PICKAXE_LEVELS[pickaxe_level]["upgrade_cost"]

                    if player['money'] >= upgrade_cost:
                        player['money'] -= upgrade_cost
                        pickaxe_level += 1
                        new_mineral = PICKAXE_LEVELS[pickaxe_level]["minerals"][-1]
                        print(
                            f"Congratulations! You can now mine {new_mineral}!")
                    else:
                        print("Not enough GP for pickaxe upgrade.")

                elif choice == "b":
                    if player['money'] >= (newstorage*2):
                        player['money'] -= (newstorage*2)
                        player['space'] += 2
                        print(
                            f"Congratulations! Your bag can now carry {player['space']}!")
                    else:
                        print("Not enough GP for bag upgrade.")

                elif choice == "l":
                    break

                else:
                    print("Invalid input. Please try again.")

        # sell ore
        elif town_choice == 's':
            if 'money' not in player:  # so error doesnt occur, money has value assigned
                player['money'] += 0
            selling = input(
                "Are you sure you want to sell all your ore? Type 'Y' for yes to sell: ").lower()
            if selling == 'y':
                sell_minerals(player, prices)
            else:
                print("Ok then, keep the ore.")

        # see player infoo
        elif town_choice == 'i':

            if pickaxe_level == 1:
                minable = 'copper'
            elif pickaxe_level == 2:
                minable = 'silver'
            elif pickaxe_level == 3:
                minable = 'gold'

            print("----- Player Information -----")
            print(f"Name: {name}")
            print(f"Portal position: {player['x']},{player['y']}")
            print(f"Pickaxe level: {pickaxe_level}, {minable}")
            print("------------------------------")
            print(f"Load: {player['load']}/{player['space']}")
            print("------------------------------")
            print(f"GP: {player['money']}")
            print(f"Steps taken: {player['steps']}")
            print("------------------------------")

        # see the map
        elif town_choice == 'm':
            initialize_game(game_map, fog, player)
            if game_map:
                print(
                    f"Map exploration progress:")
            else:
                print("Game map is empty!")

            draw_map(game_map, fog, player)

        # save the game
        elif town_choice.lower() == 'v':
            save_game(game_map, fog, player)
            save_player_info()

        # quit to main menu
        elif town_choice.lower() == 'q':
            break

        # enter the mine
        elif town_choice == 'e':
            initialize_game(game_map, fog, player)
            if player.get('last_cave_x') is not None and player.get('last_cave_y') is not None:
                player['x'] = player['last_cave_x']
                player['y'] = player['last_cave_y']
            else:
                # default start
                player['x'], player['y'] = 1, 1

            while True:
                draw_map(game_map, fog, player)
                draw_view(game_map, fog, player)
                result = move_player(player, game_map, fog)

                if result == "fainted":
                    day += 1
                    break
                elif result == "quit":
                    day += 1
                    print(
                        "Placed portal stone... Exiting mine... returning to town menu...")
                    break
                elif result == 'i':
                    if pickaxe_level == 1:
                        minable = 'copper'
                    elif pickaxe_level == 2:
                        minable = 'silver'
                    elif pickaxe_level == 3:
                        minable = 'gold'
                    print("----- Player Information -----")
                    print(f"Name: {name}")
                    print(f"Portal position: {player['x']},{player['y']}")
                    print(f"Pickaxe level: {pickaxe_level}, {minable}")
                    print("------------------------------")
                    print(f"Load: {player['load']}/{player['space']}")
                    print("------------------------------")
                    print(f"GP: {player['money']}")
                    print(f"Steps taken: {player['steps']}")
                    print("------------------------------")

        else:
            print("Invalid input, pleast try again.")
