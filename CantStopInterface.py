import Rollouts
import CantStopBoard
import random
import numpy as np


def roll_die():
    return random.randint(1, 6)


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

save_id = input("Do you wish to save data? [y/n] ")
if save_id == "y":
    save_id = True
    y_v = np.ones(2) * 4
    y_v[0] = 1
    y_counter = False
    save_name = input("What do you want to call the file (include .txt)? ")
    f = open(save_name, 'w')
    y_save_name = input("What do you want to call the y file (include .txt)? ")
    yf = open(y_save_name, 'w')
else:
    save_id = False

any_humans = not one_id or not two_id

if any_humans:
    print()
    print("Note: order of dice rolls matter!")
    print("If you have two caps on the board and neither of the two rolls")
    print("are existing caps, then ONLY THE FIRST WILL COUNT!")
    print()
    print("Also, it's your fault if the program crashes. There aren't any input checks.")
    print("You have been warned.\t:)")
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
                lor = Rollouts.roll_dice()      # list_of_rolls
                print("Here are your rolls:")
                print("\t", lor)
                options = Rollouts.generate_moves(b, lor, player)
                if(options is None):
                    print()
                    input("Sorry, you lose your progress.")
                    to_continue = False
                    b.end_turn_assumed_legal(player, False)
                else:
                    print("Here are your options:")
                    print("\t", options)
                    print()
                    user_choice = int(input("Which option number will you choose? "))
                    o_index = user_choice - 1
                    b.move_player(options[o_index][0], player)
                    if(len(options[o_index]) == 2):
                        b.move_player(options[o_index][1], player)
                    b.aha()
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

            # Here is the code for putting stuff into a text file
            if save_id:
                m = b.nnMatrix.copy()
                if player == 2:
                    n = b.nnMatrix.copy()
                    m[:, :2] = n[:, 2:]
                    m[:, 2:] = n[:, :2]
                m = m.reshape(44)
                # b = np.array2string(a)
                s = np.array2string(m, max_line_width=1000)
                print(s)
                f.write(s + "\n")
                if y_counter:
                    # Code for appending player's stuff
                    q = np.array([player, 4])
                    y_v = np.vstack((y_v, q))
                else:
                    y_counter = True    # Meaning it's the first turn and it already did stuff
        turn = not turn
    if any_humans:
        print()
        print()
        print()
        input("Game is over!")
    if save_id:
        if b.playerOneWins == 3:
            winner = 1
        else:
            winner = 2
        y = (y_v[:, 0] == winner)
        s = np.array2string(y)
        yf.write(s)

        f.close()
        yf.close()