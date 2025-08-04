# Chloe Gabriella Kwie S10272750C

from random import randint

player = []  # i changed it to a list so I can append and insert info when needed
game_map = []
fog = []
pickaxe = ['1 (copper)']  # i needed a place to insert the pickaxe level
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
    map_file = open(filename, 'r')
    global MAP_WIDTH
    global MAP_HEIGHT

    map_struct.clear()

    # TODO: Add your map loading code here

    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)

    map_file.close()

# This function clears the fog of war at the 3x3 square around the player


def clear_fog(fog, player):
    return


def initialize_game(game_map, fog, player):
    # initialize map
    load_map("level1.txt", game_map)

    # TODO: initialize fog

    # TODO: initialize player
    #   You will probably add other entries into the player dictionary
    player['x'] = 0
    player['y'] = 0
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
    return

# This function draws the 3x3 viewport


def draw_view(game_map, fog, player):
    return

# This function shows the information for the player


def show_information(player):
    return

# This saves player information


def save_player_info():
    with open("savefile.txt", "w") as file:
        file.write(name + "\n")
        file.write(f"{position[0]},{position[1]}\n")
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
            position = (int(pos_line[0]), int(pos_line[1]))
            pickaxe = file.readline().strip()
            load = int(file.readline().strip())
            space = int(file.readline().strip())
            gold = int(file.readline().strip())
            steps = int(file.readline().strip())
        print("Game loaded!")
        return name, position, pickaxe, load, space, gold, steps
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

show_main_menu()
player_choice = input("Your choice? ")

# when player wants a new game
if player_choice.lower() == 'n':
    name = input("Greetings, miner! What is your name? ")
    print(f"Pleased to meet you {name}. Welcome to Sundrop Town!")


# when player wants to load game
if player_choice.lower() == 'l':
    load_game(game_map, fog, player)

# when player wants to quit game
if player_choice.lower() == 'q':
    import sys  # google searched this..;w;
    print("Saving your progress...")
    save_game(game_map, fog, player)
    print("Progress saved.")
    print("I hope you enjoyed your stay in Sundrop Town!")
    print("Good luck on finding your next job for retirement! :3")
    sys.exit()

# display town menu PART 2
day = 0
day += 1
# everything but the day + money and pickaxe resets
position = [0, 0]
load = 0
steps = 0
# gold
while True:
    show_town_menu()
    town_choice = input("Your choice? ").lower()

    # buy stuff
    if town_choice == 'b':
        print('Shopp')

    # see player infoo
    elif town_choice == 'i':
        load_player_info()
        print("----- Player Information -----")
        print(f"Name: {name}")
        print(f"Portal position: {position}")
        print(f"Pickaxe level: {pickaxe[0]}")
        # pickaxe[0] so it doesnt show as ['1 copper'] <eg.
        print("------------------------------")
        print(f"Load: {load}/{space}")
        print("------------------------------")
        print(f"GP:{money}")
        print(f"Steps taken: {steps}")
        print("------------------------------")

    # see the map

    # enter the mine
    elif town_choice == 'e':
        print("Entering the mine...")
        break

    # save the game
    elif town_choice.lower() == 'v':
        save_game()
        save_player_info()
        print("Game saved!")

    # quit to main menu
    elif town_choice.lower() == 'q':
        show_main_menu()
        break
