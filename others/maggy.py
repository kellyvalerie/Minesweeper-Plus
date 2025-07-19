import random
import time
checked = []
flagged = []
questioned = []
bombing = []
unchecked = []
row_description = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21}
input_left_start = False
#'\033[48;5;196m'+board[row][column]+"\033[0m"
# ANSI escape codes for text color
class colors:
    num0 = "\033[37m0\033[0m"  #White for 0
    num1 = "\033[34m1\033[0m"  #Blue for 1
    num2 = "\033[32m2\033[0m"  #Green for 2
    num3 = "\033[31m3\033[0m"  #Red for 3
    num4 = "\033[33m4\033[0m"  #Yellow for 4
    num5 = "\033[35m5\033[0m"  #Magenta for 5
    num6 = "\033[36m6\033[0m"  #Cyan for 6
    num7 = "\033[38;5;202m7\033[0m"  #Light red for 7
    num8 = "\033[38;5;196m8\033[0m"  #Light red for 8
    return_color="\033[0m" #Reset color back to default

#Function for randomly plant bombs on the board
def validate_answer(name): 
    while True:
        cell_input = input("Choose which cell to {name} (example: A1) : ")
        if len(cell_input) >= 2 and cell_input[0].isalpha() and cell_input[1:].isdigit():
            if cell_input[0] in row_description and 0 < int(cell_input[1:]) <= dimension:
                center_row = row_description[cell_input[0]]  # Convert the row to its corresponding index
                center_column = int(cell_input[1:]) - 1  # Convert column to zero-based index
                if [center_row, center_column] in checked:
                    print("\nYou cannot {name} a dug cell")
                    continue
                else:
                    break
            else:
                print("\nPlease enter a valid input.")
                continue

def bomb_planting(dimension, numbombs):
    board = [[' ' for i in range(dimension)]  for j in range(dimension)]
    bombs = 0
    while bombs < numbombs:
        location = random.randint(0, (dimension**2 - 1))
        #if 10 dimension, total number of cells are 100
        #for example if location = 62
        row = location // dimension
        #row = 6
        column = location % dimension
        #column = 2
        if board[row][column] == '💣':
            continue
        board[row][column] = '💣'
        bombs +=1
    return board

#Function to count the neighbouring bombs of that cell
def get_neighbour_bomb(board, dimension, row, column):
    num = 0
    for r in range(max(0, row-1), min(dimension-1, row+1)+1): # max and min to not be out of range
        for c in range(max(0, column-1), min(dimension-1, column+1)+1):
            if r == row and c == column:
                continue
            elif board[r][c] == '💣':
                num += 1
    return num

def get_neighbour_flag(output, dimension, row, column, board):
    numflag=0
    for r in range(max(0, row-1), min(dimension-1, row+1)+1): # max and min to not be out of range
        for c in range(max(0, column-1), min(dimension-1, column+1)+1):
            if r == row and c == column:
                continue
            elif output[r][c] == colors.num6+'🚩'+colors.return_color and board[r][c]=='💣':
                numflag += 1
    return numflag

#Function to evaluate the board and return a board with numbers of surrounding bombs
def evaluate_bomb(board, dimension):
    for r in range(dimension):
        for c in range(dimension):
            if board[r][c] == '💣': #check if it's a bomb
                continue #skip to next column
            else: #if it's not a bomb
                number = get_neighbour_bomb(board, dimension, r, c)
                board[r][c] = number
                #the cell is now the count of the neighbouring bombs
    return board

#Function to keep open up the cells until hit a cell that has surrounding bombs/cells with numbers
    # if didnt found any neighbouring, keep diging until get it    
def mining(board, dimension, row, column, powerlocation, second_life):
    user_input = [row, column]
    checked.append(user_input)# the row and column will be append to checked(the data of user inputs)

    if board[row][column] == '💣':
        if second_life:
            print("You hit a mine! But you have a second life! Be careful now.")
            second_life = False  # Lose the second life
            return True, second_life
        else:
            return False, second_life

    elif int(board[row][column]) > 0:
        return True, second_life
       
    #if there no neighbouring bombs yet / board[row][column] == 0
    for r in range(max(0, row-1), min(dimension, row+2)): # max and min to not be out of range
        for c in range(max(0, column-1), min(dimension, column+2)):
            if [r, c] in checked:
                continue
            result, second_life = mining(board, dimension, r, c, second_life, powerlocation)
            if not result:
                return False
    return True, second_life

def safemining(board, dimension, row, column, output):
    for r in range(max(0, row-1), min(dimension, row+2)): # max and min to not be out of range
        for c in range(max(0, column-1), min(dimension, column+2)):
            if [r, c] in checked or [r, c] in flagged:
                continue
            if int(board[r][c][2]) > 0:
                checked.append([r, c])
            if int(board[r][c][2])== 0:
                checked.append([r, c])
                safemining(board, dimension, r, c, output)

#function to print the board or userboard
def printout(board, dimension):
    #print top borders
    print('╔═══' + '╦═══' * dimension + '╗')
    #column description (1, 2, 3,...)
    print('║   ', end='')
    for j in range(dimension):
        if j+1 > 9:
            print(f'║ {j+1}', end='')
            continue
        print(f'║ {j+1} ', end='')
    print('║')
    print('╠═══' + '╬═══' * dimension+ '╣')
    for row in range(dimension):
        #row descriptions (a, b, c,...)
        print(f'║ {chr(ord("A") + row)} ', end='')
        for column in range(dimension):
            #if it's a bomb or a flag delete 1 space in the box (because a flag and a bomb uses 2 space)
            if board[row][column] == '💣' or board[row][column] == '🚩':
                print('║ '+ board[row][column], end='')
                continue
            print('║', board[row][column], end=' ')
        print('║')
        if row != dimension-1:
            print('╠═══' + '╬═══' * dimension+ '╣')
    print('╚═══' + '╩═══' * dimension + '╝')#bottom borders

#function for User's board that has invisible bombs, and invisible numbers(numbers of surrounding bombs)
def generateuser_board(board, dimension): #user's board
    user_board = [[' ' for i in range(dimension)] for j in range(dimension)]
    for row in range(dimension):
        for column in range(dimension):
            
            #check if the row,column (input) is in checked(the user_input data)
            if [row, column] in checked:
                num = get_neighbour_bomb(board, dimension, row, column)

                #output certain numbers with certain colors
                if num == 0:
                    user_board[row][column] = str(colors.num0 + colors.return_color)
                elif num == 1:
                    user_board[row][column] = str(colors.num1 + colors.return_color)
                elif num == 2:
                    user_board[row][column] = str(colors.num2 + colors.return_color)
                elif num == 3:
                    user_board[row][column] = str(colors.num3 + colors.return_color)
                elif num == 4:
                    user_board[row][column] = str(colors.num4 + colors.return_color)
                elif num == 5:
                    user_board[row][column] = str(colors.num5 + colors.return_color)
                elif num == 6:
                    user_board[row][column] = str(colors.num6 + colors.return_color)
                elif num == 7:
                    user_board[row][column] = str(colors.num7 + colors.return_color)
                elif num == 8:
                    user_board[row][column] = str(colors.num8 + colors.return_color)
                elif num == 9:
                    user_board[row][column] = str(colors.num9 + colors.return_color)
            
            #if that cell is flagged
            elif [row, column] in flagged:
                user_board[row][column] = '🚩'
            elif [row, column] in questioned:
                user_board[row][column] = '?'
            else:
                user_board[row][column] = ' '
    return user_board


#FLAG FUNCTION
def flag(outputboard, dimension):
    row, column = int(), int()
    #loop until get the correct input format
    while True:
        cell_input = input("Choose which cell to flag (example: A1) : ")
        if len(cell_input) >= 2 and cell_input[0].isalpha() and cell_input[1:].isdigit():
            if cell_input[0] in row_description and 0 < int(cell_input[1:]) <= dimension:
                center_row = row_description[cell_input[0]]  # Convert the row to its corresponding index
                center_column = int(cell_input[1:]) - 1  # Convert column to zero-based index
                if [center_row, center_column] in checked:
                    print("\nYou cannot flag a dug cell")
                    continue
                else:
                    break
            else:
                print("\nPlease enter a valid input.")
                continue
            
    if [row, column] not in checked:
        flagged.append([row, column])
        outputboard[row][column] = '🚩'
    elif [row, column] in checked:
        print('You cannot flag a dug cell')

#UNFLAG FUNCTION
def unflag(outputboard, dimension):
    row, column = int(), int()
    #loop until get the correct input format
    while True:
        cell_input = input("Choose which cell to unflag : ")
        if len(cell_input) >= 2 and cell_input[0].isalpha() and cell_input[1:].isdigit():
            if cell_input[0] in row_description and 0 < int(cell_input[1:]) <= dimension:
                center_row = row_description[cell_input[0]]  # Convert the row to its corresponding index
                center_column = int(cell_input[1:]) - 1  # Convert column to zero-based index
                if [center_row, center_column] in checked:
                    print("\nYou cannot unflag a dug cell")
                    continue
                else:
                    break
            else:
                print("\nPlease enter a valid input.")
                continue

    if outputboard[row][column] == '🚩':
        flagged.remove([row, column])
        outputboard[row][column] = ' '
    else:
        print('There is no flag there')

#QUESTIONMARK FUNCTION
def question(outputboard, dimension):
    row, column = int(), int()
    #loop until get the correct input format

    while True:
        cell_input = input('Choose which cell to Questionmark or (cancel): ')

        # Check if input is long enough, and use parentheses for methods
        if len(cell_input) >= 2 and cell_input[0].isalpha() and cell_input[1:].isdigit():
            if cell_input[0] in row_description and 0 < int(cell_input[1:]) <= dimension:
                row = row_description[cell_input[0]]  # Convert the row to its corresponding index
                column = int(cell_input[1:]) - 1  # Convert column to zero-based index
                if [row, column] in checked:
                    print("\nYou cannot input a dug cell")
                    continue
                else:
                    break
            else:
                print("\nPlease enter a valid input.")
                continue
        elif cell_input.lower() == 'cancel':
            break
        else:
            print("\nPlease enter a valid input.")

    if [row, column] not in checked:
        #if user questionmarked a flag, automatically remove the flag, and questionmark the cell
        if outputboard[row][column] == '🚩':
            flagged.remove([row, column])
        questioned.append([row, column])
        outputboard[row][column] = '?'
    elif [row, column] in checked:
        print('You cannot Questionmark a dug cell')

#UNQUESTIONMARK FUNCTION
def unquestion(outputboard, dimension):
    row, column = int(), int()
    
    #loop until get the correct input format
    while True:
        cell_input = input("Choose which cell to Unquestionmark : ")
        if len(cell_input) >= 2 and cell_input[0].isalpha() and cell_input[1:].isdigit():
            if cell_input[0] in row_description and 0 < int(cell_input[1:]) <= dimension:
                center_row = row_description[cell_input[0]]  # Convert the row to its corresponding index
                center_column = int(cell_input[1:]) - 1  # Convert column to zero-based index
                if [center_row, center_column] in checked:
                    print("\nYou cannot dig a dug cell")
                    continue
                else:
                    break
            else:
                print("\nPlease enter a valid input.")
                continue

    if outputboard[row][column] == '?':
        questioned.remove([row, column])
        outputboard[row][column] = ' '
    else:
        print('There is no Questionmark there')
def answerboard(row,column,board,dimension):
    answerboard=board
    highlight=f'\033[48;5;196m{board[row][column]}\033[0m'
    #answerboard[row][column]=highlight.strip()
    return answerboard
    
def randomreveal(dimension,board,output):
    #it should be initialized putside the function
    for i in range(dimension):
        for j in range(dimension):
            if [i,j] not in checked:
                unchecked.append([i,j])          
    chosen_row,chosen_column=random.choice(unchecked)#randomly reveal a cell
    checked.append([chosen_row,chosen_column])
    output[chosen_row][chosen_column]=board[chosen_row][chosen_column]
    safe = mining(board, dimension, chosen_row, chosen_column, output)
    if safe == False:
        print("""💔 Oh no! You lost! 💔
😢 Better luck next time! 😢
✨ Keep smiling and try again! ✨
""")
        answer_board=answerboard(chosen_row, chosen_column, board, dimension)
        printout(answer_board)
    return output

def reveal1bomb(dimension,board,output,user_board, bomb_display):
    #it should be initialized putside the function
    for i in range(dimension):
        for j in range(dimension):
            if board[i][j]=='💣':
                bombing.append([i,j])          
    chosen_row,chosen_column=random.choice(bombing)
    output[chosen_row][chosen_column]=board[chosen_row][chosen_column]#randomly choose to reveal a bomb
    checked.append([chosen_row,chosen_column])
    bombing.remove([chosen_row,chosen_column])
    user_board[chosen_row][chosen_column]=board[chosen_row][chosen_column]
    bomb_display -=1
    return user_board
    
def add_time(remaining_time):
    remaining_time += 30
    return remaining_time

def reduce_time(remaining_time):
    remaining_time -= 30
    return remaining_time
    
def bomb_sweep(board, dimension):
    while True:
        cell_input = input("Choose the center for Bomb Sweep : ")
        if len(cell_input) >= 2 and cell_input[0].isalpha() and cell_input[1:].isdigit():
            if cell_input[0] in row_description and 0 < int(cell_input[1:]) <= dimension:
                center_row = row_description[cell_input[0]]  # Convert the row to its corresponding index
                center_column = int(cell_input[1:]) - 1  # Convert column to zero-based index
                if [center_row, center_column] in checked:
                    print("\nYou cannot dig a dug cell")
                    continue
                else:
                    break
            else:
                print("\nPlease enter a valid input.")
                continue

            # ensure that the selected center is not on the edge of the board
            if center_row <= 0 or center_row >= dimension - 1 or center_column <= 0 or center_column >= dimension - 1:
                print("Invalid center! It should not be on the edge of the board. Please choose a valid center.")
                continue  # go back to prompt the player again

            # list to store any bombs found in the 3x3 area
            bombs_found = []

            # loop through the 3x3 area centered at (center_row, center_column)
            for r in range(center_row - 1, center_row + 2):
                for c in range(center_column - 1, center_column + 2):
                    # check if there's a bomb at the current cell and add it to the list if true
                    if board[r][c] == '💣':
                        bombs_found.append((r, c))

                    # mark the cell as checked to reveal it on the user board
                    if [r, c] not in checked:
                        checked.append([r, c])

            # report any bombs found in the swept area
            if bombs_found:
                print("Bombs detected in the following locations:")
                for bomb in bombs_found:
                    print(f"Bomb at row {bomb[0]}, column {bomb[1]}")
            else:
                print("No bombs found in the 3x3 area.")

            # mark Bomb Sweep as used only after a valid sweep
            global bomb_sweep_used
            bomb_sweep_used = True
            break  # exit the function after a valid sweep
            
def safe_click(board, dimension, checked):
    while True:
        try:
            cell = input("Choose a cell to Safe Click (row, column): ").split(", ")
            if len(cell_input) >= 2 and cell_input[0].isalpha() and cell_input[1:].isdigit():
                if cell_input[0] in row_description and 0 < int(cell_input[1:]) <= dimension:
                    center_row = row_description[cell_input[0]]  # Convert the row to its corresponding index
                    center_column = int(cell_input[1:]) - 1  # Convert column to zero-based index
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
            
# random choose a powerup        
def choose_powerup(dimension, board, output, bomb_display, remaining_time):
    mylist=[0,0,1,1,2,2,3,3,4,4,5,6,7]
    chosen_number=random.choice(mylist)
    global input_left_start
    # if chosen_number==0:
    #     print('I will reveal one bomb for you 🥳✨🌟')
    #     user_board = [[' ' for i in range(dimension)] for j in range(dimension)]
    #     reveal1bomb(dimension, board, output, user_board, bomb_display)
    if chosen_number==1:
        print('You get a second life! 🥳✨🌟')
        second_life = True
    # if chosen_number==2:
    #     print('You get added time!🥳✨🌟')
    #     remaining_time = add_time(remaining_time)
    if chosen_number==3:
        print('You get a bomb sweep 🥳✨🌟!')
        bomb_sweep(board, dimension)
    if chosen_number ==4:
        print('It is safe_click🥳✨🌟!')
        safe_click = True
    if chosen_number==6:
        global input_left_start
        print('Got limited times to flag😈😈😈')
        input_left_start=True
    # if chosen_number==7:
    #     print('I will randomly reveal a cell for you, maybe it is a bomb 😈😈')
    #     randomreveal(dimension,board,output)
    return board, output, bomb_display, remaining_time, second_life
def main():
    correct_input = False
    inputnum=0
    i=0
    input_total = 0
    bomb_sweep_available = True
    second_life = False
    print('''
***********************************************************''')
    print(r'''
  __        __   _                            _             
  \ \      / /__| | ___ ___  _ __ ___   ___  | |_ ___       
   \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \      
    \ V  V /  __/ | (_| (_) | | | | | |  __/ | || (_) |     
 __  \_/\_/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/      
|  \/  (_)_ __   ___  _____      _____  ___ _ __   ___ _ __ 
| |\/| | | '_ \ / _ \/ __\ \ /\ / / _ \/ _ \ '_ \ / _ \ '__|
| |  | | | | | |  __/\__ \\ V  V /  __/  __/ |_) |  __/ |   
|_|__|_|_|_| |_|\___||___/ \_/\_/ \___|\___| .__/ \___|_|   
|  _ \| |_   _ ___                         |_|              
| |_) | | | | / __|                                         
|  __/| | |_| \__ \                                         
|_|   |_|\__,_|___/ 
''')
    print('''***********************************************************
''')

    while correct_input == False:
        print("""Difficulty:
- Easy (9x9)
- Hard (15x15)""")
        inp = input('Choose difficulty: ')
        if inp.lower() == 'easy':
            dimension = 9 #9 rows and 9 columns
            numbombs = 8
            num_powerups = 15
            remaining_time = 60
            correct_input = True
                  
        elif inp.lower() == 'hard':
            dimension = 16
            numbombs = 30
            num_powerups = 10
            remaining_time = 300
            correct_input = True

        else:#incorrect input
            print('''
Invalid input for difficulty!
Please try again
''')
         
    
    board = bomb_planting(dimension, numbombs)
    #bombs planted randomly
    board = evaluate_bomb(board, dimension)
    # check surrounding cells if it has bombs
    # basically board = the key answer of the board, with the bombs and number of bombs surrounding that cell (hidden from the user)

    #keeps the program going, while all cells except the bombs are not open yet
    while len(checked) < (dimension**2 - numbombs) or remaining > 0:
        if remaining_time <= 0:
            print("\nTime is Up! You Lose!!")
            return 0
        #output empty new minesweeper board for user
        print('')
        output = generateuser_board(board, dimension)

        #if the number of flags = number of bombs, check if they are all correct(bombs)
        if len(flagged) == numbombs:
            correct_bombs = 0
            for i in flagged:
                if board[i[0]][i[-1]] == '💣':
                    correct_bombs += 1
            # if all flags are bombs, end game because they won
            if correct_bombs == numbombs:
                break
        if i==0 and input_left_start:
            correct_bombs = 0
            for i in flagged:
                if board[i[0]][i[-1]] == '💣':
                    correct_bombs += 1
            input_total=(numbombs-correct_bombs)*2
            i=1
        inputleft=input_total-inputnum
        if input_left_start:
            if inputleft==0:
                print("""💔 Oh no! You lost! 💔
😢 Better luck next time! 😢
✨ Keep smiling and try again! ✨
""")
               
                printout(board, dimension)
                safe=False
                break

        printout(output, dimension)#call printout function
        minutes = int(remaining_time // 60)  # Use integer division for minutes
        seconds = int(remaining_time % 60)    # Use modulus for seconds
        print(f"\nRemaining time: {minutes} minute{'s' if minutes != 1 else ''} {seconds} second{'s' if seconds != 1 else ''}")
        start_time = time.time()

        #display the number of bombs, = actual number of bombs for the difficulty - how many flags are on the board
        bomb_display = numbombs - len(flagged) 
        print('Bombs:', bomb_display)
        if input_left_start:
            print('Input left: ',inputleft)#after printing Bombs and before displaying Modes

        #ask user for input
        mode = input('''Modes: Dig (D), Flag (F), Unflag (UF), Questionmark (Q), Unquestionmark (UQ), End (E)
Choose (D, F, UF, Q, UQ, E): ''')
        if input_left_start:
            inputnum+=1 #after input

        #End game
        if mode.lower() == 'e' or mode.lower() == 'end':
            print('''
Game Ended
''')
            return 0

        #Dig mode
        if mode.lower() == 'd' or mode.lower() == 'dig':
            row, column = int(), int()

            #loop until get the correct input format
            while True:
                cell_input = input('Where to dig (example: A1) or (cancel): ')
        
                # Check if input is long enough, and use parentheses for methods
                if len(cell_input) >= 2 and cell_input[0].isalpha() and cell_input[1:].isdigit():
                    if cell_input[0] in row_description and 0 < int(cell_input[1:]) <= dimension:
                        row = row_description[cell_input[0]]  # Convert the row to its corresponding index
                        column = int(cell_input[1:]) - 1  # Convert column to zero-based index
                        if [row, column] in checked:
                            print("\nYou cannot dig a dug cell")
                            continue
                        else:
                            break
                    else:
                        print("\nPlease enter a valid input.")
                        continue
                elif cell_input.lower() == 'cancel':
                    break
                else:
                    print("\nPlease enter a valid input.")

            #if user digs a flag, automatically remove the flag, and dig the cell
            if output[row][column] == '🚩':
                flagged.remove([row, column])
            #if user input same cell, then continue the loop
            if [row, column] in checked:
                if int(get_neighbour_flag(output, dimension, row, column, board))==int(board[row][column]):
                    safemining(board, dimension, row, column, output)   
            else: 
                safe = mining(board, dimension, row, column, output, second_life)  
            #check for their input(dug cell), if they are safe or not
            
            if safe == False:
                print("""💔 Oh no! You lost! 💔
😢 Better luck next time! 😢
✨ Keep smiling and try again! ✨
""")
                answer_board=answerboard(row, column, board, dimension)
                printout(answer_board, dimension)
                break

            if isinstance(board[row][column],int) :
                if int(board[row][column]) > 0:
                    if random.random() < 0.90:  # 25% chance
                        takepowerup = input('You got a random powerup. Take powerup? (Yes/No): ')
                        if takepowerup.lower() == 'yes' or takepowerup.lower() == 'y':
                        #call choose_powerup function, to generate random power up for the user
                            board, output, bomb_display, remaining_time, second_life = choose_powerup(dimension, board, output, bomb_display, remaining_time)
                            valid_powerup_input = True
                            break
                        elif takepowerup.lower() == 'no' or takepowerup.lower() == 'n':
                            valid_powerup_input = True
                            break
                        print('Please input a valid answer (yes/no)')
                
                
            
        elif mode.lower() == 'f' or mode.lower() == 'flag':
            flag(output, dimension)

        elif mode.lower() == 'uf' or mode.lower() == 'unflag':
            unflag(output, dimension)

        elif mode.lower() == 'q' or mode.lower() == 'questionmark' or mode.lower() == 'question':
            question(output, dimension)

        elif mode.lower() == 'uq' or mode.lower() == 'unquestion' or mode.lower() == 'unquestionmark':
            unquestion(output, dimension)
                
        else:#Invalid input for mode
            print('''
Invalid input!
Please try again''')
         
        end_time = time.time()
        elapsed_time = end_time - start_time  # Calculate elapsed time
        remaining_time -= elapsed_time  # Decrease remaintime by the elapsed time

    #outside of while loop
    if safe == True:
        print("""🎉🎊 Hooray! You Win! 🎊🎉
🌟✨ You navigated the mines like a pro! ✨🌟
🥳 Congrats on your victory! 🥳
""")
       
        printout(board, dimension)


main()


