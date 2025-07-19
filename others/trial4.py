def mining(board, dimension, row, column, second_life):
    checked.append([row, column])

    if board[row][column] == '| 💣 |':
        if second_life:
            print("You hit a mine! But you have a second life! Be careful now.")
            second_life = False  # Lose the second life
            return True, second_life
        else:
            return False, second_life
    elif int(board[row][column][2]) > 0:
        return True, second_life
        
    for r in range(max(0, row-1), min(dimension, row+2)):
        for c in range(max(0, column-1), min(dimension, column+2)):
            if [r, c] in checked:
                continue
            result, second_life = mining(board, dimension, r, c, second_life)
            if not result:
                return False, second_life

    return True, second_life

def main():
    import time
    correct_input = False
    dimension = 0
    numbombs = 0
    while correct_input == False:
        print("""Difficulty:
- Easy (9x9)
- Medium (15x15)
- Hard (22x22)""")
        inp = input('Choose difficulty: ')
        if inp.lower() == 'easy':
            dimension = 9 #9 rows and 9 columns
            numbombs = 3
            correct_input = True
                  
        elif inp.lower() == 'medium':
            dimension = 16
            numbombs = 30
            correct_input = True
        
        elif inp.lower() == "hard":
            dimension = 22
            numbombs = 99
            correct_input = True
    
    board = bomb_planting(dimension, numbombs)
    board = evaluate_bomb(board, dimension)  # Check surrounding cells if it has bombs

    second_life = True  # Initialize second_life

    while len(checked) < (dimension**2 - numbombs):
        print('')
        output = user_board(board, dimension)
        if len(flagged) == numbombs:
            correct_bombs = 0
            for i in flagged:
                if board[i[0]][i[-1]] == '| 💣 |':
                    correct_bombs += 1
            
            if correct_bombs == numbombs:
                break

        printout(output)
        
        bomb_display = numbombs - len(flagged)
        print('Bombs:', bomb_display)
        mode = input('''Modes: Dig (D), Flag (F), Unflag (UF), Questionmark (Q), Unquestionmark (UQ)
Choose (D, F, UF, Q, UQ): ''')

        if mode.lower() == 'd' or mode.lower() == 'dig':
            row, column = int(), int()
            while True:
                cell_input = input('Where to dig (row, column): ').split(", ") #2, 3 = row 2 column 3
                try: 
                    row, column = (int(cell_input[0])-1), (int(cell_input[-1])-1)
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number in correct format.")
            
            if output[row][column] == '| 🚩 |':
                flagged.remove([row, column])

            if [row, column] in checked:
                continue

            safe, second_life = mining(board, dimension, row, column, second_life)
            if not safe:
                print(colors.num6 + "YOU LOSE HAHAHAHAHAHHAHA LMAO😊😊😊!!" + colors.return_color)
                time.sleep(2)  # To allow the player to react that they have lost
                printout(board)
                break
            
        elif mode.lower() == 'f' or mode.lower() == 'flag':
            flag(output)

        elif mode.lower() == 'uf' or mode.lower() == 'unflag':
            cell = input('Choose which cell to Unflag (row, column): ').split(', ')
            row, column = int(cell[0])-1, int(cell[-1])-1
            if output[row][column] == '| 🚩 |':
                flagged.remove([row, column])
            else:
                print(colors.num6 + 'There is no flag there' + colors.return_color)

        elif mode.lower() == 'q' or mode.lower() == 'questionmark' or mode.lower() == 'question':
            question(output)

        elif mode.lower() == 'uq' or mode.lower() == 'unquestion' or mode.lower() == 'unquestionmark':
            cell = input('Choose which cell to Unquestionmark (row, column): ').split(', ')
            row, column = int(cell[0])-1, int(cell[-1])-1
            if output[row][column] == '| ? |':
                questioned.remove([row, column])
            else:
                print(colors.num6 + 'There is no Questionmark there' + colors.return_color)
                
        else:  # If the player's input for mode is invalid
            print('''
Invalid input!
Please try again''')
            time.sleep(2)  # To allow the player to react to the invalid input for mode

    if safe:
        print(colors.num3 + 'YOU WIN, CONGRATS!!⭐⭐⭐' + colors.return_color)
        time.sleep(2)  # To allow the player to react that they have won
main()
