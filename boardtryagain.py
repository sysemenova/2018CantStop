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
        print("Sorry, this is currently unusable")
        # These lines force pycharm not to scream at me; ignore them
        self.nnMatrix = self.nnMatrix
        return player

    def return_pure_matrix(self):
        return self.boardMatrix

    def aha(self):
        # print(self.readable_matrix(1))
        # print()
        # print(self.readable_matrix(2))
        print(self.nnMatrix)
