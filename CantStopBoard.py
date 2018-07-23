import numpy as np


def index_function(i):
    # Returns at which index the board starts at based on the index
    return abs(2*i - 10)


class Board:
    def __init__(self):
        self.boardMatrix = np.ones([11, 13, 2]) * -1
        # Variables to signify who's turn it is
        self.midTurn = False
        # Current player will be either 0 (no one's turn) or 1 or 2
        self.currentPlayer = 0
        self.playerOneWins = 0
        self.playerTwoWins = 0
        self.fullValues = []
        self.midTurnValues = []
        self.nnMatrix = np.ones([11, 4])

        self.reset()

    def reset_nn_matrix(self):
        self.nnMatrix[:, 1] = 12 - (index_function(np.arange(11)) - 1)
        self.nnMatrix[:, 3] = self.nnMatrix[:, 1]
        self.nnMatrix[:, 0] = 0
        self.nnMatrix[:, 2] = 0

    def reset(self):
        self.reset_nn_matrix()
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
        # Neural network matrix stuff
        if not(value in self.midTurnValues):
            self.midTurnValues.append(value)
        x = value - 2
        y = (player - 1) * 2
        self.nnMatrix[x, y] += 1

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
        if self.player_mid_turn_position(player, value) == 0:
            return False
        # If all the caps are filled but the value isn't one of the caps, illegal
        if len(self.midTurnValues) == 3 and not(value in self.midTurnValues):
            return False

        # If no illegal moves, return true
        return True

    def get_active_values(self):
        return self.midTurnValues

    def get_current_player(self):
        return self.currentPlayer

    def check_column(self, value):
        # A neural network try
        x = value - 2
        if self.nnMatrix[x, 1] == 0:
            value_to_return = 1
        elif self.nnMatrix[x, 3] == 0:
            value_to_return = 2
        else:
            value_to_return = 0

        return value_to_return

    def return_full_values(self):
        return self.fullValues

    def check_overlaps(self):
        # A neural network try
        for value in self.midTurnValues:
            x = value - 2
            if (self.nnMatrix[x, 0] + (12 - self.nnMatrix[x, 1])) == (self.nnMatrix[x, 2] + (12 - self.nnMatrix[x, 3])):
                return True
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
        # A neural network try
        if not save:
            self.nnMatrix[:, (player - 1) * 2] = 0
        else:
            self.nnMatrix[:, (player - 1) * 2 + 1] = self.nnMatrix[:, (player - 1) * 2 + 1] - self.nnMatrix[:, (player - 1) * 2]
            self.nnMatrix[:, (player - 1) * 2] = 0

        for x in range(11):
            value = x + 2
            if self.check_column(value) > 0 and not(value in self.fullValues):
                self.fullValues.append(value)
                if player == 1:
                    self.playerOneWins += 1
                else:
                    self.playerTwoWins += 1

    def hypo_end_turn(self, player, save):
        hypomatrix = self.nnMatrix.copy()
        if not save:
            hypomatrix[:, (player - 1) * 2] = 0
        else:
            hypomatrix[:, (player - 1) * 2 + 1] = hypomatrix[:, (player - 1) * 2 + 1] - hypomatrix[:, (player - 1) * 2]
            hypomatrix[:, (player - 1) * 2] = 0
        return hypomatrix

    def player_solid_position(self, player, value):
        # A neural network try
        x = value - 2
        y = (player - 1) * 2 + 1
        value_to_return = self.nnMatrix[x, y]

        return value_to_return

    def player_mid_turn_position(self, player, value):
        # A neural network try
        x = value - 2
        y = (player - 1) * 2
        value_to_return = self.nnMatrix[x, y] - self.nnMatrix[x, y + 1]

        return value_to_return

    def return_nn_matrix(self):
        return self.nnMatrix

    def readable_matrix(self, player):
        mat = np.ones([13, 11]) * -1
        nn_col_index = 0
        if (
            player == 1):  # NOTE: one of the iterations is unnecessary. use conditional for second half when while condition > 0?
            nn_col_index = 0
        else:
            nn_col_index = 2
        # for 2: #
        mat = np.ones([13, 11]) * -1
        start_row = 12
        end_row = 10
        col = 0
        num_of_loops = 3  # start at 3 for 2s
        count = 1
        while (end_row >= 0):
            row = 12
            for x in range(0, num_of_loops):
                mat[row][col] = 0
                if (end_row > 0):
                    mat[row][10 - col] = 0
                row -= 1
                count += 1
            i = int(self.nnMatrix[col][nn_col_index])
            j = int(self.nnMatrix[col][nn_col_index + 1])
            if (i == 0 and j > 0 and j < num_of_loops):  # after nn_matrix is reset
                mat[13 - num_of_loops + j][col] = 1
            elif (i != 0 and j == num_of_loops):
                # if distance from cap is not zero, but distance from end is max
                mat[12 - i + 1][col] = 1
            elif (i == 0 and j == 0):
                mat[13 - num_of_loops][col] == 1  # if player won last column, put piece at end

            elif (i != 0 and j != num_of_loops):
                # if distance from cap is not zero but distance from end is not zero either
                mat[12 - i - j][col] = 1
            i = int(self.nnMatrix[10 - col][nn_col_index])
            j = int(self.nnMatrix[10 - col][nn_col_index + 1])
            if (i == 0 and j > 0 and j < num_of_loops):
                mat[13 - num_of_loops + j][10 - col] = 1
            elif (i != 0 and j == num_of_loops):
                # if distance from cap is not zero, but distance from end is max
                mat[12 - i + 1][10 - col] = 1
            elif (i == 0 and j == 0):
                mat[13 - num_of_loops][10 - col] == 1  # if player won last column, put piece at end
            elif (i != 0 and j != num_of_loops):
                # if distance from cap is not zero but distance from end is not zero either
                mat[12 - i - j][10 - col] = 1
            end_row -= 2
            num_of_loops += 2
            col += 1

        return mat

    def return_pure_matrix(self):
        return self.nnMatrix

    def aha(self):
        print(self.nnMatrix)
