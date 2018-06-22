import numpy as np


def index_function(i):
    # Returns at which index the board starts at based on the index
    return abs(2*i - 10)


class Board:
    def __init__(self):
        self.boardMatrix = np.ones([11, 13, 2]) * -1
        self.reset()
        # Variables to signify who's turn it is
        self.midTurn = False
        # Current player will be either 0 (no one's turn) or 1 or 2
        self.currentPlayer = 0

    def reset(self):
        # Make the board 0 on playable area
        for z in range(2):
            for x in range(11):
                for y in range(13):
                    if y >= index_function(x):
                        self.boardMatrix[x, y, z] = 0

    def move_player(self, value, player):
        if self.legal_move(value, player):
            # Modify mid turn variables
            self.midTurn = True
            self.currentPlayer = player
            # Set the correct indices
            z = player - 1
            x = value - 2
            y = self.player_mid_turn_position(player, value)    # Mid turn position also gives solid position
            # If they haven't made progress, start them
            if y == -1:
                self.boardMatrix[x, index_function(x), z] = 2
            else:
                if self.player_mid_turn_position(player, value) == self.player_solid_position(player, value):
                    self.boardMatrix[x, y+1, z] = 2
                else:
                    self.boardMatrix[x, y, z] = 0
                    self.boardMatrix[x, y+1, z] = 2

    def legal_move(self, value, player):
        # Did someone already win?
        if self.check_game_over():
            return False
        # Did someone win the column?
        if self.check_column(value) > 0:
            return False
        # Is the player trying to move on not their turn?
        if self.currentPlayer != player and self.currentPlayer != 0:
            return False
        # Is current player already at the end?
        if self.player_mid_turn_position(player, value) == 12:
            return False

        # Finds the position of the caps
        counter = 0
        list_of_caps = [-1, -1, -1]
        for x in range(11):
            for y in range(index_function(x), 13):
                if self.boardMatrix[x, y, player - 1] == 2:
                    list_of_caps[counter] = x
                    counter += 1
        # If all the caps are filled but the value isn't one of the caps, illegal
        if counter == 3 and not(value - 2 in list_of_caps):
            print("Hello illegal being")
            return False

        # If no illegal moves, return true
        print("Yay legal")
        return True

    def check_column(self, value):
        # Value is actual value, not index
        x = value - 2
        if self.boardMatrix[x, 12, 0] == 1:
            # First player won the column
            return 1
        elif self.boardMatrix[x, 12, 1] == 1:
            # Second player won the column
            return 2
        else:
            # Still an empty column
            return 0

    def check_overlaps(self):
        # Returns true or false only
        for x in range(11):
            for y in range(index_function(x), 13):
                # If it at any  point overlaps, return true
                if self.boardMatrix[x, y, 0] > 0 and self.boardMatrix[x, y, 1] > 0:
                    return True
        # If it never overlapped, return false
        return False

    def check_game_over(self):
        # Wins is a list of who won which column
        wins = [self.check_column(2), self.check_column(3), self.check_column(4), self.check_column(5),
                self.check_column(6), self.check_column(7), self.check_column(8), self.check_column(9),
                self.check_column(10), self.check_column(11), self.check_column(12)]
        p1wins = 0
        p2wins = 0

        for i in wins:
            if i == 1:
                p1wins += 1
            elif i == 2:
                p2wins += 1

        if p1wins == 3 or p2wins == 3:
            return True
        else:
            return False

    def end_turn(self, player, save):
        # If it is illegal to stop, it doesn't. Assumes legality, though makes sure it only acts
        # under legal circumstances, basically.
        # Save is a boolean
        if not self.check_overlaps():
            self.midTurn = False
            self.currentPlayer = 0
            z = player - 1
            # x is the value - 2
            for x in range(11):
                value = x + 2
                if self.player_solid_position(player, value) != self.player_mid_turn_position(player, value):
                    # print("I'm in the 'not equal to each other' thing")
                    if save:
                        if self.player_solid_position(player, value) != -1:
                            self.boardMatrix[x, self.player_solid_position(player, value), z] = 0
                        self.boardMatrix[x, self.player_mid_turn_position(player, value), z] = 1
                        # If the player won this turn, remove the other player's progress
                        if self.check_column(x + 2) == player:
                            # If player 1 won, remove player two's progress
                            if player == 1:
                                other_player = self.player_solid_position(2, value)
                                # If they made no progress at all, don't do anything
                                if other_player != -1:
                                    self.boardMatrix[x][other_player][1] = 0
                            # If player 2 won, remove player one's progress
                            else:
                                other_player = self.player_solid_position(1, value)
                                if other_player != -1:
                                    self.boardMatrix[x, other_player, 0] = 0
                    else:
                        self.boardMatrix[x, self.player_mid_turn_position(player, value), z] = 0

    def player_solid_position(self, player, value):
        # Value and player are both not indices
        # RETURNS THE INDEX (meaning the closer they are to 12, the closer they are to winning
        # Returns -1 if haven't started
        z = player - 1
        x = value - 2
        for y in range(index_function(x), 13):
            if self.boardMatrix[x, y, z] == 1:
                return y
        return -1

    def player_mid_turn_position(self, player, value):
        # Value and player aren't indices
        # Returns the index of the position (closer to 12 means better)
        # Returns -1 if haven't started
        z = player - 1
        x = value - 2
        for y in range(index_function(x), 13):
            if self.boardMatrix[x, y, z] == 2:
                return y
        return self.player_solid_position(player, value)

    def return_pure_matrix(self):
        return self.boardMatrix

    def aha(self):
        print(self.boardMatrix)
