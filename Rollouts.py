import numpy as np

def roll_dice():
    return np.random.randint(1, high=7, size=4)

def generate_moves(board, roll): # value = index + 2
    """
    Given the current boardstate and the results from a roll,
    this function generates the possible combinations of moves.
    If the roll is something like [1, 3, 4, 5], an output could be
    [[4, 9], [5, 8], [6, 7]], but depending on the boardstate, it could be
    [[4, 9], [7]] if only 4, 7, and 9 are valid moves.
    If no moves are valid, the function will return None.
    """
    roll_sum = sum(roll)
    valid_moves = []
    sum01 = roll[0] + roll[1]
    valid_moves.append([sum01, roll_sum - sum01])
    # Ensures there are no repeats in the list
    sum02 = roll[0] + roll[2]
    if sum02 != sum01 and sum02 != roll_sum - sum01:
        valid_moves.append([sum02, roll_sum - sum02])
    sum03 = roll[0] + roll[3]
    if sum03 != sum01 and sum03 != roll_sum - sum01 and sum03 != sum02 and sum03 != roll_sum - sum02:
        valid_moves.append([sum03, roll_sum - sum03])
    #print(valid_moves)
    i = 0
    while i < len(valid_moves):
        """
         Reasons to reject
             1. Row completed
             2. Double move when 1 away from end
             3. 3 white peices already placed & not one of them
                 Note: If 2 placed, may need to split up a combination
                       into 2
        """
        active_values = board.get_active_values()
        current_player = board.get_current_player()
        if len(valid_moves[i]) == 2 and valid_moves[i][0] == valid_moves[i][1]: # Double move
            row = valid_moves[i][0]
            if row in active_values or len(active_values) < 3:
                if board.get_absolute_matrix()[row - 2, 2 * current_player - 1] == 1: # If spaces left == 1
                    valid_moves[i].pop(0) # Remove one of them
        elif len(active_values) == 2 and valid_moves[i][0] not in active_values and valid_moves[i][1] not in active_values:
            valid_moves.append([valid_moves[i].pop(1)]) # Splits up combination into 2
        j = 0
        while j < len(valid_moves[i]):
            if valid_moves[i][j] in board.get_full_values(): # Row completed
                valid_moves[i].pop(j)
            elif len(active_values) == 3 and valid_moves[i][j] not in active_values: # 3 white pieces already placed
                valid_moves[i].pop(j)
            else:
                j += 1
        if len(valid_moves[i]) == 0:
            valid_moves.pop(i)           
    if len(valid_moves) == 0:
        return None
    return valid_moves