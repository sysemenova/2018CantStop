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
        self.playerOneWins = 0
        self.playerTwoWins = 0
        self.fullValues = []
        self.midTurnValues = []

    def reset(self):
        # Make the board 0 on playable area
        for z in range(2):
            for x in range(11):
                for y in range(13):
                    if y >= index_function(x):
                        self.boardMatrix[x, y, z] = 0
                        # Variables to signify who's turn it is
        self.midTurn = False
        # Current player will be either 0 (no one's turn) or 1 or 2
        self.currentPlayer = 0
        self.playerOneWins = 0
        self.playerTwoWins = 0
        self.fullValues = []
        self.midTurnValues = []

    def move_player(self, value, player):
        # Checks for legality before play
        if self.legal_move(value, player):
            self.move_player_legal_move(value, player)

    def move_player_legal_move(self, value, player):
        # Assumes the move is legal
        # Modify mid turn variables
        if not (value in self.midTurnValues):
            self.midTurnValues.append(value)
        self.midTurn = True
        self.currentPlayer = player
        # Set the correct indices
        z = player - 1
        x = value - 2
        y = self.player_mid_turn_position(player, value)  # Mid turn position also gives solid position
        # If they haven't made progress, start them
        if y == -1:
            self.boardMatrix[x, index_function(x), z] = 2
        else:
            if self.player_mid_turn_position(player, value) == self.player_solid_position(player, value):
                self.boardMatrix[x, y + 1, z] = 2
            else:
                self.boardMatrix[x, y, z] = 0
                self.boardMatrix[x, y + 1, z] = 2

    def legal_move(self, value, player):
        # Did someone already win?
        if self.check_game_over():
            return False
        # Is the value within the appropriate range?
        if not (value in range(2, 13)):
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
            return False

        # If no illegal moves, return true
        return True

    def get_active_values(self):
        return self.midTurnValues

    def get_current_player(self):
        return self.currentPlayer

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

    def return_full_values(self):
        return self.fullValues

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
        if self.playerOneWins == 3 or self.playerTwoWins == 3:
            return True
        else:
            return False

    def end_turn(self, player, save):
        # If it is illegal to stop, it doesn't. Assumes legality, though makes sure it only acts
        # under legal circumstances, basically.
        # Save is a boolean
        if not self.check_overlaps():
            self.end_turn_assumed_legal(player, save)

    def end_turn_assumed_legal(self, player, save):
        self.midTurn = False
        self.midTurnValues = []
        self.currentPlayer = 0
        z = player - 1
        # x is the value - 2
        for x in range(11):
            value = x + 2
            if self.player_solid_position(player, value) != self.player_mid_turn_position(player, value):
                if save:
                    if self.player_solid_position(player, value) != -1:
                        self.boardMatrix[x, self.player_solid_position(player, value), z] = 0
                    self.boardMatrix[x, self.player_mid_turn_position(player, value), z] = 1
                    # If the player won this turn, remove the other player's progress
                    if self.check_column(x + 2) == player:
                        self.fullValues.append(x + 2)
                        # If player 1 won, remove player two's progress
                        if player == 1:
                            self.playerOneWins += 1
                            other_player = self.player_solid_position(2, value)
                            # If they made no progress at all, don't do anything
                            if other_player != -1:
                                self.boardMatrix[x][other_player][1] = 0
                        # If player 2 won, remove player one's progress
                        else:
                            self.playerTwoWins += 1
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

    def return_nn_matrix(self):
        nnmatrix = np.ones([11, 4])
        for x in range(11):
            playeronesolid = self.player_solid_position(1, x + 2)
            if playeronesolid == -1:
                playeronemid = self.player_mid_turn_position(1, x + 2)
                if playeronemid == -1:
                    nnmatrix[x, 0] = 0
                else:
                    nnmatrix[x, 0] = playeronemid - index_function(x) + 1
                nnmatrix[x, 1] = 12 - index_function(x) + 1
            else:
                nnmatrix[x, 0] = self.player_mid_turn_position(1, x + 2) - playeronesolid
                nnmatrix[x, 1] = 12 - playeronesolid

            playertwosolid = self.player_solid_position(2, x + 2)
            if playertwosolid == -1:
                playertwomid = self.player_mid_turn_position(2, x + 2)
                if playertwomid == -1:
                    nnmatrix[x, 2] = 0
                else:
                    nnmatrix[x, 2] = self.player_mid_turn_position(2, x + 2) - index_function(x) + 1
                nnmatrix[x, 3] = 12 - index_function(x) + 1
            else:
                nnmatrix[x, 2] = self.player_mid_turn_position(2, x + 2) - playertwosolid
                nnmatrix[x, 3] = 12 - playertwosolid
        return nnmatrix

    def readable_matrix(self, player):
        z = player - 1
        # for 2: #
        mat = np.ones([13, 11]) * -1
        start = 5  # starting index for row of readable
        end = 7  # ending index for row of readable
        startBoard = 10  # starting index for col of original
        endBoard = 12  # ending index for col of original
        col = 0  # col of readable
        other_half = 10  # this is the corresponding col for the right half of the readable
        other_original_half = 10  # this is the corresponding row for the bottom half of the original
        while (start >= 0):
            for x in range(start, end + 1):
                for y in range(startBoard, endBoard + 1):
                    mat[x, col] = self.boardMatrix[col + 1, y, z]
                    mat[x, 10 - col] = self.boardMatrix[other_half, other_original_half, z]
            start -= 1
            end += 1
            startBoard -= 2
            col += 1
            other_half -= 1
            other_original_half -= 2
        return mat

    def return_pure_matrix(self):
        return self.boardMatrix

    def aha(self):
        # print(self.readable_matrix(1))
        # print()
        # print(self.readable_matrix(2))
        print(self.boardMatrix[:, :, 0])
        print()
        print(self.boardMatrix[:, :, 1])
