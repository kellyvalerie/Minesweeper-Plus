second_life = True #initiate second life function

def mining(board, dimension, row, column, second_life):
    checked.append([row, column])

    if board[row][column] == '| 💣|': # if the user hit a mine
        if second_life: # and the user have a second life
            print("You hit a mine! But you have a second life! Be careful now.") # warning
            second_life = False  # use up the second life
            return True, second_life
        else:
            return False, second_life
    elif int(board[row][column]) > 0: # from the original mine.py
        return True, second_life
        
    for r in range(max(0, row-1), min(dimension, row+2)):
        for c in range(max(0, column-1), min(dimension, column+2)):
            if [r, c] in checked:
                continue
            result, second_life = mining(board, dimension, r, c, second_life)
            if not result:
                return False, second_life
