import random
import os
import colorama
import platform

from colorama import Fore, Back, Style
from torpydo.ship import Color, Letter, Position, Ship
from torpydo.game_controller import GameController
from torpydo.telemetryclient import TelemetryClient

print("Starting")

myFleet = []
enemyFleet = []
all_coordinates = [Position(column, row) for column in Letter for row in range(1, 9)]

def main():
    TelemetryClient.init()
    TelemetryClient.trackEvent('ApplicationStarted', {'custom_dimensions': {'Technology': 'Python'}})
    colorama.init()
    print(Fore.YELLOW + r"""
                                    |__
                                    |\/
                                    ---
                                    / | [
                             !      | |||
                           _/|     _/|-++'
                       +  +--|    |--|--|_ |-
                     { /|__|  |/\__|  |--- |||__/
                    +---------------___[}-_===_.'____                 /\
                ____`-' ||___-{]_| _[}-  |     |_[___\==--            \/   _
 __..._____--==/___]_|__|_____________________________[___\==--____,------' .7
|                        Welcome to Battleship                         BB-61/
 \_________________________________________________________________________|""" + Style.RESET_ALL)

    initialize_game()

    start_game()

def start_game():
    global myFleet, enemyFleet
    # clear the screen
    if(platform.system().lower()=="windows"):
        cmd='cls'
    else:
        cmd='clear'
    
    os.system(cmd)

    print(r'''
                  __
                 /  \
           .-.  |    |
   *    _.-'  \  \__/
    \.-'       \
   /          _/
   |      _  /
   |     /_\
    \    \_/
     """"""""''')
    mark_segment("GAME STARTED. GOOD LUCK!")
    while True:
        print()
        
        mark_segment("PLAYER, IT IS YOUR TURN!")

        valid_position = False
        while (not valid_position):
            position = parse_position(input("Enter coordinates for your shot :"))
            if (position in all_coordinates):
                valid_position = True
            else:
               mark_segment("INVALID POSITION, RETRY!") 

        is_hit = GameController.check_is_hit(enemyFleet, position)
        if is_hit:
            print_hit("Yeah ! Nice hit !")
        else:
            print_miss("Miss")

        TelemetryClient.trackEvent('Player_ShootPosition', {'custom_dimensions': {'Position': str(position), 'IsHit': is_hit}})

        position = get_random_position()
        is_hit = GameController.check_is_hit(myFleet, position)
        
        TelemetryClient.trackEvent('Computer_ShootPosition', {'custom_dimensions': {'Position': str(position), 'IsHit': is_hit}})

def parse_position(input: str):
    letter = Letter[input.upper()[:1]]
    number = int(input[1:])
    position = Position(letter, number)

    return Position(letter, number)

def get_random_position():
    rows = 8
    lines = 8

    letter = Letter(random.randint(1, lines))
    number = random.randint(1, rows)
    position = Position(letter, number)

    return position

def initialize_game():
    mark_segment("INITIALIZE PLAYER SHIPS")
    initialize_myFleet()

    mark_segment("INITIALIZE ENEMY SHIPS")
    initialize_enemyFleet()

def initialize_myFleet():
    global myFleet

    #myFleet = GameController.initialize_ships()

    #myFleet[0].positions.append(Position(Letter.B, 4))
    # myFleet[0].positions.append(Position(Letter.B, 5))
    # myFleet[0].positions.append(Position(Letter.B, 6))
    # myFleet[0].positions.append(Position(Letter.B, 7))
    # myFleet[0].positions.append(Position(Letter.B, 8))

    # myFleet[1].positions.append(Position(Letter.E, 6))
    # myFleet[1].positions.append(Position(Letter.E, 7))
    # myFleet[1].positions.append(Position(Letter.E, 8))
    # myFleet[1].positions.append(Position(Letter.E, 9))

    # myFleet[2].positions.append(Position(Letter.A, 3))
    # myFleet[2].positions.append(Position(Letter.B, 3))
    # myFleet[2].positions.append(Position(Letter.C, 3))

    # myFleet[3].positions.append(Position(Letter.F, 8))
    # myFleet[3].positions.append(Position(Letter.G, 8))
    # myFleet[3].positions.append(Position(Letter.H, 8))

    # myFleet[4].positions.append(Position(Letter.C, 5))
    # myFleet[4].positions.append(Position(Letter.C, 6))

    myFleet = GameController.initialize_ships()

    print("Please position your fleet (Game board has size from A to H and 1 to 8) :")

    for ship in myFleet:
        print()
        print(f"Please enter the positions for the {ship.name} (size: {ship.size})")

        for i in range(ship.size):
            valid_position = False
            while (not valid_position):
                position_input = parse_position(input("Enter coordinates for your shot :"))
                if (position_input in all_coordinates):
                    valid_position = True
                else:
                   mark_segment("INVALID POSITION, RETRY!") 
            ship.add_position(position_input)
            TelemetryClient.trackEvent('Player_PlaceShipPosition', {'custom_dimensions': {'Position': position_input, 'Ship': ship.name, 'PositionInShip': i}})


        ship_text = f"The {ship.name} is placed!"
        mark_segment(ship_text)

def initialize_enemyFleet():
    global enemyFleet

    enemyFleet = GameController.initialize_ships()

    enemyFleet[0].positions.append(Position(Letter.B, 4))
    enemyFleet[0].positions.append(Position(Letter.B, 5))
    enemyFleet[0].positions.append(Position(Letter.B, 6))
    enemyFleet[0].positions.append(Position(Letter.B, 7))
    enemyFleet[0].positions.append(Position(Letter.B, 8))

    enemyFleet[1].positions.append(Position(Letter.E, 6))
    enemyFleet[1].positions.append(Position(Letter.E, 7))
    enemyFleet[1].positions.append(Position(Letter.E, 8))
    enemyFleet[1].positions.append(Position(Letter.E, 9))

    enemyFleet[2].positions.append(Position(Letter.A, 3))
    enemyFleet[2].positions.append(Position(Letter.B, 3))
    enemyFleet[2].positions.append(Position(Letter.C, 3))

    enemyFleet[3].positions.append(Position(Letter.F, 8))
    enemyFleet[3].positions.append(Position(Letter.G, 8))
    enemyFleet[3].positions.append(Position(Letter.H, 8))

    enemyFleet[4].positions.append(Position(Letter.C, 5))
    enemyFleet[4].positions.append(Position(Letter.C, 6))

def mark_segment(segment):
    width = 73  # This is the approximate width of the line of '#'
    centered_segment = segment.center(width)  # Center the segment within the line width

    print(Fore.YELLOW + r"""
    #############################################################################
    #{}#
    #############################################################################
    """.format(centered_segment) + Style.RESET_ALL)

def print_hit(additionText):
    print(Fore.RED + additionText)
    print(Fore.RED + r'''
                \          .  ./
              \   .:"";'.:..""   /
                 (M^^.^~~:.'"").
            -   (/  .    . . \ \)  -
               ((| :. ~ ^  :. .|))
            -   (\- |  \ /  |  /)  -
                 -\  \     /  /-
                   \  \   /  /''' + Style.RESET_ALL)

def print_miss(additionText):
    print(Fore.BLUE +additionText)
    print(Fore.BLUE + r'''
            .====.._
         ,:._       ~-_
             `\        ~-_
               |          `.
             ,/            ~-_
    -..__..-''                ~~--..__''' + Style.RESET_ALL)

if __name__ == '__main__':
    main()
