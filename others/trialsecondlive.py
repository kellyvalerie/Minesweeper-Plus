import random
checked = []
flagged = []
questioned = []
# ANSI escape codes for text color
class colors:
    num0="\033[0;94m"
    num1="\033[34m"
    num2="\033[36m"
    num3="\033[32m"
    num4="\033[33m"
    num5="\033[38;5;202m"
    num6="\033[31m"
    num7="\033[38;5;196m"
    num8="\033[38;5;213m"
    purple = "\033[35m"
    return_color="\033[0m"

#Function for randomly plant bombs on the board
def bomb_planting(dimension, numbombs):
    board = [['|   |' for i in range(dimension)]  for j in range(dimension)]
    bombs = 0
    while bombs < numbombs:
        location = random.randint(0, (dimension**2 - 1))
        #if 9 dimension maximum number of cells are 81 (-1 because index starts from 0)
        #for example if location = 62
        row = location // dimension
        #row = 6
        column = location % dimension
        #column = 2
        if board[row][column] == '| 💣 |':
            continue
        board[row][column] = '| 💣 |'
        bombs +=1
    return board

#Function to count the neighbouring bombs of that cell
def get_neighbour_bomb(board, dimension, row, column):
    num = 0
    for r in range(max(0, row-1), min(dimension-1, row+1)+1): # max and min to not be out of range
        for c in range(max(0, column-1), min(dimension-1, column+1)+1):
            if r == row and c == column:
                continue
            elif board[r][c] == '| 💣 |':
                num += 1
    return num

#Function to evaluate the board and return a board with numbers of surrounding bombs
def evaluate_bomb(board, dimension):
    for r in range(dimension):
        for c in range(dimension):
            if board[r][c] == '| 💣 |': #check if it's a bomb
                continue #skip to next column
            else: #if it's not a bomb
                board[r][c] = f'| {get_neighbour_bomb(board, dimension, r, c)} |'
                 #the cell is now the count of the neighbouring bombs
    return board

#Function to keep open up the cells until hit a cell that has surrounding bombs/cells with numbers
    # if didnt found any neighbouring, keep diging until get it    
def mining(board, dimension, row, column, second_life):
    # the row and column will be append in form of list inside list
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
        
    #if there no neighbouring bombs yet / board[row][column] == 0
    for r in range(max(0, row-1), min(dimension, row+2)): # max and min to not be out of range
        for c in range(max(0, column-1), min(dimension, column+2)):
            if [r, c] in checked:
                continue
            result, second_life = mining(board, dimension, r, c, second_life)
            if not result:
                return False, second_life
    return True, second_life
#make the revealed user_board more neat
def printout(user_board):
    for row in user_board:
        print(''.join(row))

#function for User's board that has invisible bombs, and invisible numbers(numbers of surrounding bombs)
def user_board(board, dimension): #user's board
    user_board = [['|   |' for i in range(dimension)] for j in range(dimension)]
    for row in range(dimension):
        for column in range(dimension):    
            if [row, column] in checked:
                user_board[row][column] = evaluate_bomb(board,dimension)[row][column]
                if get_neighbour_bomb(board, dimension, row, column)==0:
                    user_board[row][column]=colors.num0+user_board[row][column]+colors.return_color
                elif get_neighbour_bomb(board, dimension, row, column)==1:
                    user_board[row][column]=colors.num1+user_board[row][column]+colors.return_color
                elif get_neighbour_bomb(board, dimension, row, column)==2:
                    user_board[row][column]=colors.num2+user_board[row][column]+colors.return_color
                elif get_neighbour_bomb(board, dimension, row, column)==3:
                    user_board[row][column]=colors.num3+user_board[row][column]+colors.return_color
                elif get_neighbour_bomb(board, dimension, row, column)==4:
                    user_board[row][column]=colors.num4+user_board[row][column]+colors.return_color
                elif get_neighbour_bomb(board, dimension, row, column)==5:
                    user_board[row][column]=colors.num5+user_board[row][column]+colors.return_color
                elif get_neighbour_bomb(board, dimension, row, column)==6:
                    user_board[row][column]=colors.num6+user_board[row][column]+colors.return_color
                elif get_neighbour_bomb(board, dimension, row, column)==7:
                    user_board[row][column]=colors.num7+user_board[row][column]+colors.return_color
                elif get_neighbour_bomb(board, dimension, row, column)==8:
                    user_board[row][column]=colors.num8+user_board[row][column]+colors.return_color
                elif get_neighbour_bomb(board, dimension, row, column)==9:
                    user_board[row][column]=colors.num9+user_board[row][column]+colors.return_color
            elif [row, column] in flagged:
                user_board[row][column] = colors.num6+'| 🚩 |'+colors.return_color
            elif [row, column] in questioned:
                user_board[row][column] = colors.purple+'| ? |'+colors.return_color
            else:
                user_board[row][column] = '|   |'
    return user_board


#Flag function
def flag(outputboard):
    cell = input('Choose which cell to Flag (row, column): ').split(', ')
    row, column = int(cell[0])-1, int(cell[-1])-1
    if [row, column] not in checked:
        flagged.append([row, column])
    elif [row, column] in checked:
        print(colors.num6+'You cannot flag a dug cell'+colors.return_color)

#Question function
def question(outputboard):
    cell = input('Choose which cell to Questionmark (row, column): ').split(', ')
    row, column = int(cell[0])-1, int(cell[-1])-1
    if [row, column] not in checked:
        questioned.append([row, column])
    elif [row, column] in checked:
        print(colors.num6+'You cannot Questionmark a dug cell'+colors.return_color)


def main():
    second_live = True
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
    # the key answer of board (but hidden from the user)
    # board already planted with bombs
    board = evaluate_bomb(board, dimension)#check surrounding cells if it has bombs
     # Initialize second_life
    
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

            #if user input same cell, then continue the loop
            if [row, column] in checked:
                continue

            safe = mining(board, dimension, row, column, second_live)
            if safe == False:
                print(colors.num6+"YOU LOSE HAHAHAHAHAHHAHA LMAO😊😊😊!!"+colors.return_color)
                time.sleep(2)#To allow the player to react that he has lost
                printout(board)
                break
            
        elif mode.lower() == 'f' or mode.lower() == 'flag':
            flag(output)

        elif mode.lower() == 'uf' or mode.lower() == 'unflag':
            cell = input('Choose which cell to Unflag (row, column): ').split(', ')
            row, column = int(cell[0]), int(cell[-1])
            if output[row][column] == '| 🚩 |':
                flagged.remove([row, column])
            else:
                print(colors.num6+'There is no flag there'+colors.return_color)

        elif mode.lower() == 'q' or mode.lower() == 'questionmark' or mode.lower() == 'question':
            question(output)

        elif mode.lower() == 'uq' or mode.lower() == 'unquestion' or mode.lower() == 'unquestionmark':
            cell = input('Choose which cell to Unquestionmark (row, column): ').split(', ')
            row, column = int(cell[0])-1, int(cell[-1])-1
            if output[row][column] == '| ? |':
                questioned.remove([row, column])
            else:
                print(colors.num6+'There is no Questionmark there'+colors.return_color)
                
        else:#If the player's input for mode is invalid
            print('''
Invalid input!
Please try again''')
            time.sleep(2)#To allow the player to react that he has an invalid input for mode


    #outside of while loop
    if safe == True:
        print(colors.num3+'YOU WIN, CONGRATS!!⭐⭐⭐'+colors.return_color)
        time.sleep(2)#To allow the player to react that he has won

main()

