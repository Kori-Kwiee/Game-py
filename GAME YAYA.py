# Chloe Gabriella Kwie S10272750C

from random import randint

# i changed it to a list so I can append and insert info when needed
player = {}
map_struct = []
game_map = []
fog = []
pickaxe = ['1 (copper)']  # i needed a place to insert the pickaxe level
pickaxe_level = 1
bag_level = 10
space = 10  # also needed space to put bag space
money = 0  # and the money

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

    fog.clear()
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

    # TODO: initialize player
    #   You will probably add other entries into the player dictionary

    player['x'] = 1
    player['y'] = 1
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['day'] = 0
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY

    clear_fog(fog, player)

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

# This fuction moves the player


def move_player(player, game_map, fog):
    direction = input("Move (W/A/S/D)? ").lower()
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
        return 'quit'
    else:
        print("Invalid input. Use W/A/S/D to move.")
        return

    new_x = player['x'] + dx
    new_y = player['y'] + dy

    # Check if within map boundaries
    if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
        target_tile = game_map[new_y][new_x]

        # Check for walls
        if target_tile not in ['-', '+', '|']:
            player['x'] = new_x
            player['y'] = new_y
            player['steps'] += 1
            player['turns'] -= 1
            clear_fog(fog, player)
            print("You moved.")
        else:
            print("You bumped into a wall!")
    else:
        print("You can't move outside the map.")

# This function saves the information for the player


def save_player_info():
    with open("savefile.txt", "w") as file:
        file.write(name + "\n")
        file.write(f"{player[0]},{player[1]}\n")
        file.write(str(pickaxe) + "\n")
        file.write(str(load) + "\n")
        file.write(str(space) + "\n")
        file.write(str(money) + "\n")
        file.write(str(steps) + "\n")
    print("Game saved!")

# This loads the player information


def load_player_info():
    try:
        with open("savefile.txt", "r") as file:
            name = file.readline().strip()
            pos_line = file.readline().strip().split(",")
            player = (int(pos_line[0]), int(pos_line[1]))
            pickaxe = file.readline().strip()
            load = int(file.readline().strip())
            space = int(file.readline().strip())
            gold = int(file.readline().strip())
            steps = int(file.readline().strip())
        print("Game loaded!")
        return name, player, pickaxe, load, space, gold, steps
    except FileNotFoundError:
        print("No save file found.")
        return None

# This function saves the game


def save_game(game_map, fog, player):
    # save map
    # save fog
    # save player
    return

# This function loads the game


def load_game(game_map, fog, player):
    # load map
    # load fog
    # load player
    return


def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
#    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")


def show_town_menu():
    print()  # provide spacing so it does not look so packed
    print(f"DAY {day}")  # edited to show days
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
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
            load_game(game_map, fog, player)
            if name == '':  # if name is None or empty string
                print("Data not found, please create a new game.")

            else:
                print(f"Welcome back, {name}")
                break
    # when player wants to quit game
        elif player_choice.lower() == 'q':
            import sys  # google searched this..;w;
            print("Saving your progress...")
            save_game(game_map, fog, player)
            print("Progress saved.")
            print("I hope you enjoyed your stay in Sundrop Town!")
            print("Good luck on finding your next job for retirement! :3")
            sys.exit()
        else:
            print("Invalid input. Please try again.")


while True:
    start_game()
    while True:
        # display town menu PART 2
        day = 0
        day += 1
        print(f"\n--- Day {day} ---")
        # load and steps reset
        load = 0
        steps = 0
        # gold
        show_town_menu()
        town_choice = input("Your choice? ").lower()

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

                newstorage = bag_level+2

                print(
                    f"(B)ackpack upgrade to carry {newstorage} items for {newstorage*2} GP")  # idt theres a limit for the backpack so.. I didn't limit it
                print("(L)eave shop")
                print("-----------------------------------------------------------")
                print(f"GP: {money}")
                print("-----------------------------------------------------------")

                choice = input("Your choice? ").lower()
                # just added space for easier visibility [personal choice]
                print()

                if choice == "m":
                    # cheat code for me to test... aha (easter egg~)
                    money += 100

                if choice == "p":
                    if pickaxe_level >= 3:
                        print("Your pickaxe is already at the maximum level.")
                        continue

                    upgrade_cost = PICKAXE_LEVELS[pickaxe_level]["upgrade_cost"]

                    if money >= upgrade_cost:
                        money -= upgrade_cost
                        pickaxe_level += 1
                        new_mineral = PICKAXE_LEVELS[pickaxe_level]["minerals"][-1]
                        print(
                            f"Congratulations! You can now mine {new_mineral}!")
                    else:
                        print("Not enough GP for pickaxe upgrade.")

                elif choice == "b":
                    if money >= (newstorage*2):
                        money -= (newstorage*2)
                        bag_level += 2
                        print(
                            f"Congratulations! Your bag can now carry {bag_level}!")
                    else:
                        print("Not enough GP for bag upgrade.")

                elif choice == "l":
                    break

                else:
                    print("Invalid input. Please try again.")

        # see player infoo
        elif town_choice == 'i':
            load_player_info()
            print("----- Player Information -----")
            print(f"Name: {name}")
            print(f"Portal position: {player}")
            print(f"Pickaxe level: {pickaxe[0]}")
            # pickaxe[0] so it doesnt show as ['1 copper'] <eg.
            print("------------------------------")
            print(f"Load: {load}/{space}")
            print("------------------------------")
            print(f"GP:{money}")
            print(f"Steps taken: {steps}")
            print("------------------------------")

        # see the map
        elif town_choice == 'm':
            initialize_game(game_map, fog, player)
            if game_map:
                print(
                    f"Map size: {len(game_map)} rows x {len(game_map[0])} cols")
            else:
                print("Game map is empty!")

            draw_map(game_map, fog, player)

        # enter the mine
        elif town_choice == 'e':
            while True:
                initialize_game(game_map, fog, player)

                while True:
                    draw_view(game_map, fog, player)
                    result = move_player(player, game_map, fog)
                    if result == "quit":
                        break

        # save the game
        elif town_choice.lower() == 'v':
            save_game()
            save_player_info()
            print("Game saved!")

        # quit to main menu
        elif town_choice.lower() == 'q':
            break
