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
        if board[row][column] == '| 💣|':
            continue
        board[row][column] = '| 💣|'
        bombs +=1
    return board

#Function to count the neighbouring bombs of that cell
def get_neighbour_bomb(board, dimension, row, column):
    num = 0
    for r in range(max(0, row-1), min(dimension-1, row+1)+1): # max and min to not be out of range
        for c in range(max(0, column-1), min(dimension-1, column+1)+1):
            if r == row and c == column:
                continue
            elif board[r][c] == '| 💣|':
                num += 1
    return num

#Function to evaluate the board and return a board with numbers of surrounding bombs
def evaluate_bomb(board, dimension):
    for r in range(dimension):
        for c in range(dimension):
            if board[r][c] == '| 💣|': #check if it's a bomb
                continue #skip to next column
            else: #if it's not a bomb
                board[r][c] = f'| {get_neighbour_bomb(board, dimension, r, c)} |'
                #the cell is now the count of the neighbouring bombs
    return board

#Function to keep open up the cells until hit a cell that has surrounding bombs/cells with numbers
    # if didnt found any neighbouring, keep diging until get it    
def mining(board, dimension, row, column):
    # the row and column will be append in form of list inside list
    checked.append([row, column])

    if board[row][column] == '| 💣|':
        return False
    elif int(board[row][column][2]) > 0:
        return True
        
    #if there no neighbouring bombs yet / board[row][column] == 0
    for r in range(max(0, row-1), min(dimension, row+2)): # max and min to not be out of range
        for c in range(max(0, column-1), min(dimension, column+2)):
            if [r, c] in checked:
                continue
            if not mining(board, dimension, r, c):
                return False
    return True
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
                user_board[row][column] = colors.num6+'| 🚩|'+colors.return_color
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

def answerboard(row,column,board,dimension):
    answerboard=board
    answerboard[row][column]='\033[48;5;196m'+'| 💣|'+"\033[0m"
    return answerboard
# Function for Safe Click: Safely reveals a cell without risk of hitting a bomb
def safe_click(board, dimension, checked):
    while True:
        try:
            cell = input("Choose a cell to Safe Click (row, column): ").split(", ")
            row, column = int(cell[0]) - 1, int(cell[1]) - 1
            
            # Check if the cell is a bomb
            if board[row][column] == '| 💣|':
                print(colors.num6 + "Warning: This cell contains a bomb." + colors.return_color)
                 # reveal the bomb cell
                checked.append([row, column])
                return False  # This indicates the player has found a bomb
            else:
                # Reveal the cell when it's safe
                if [row, column] not in checked:
                    checked.append([row, column])
                else:
                    print("This cell is already revealed. Choose a different cell.")
                break
        except (ValueError, IndexError):
            print("Invalid input. Please enter valid row and column numbers.")

# Modify the main function to include the Safe Click option
def main():
    import time
    correct_input = False
    dimension = 0
    numbombs = 0
    while not correct_input:
        print("""Difficulty:
- Easy (9x9)
- Medium (15x15)
- Hard (22x22)""")
        inp = input('Choose difficulty: ')
        if inp.lower() == 'easy':
            dimension = 9
            numbombs = 8
            correct_input = True
        elif inp.lower() == 'medium':
            dimension = 16
            numbombs = 30
            correct_input = True
        elif inp.lower() == 'hard':
            dimension = 22
            numbombs = 99
            correct_input = True
    
    board = bomb_planting(dimension, numbombs)
    board = evaluate_bomb(board, dimension)
    
    while len(checked) < (dimension**2 - numbombs):
        print('')
        output = user_board(board, dimension)
        
        if len(flagged) == numbombs:
            correct_bombs = sum(1 for i in flagged if board[i[0]][i[-1]] == '| 💣|')
            if correct_bombs == numbombs:
                break
        
        printout(output)
        bomb_display = numbombs - len(flagged)
        print('Bombs:', bomb_display)
        
        mode = input('''Modes: Dig (D), Flag (F), Unflag (UF), Questionmark (Q), Unquestionmark (UQ), Safe Click (S)
Choose (D, F, UF, Q, UQ, S): ''')

        if mode.lower() in ['d', 'dig']:
            while True:
                try:
                    cell_input = input('Where to dig (row, column): ').split(", ")
                    row, column = int(cell_input[0]) - 1, int(cell_input[1]) - 1
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number in the correct format.")
            
            if output[row][column] == '| 🚩|':
                flagged.remove([row, column])
            
            if [row, column] in checked:
                continue
            
            safe = mining(board, dimension, row, column)
            if not safe:
                print(colors.num6 + "YOU LOSE HAHAHAHAHAHHAHA LMAO😊😊😊!!" + colors.return_color)
                time.sleep(2)
                answer_board = answerboard(row, column, board, dimension)
                printout(answer_board)
                break
        
        elif mode.lower() == 's' or mode.lower() == 'safe':
            safe_click(board, dimension, checked)

        elif mode.lower() == 'f' or mode.lower() == 'flag':
            flag(output)

        elif mode.lower() == 'uf' or mode.lower() == 'unflag':
            cell = input('Choose which cell to Unflag (row, column): ').split(', ')
            row, column = int(cell[0]) - 1, int(cell[1]) - 1
            if output[row][column] == '| 🚩|':
                flagged.remove([row, column])
            else:
                print(colors.num6 + 'There is no flag there' + colors.return_color)

        elif mode.lower() in ['q', 'questionmark', 'question']:
            question(output)

        elif mode.lower() in ['uq', 'unquestion', 'unquestionmark']:
            cell = input('Choose which cell to Unquestionmark (row, column): ').split(', ')
            row, column = int(cell[0]) - 1, int(cell[1]) - 1
            if output[row][column] == '| ? |':
                questioned.remove([row, column])
            else:
                print(colors.num6 + 'There is no Questionmark there' + colors.return_color)
                
        else:
            print('Invalid input! Please try again')
            time.sleep(2)

    if safe:
        print(colors.num3 + 'YOU WIN, CONGRATS!!⭐⭐⭐' + colors.return_color)
        time.sleep(2)

main()

