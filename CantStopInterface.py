import CantStopBoard
import random


def roll_die():
    return random.randint(1, 7)


one_id = input("Is player one a computer? [y/n] ")
if one_id == "y":
    one_id = True
else:
    one_id = False

two_id = input("Is player two a computer? [y/n] ")
if two_id == "y":
    two_id = True
else:
    two_id = False

if not one_id or not two_id:
    print()
    print("Note: order of dice rolls matter!")
    print("If you have two caps on the board and neither of the two rolls")
    print("are existing caps, then ONLY THE FIRST WILL COUNT!")
    print()
    print("Also, it's your fault if the program crashes. There aren't any input checks.")
    print("You have been warned.")
    print()
    input("Press enter to continue: ")

times_to_play = int(input("How many times do you want to play? "))
b = CantStopBoard.Board()
# This loop is for each time you play
for i in range(times_to_play):
    b.reset()
    turn = True  # True is player 1, False is player 2
    # One run through this loop is an entire turn, and it only stops running if it's game over
    while not b.check_game_over():
        if turn:
            player = 1
        else:
            player = 2

        to_continue = True  # Whether or not player wants to continue
        while to_continue:
            # The following if statement in words:
            # If not (player one's turn and they're a computer or player two's turn and they're a computer)
            # Basically this part is for human players
            if not(turn and one_id) and not (not turn and two_id):
                print()
                b.aha()
                print()
                print("CURRENT PLAYER:", player)
                print("MID TURN VALUES:", b.midTurnValues)
                print()
                lor = [roll_die(), roll_die(), roll_die(), roll_die()]      # list_of_rolls
                print("Here are your rolls:")
                print("\t", lor)
                options = [[lor[0] + lor[1], lor[2] + lor[3]], [lor[2] + lor[3], lor[0] + lor[1]],
                           [lor[0] + lor[2], lor[1] + lor[3]], [lor[1] + lor[3], lor[0] + lor[2]],
                           [lor[0] + lor[3], lor[1] + lor[2]], [lor[1] + lor[2], lor[0] + lor[3]]]
                print("Here are your options:")
                print("\t", options)
                print()
                user_choice = int(input("Which option will you choose? [1/2/3/4/5/6] "))
                o_index = user_choice - 1
                if b.legal_move(options[o_index][0], player) or b.legal_move(options[o_index][1], player):
                    b.move_player(options[o_index][0], player)
                    b.move_player(options[o_index][1], player)
                    b.aha()
                else:
                    print()
                    input("Sorry, you lose your progress.")
                    to_continue = False
                    b.end_turn_assumed_legal(player, False)
                ###
                print()
                if to_continue:
                    to_continue = input("Would you like to roll again? [y/n] ")
                    if to_continue == "y":
                        to_continue = True
                    else:
                        if b.check_overlaps():
                            input("Sorry, you Can't Stop!")
                            to_continue = True
                        else:
                            to_continue = False
                            b.end_turn_assumed_legal(player, True)
            else:
                # Put all computer and neural network functionality here!
                input("Sorry, we don't have functionality for computers yet. Check back later.")
                to_continue = False

        turn = not turn
    print()
    print()
    print()
    input("Game is over!")
