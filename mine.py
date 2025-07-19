import random
import time
dimension = 0
checked = [] #location of user input (dig)
flagged = [] #location of flags
questioned = [] #location of questionmarks
closed = [] #location of closed cell from mystery effect
bomb_locations = [] #location of bombs
revealed_bomb_location = [] #location of bombs revealed from mystery effect
row_description = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14}
second_life = False #initialization of second_life from mystery effect
user_board = [] #board which is visible to the user

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

#Function to validate the input
def validate_input(name):
    while True:
        if name == 'immunity':
            cell_input = input(f'Choose which cell to dig with immunity (example: A1) : ')
        else:
            cell_input = input(f"Choose which cell to {name} (example: A1) : ")
        if len(cell_input) >= 2 and cell_input[0].isalpha() and cell_input[1:].isdigit() and cell_input[0].upper() in row_description:
            if row_description[cell_input[0].upper()] < dimension and 1 <= int(cell_input[1:]) <= dimension:
                row = row_description[cell_input[0].upper()]  # Convert the row to its corresponding index
                column = int(cell_input[1:]) - 1  # Convert column to zero-based index
                if [row, column] in checked:
                    print(f"\nYou cannot {name} a dug cell")
                    continue
                elif [row, column] in  closed:
                    print(f"This cell is closed. You cannot {name} a closed cell")
                else:
                    return row, column
            else: #if the input is not valid
                print("\nPlease enter a valid input.")
                continue
        else: #if the length is less than 2 or the first letter is not an alphabet or the remaining letters are not digits
            print("\nPlease enter a valid input.")
            continue

def bomb_planting(numbombs):
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
def get_neighbour_bomb(board, row, column):
    bombs_found = 0
    # max returns bigger number between 0 and row-1 or column-1 if it's is < 0 (negative)
    # min returns smaller number between dimension and row+2 or column+2 if it's is > dimension
    for r in range(max(0, row-1), min(dimension, row+2)): # max and min to not be out of range for the Index
        for c in range(max(0, column-1), min(dimension, column+2)):
            if r == row and c == column:
                continue
            elif board[r][c] == '💣':
                bombs_found += 1
    return bombs_found

#Function to evaluate the board and return a board with numbers of surrounding bombs
def evaluate_board(board):
    for row in range(dimension):
        for column in range(dimension):
            if board[row][column] == '💣': #check if it's a bomb
                bomb_locations.append([row, column])
                continue #skip to next column
            else: #if it's not a bomb
                number = get_neighbour_bomb(board, row, column)
                board[row][column] = number
                #the cell is now the count of the neighbouring bombs
    return board

#Function to keep opening up the cells until hit a cell that has surrounding bombs/cells with numbers
#If cells with neighbouring bombs is not found, keep diging until found    
def mining(board, row, column):
    #Return False if the user hits a bomb
    #Return True if the user is still safe or doesn't hit a bomb
    global second_life
    user_input = [row, column]
    checked.append(user_input)# the row and column will be append to checked(the data of user inputs)

    if board[row][column] == '💣':
        if second_life == True:
            print("You hit a mine!💔 But you have a second life! Be careful now.")
            time.sleep(2)
            checked.remove([row, column])
            second_life = False  # Lose the second life
            return True
        else:
            return False

    elif int(board[row][column]) > 0:
        return True
       
    # if board[row][column] == 0 and it's not a bomb
    # max returns bigger number between 0 and row-1 or column-1 if it's is < 0 (negative)
    # min returns smaller number between dimension and row+2 or column+2 if it's is > dimension
    for r in range(max(0, row-1), min(dimension, row+2)): # max and min to not be out of range for the Index
        for c in range(max(0, column-1), min(dimension, column+2)):
            if [r, c] in checked:
                continue
            result = mining(board, r, c)
            if not result:
                return False
    return True

#function to print the board or userboard
def printout(board):
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
            if board[row][column] == '\033[48;5;196m💣\033[0m':
                print('║\033[48;5;196m \033[0m'+ board[row][column], end='')
                continue
            elif board[row][column] == '💣' or board[row][column] == '🚩':
                print('║ '+ board[row][column], end='')
                continue
            print('║', board[row][column], end=' ')
        print('║')
        if row != dimension-1:
            print('╠═══' + '╬═══' * dimension+ '╣')
    print('╚═══' + '╩═══' * dimension + '╝')#bottom borders

#function for User's board that has invisible bombs, and invisible numbers(numbers of surrounding bombs)
def generateuser_board(board): #user's board
    global user_board
    for row in range(dimension):
        for column in range(dimension):
            #check if the row,column (input) is in checked(the user_input data)
            if [row, column] in closed:
                user_board[row][column] = '\033[91mX\033[0m'
            elif [row, column] in checked:
                    num = get_neighbour_bomb(board, row, column)
                    #output certain numbers with certain colors
                    if num == 0:
                        user_board[row][column] = str(colors.num0)
                    elif num == 1:
                        user_board[row][column] = str(colors.num1)
                    elif num == 2:
                        user_board[row][column] = str(colors.num2)
                    elif num == 3:
                        user_board[row][column] = str(colors.num3)
                    elif num == 4:
                        user_board[row][column] = str(colors.num4)
                    elif num == 5:
                        user_board[row][column] = str(colors.num5)
                    elif num == 6:
                        user_board[row][column] = str(colors.num6)
                    elif num == 7:
                        user_board[row][column] = str(colors.num7)
                    elif num == 8:
                        user_board[row][column] = str(colors.num8)

                    # check if it's a flag, in case a flag cell is opened up because of 0
                    if [row, column] in flagged:
                        flagged.remove([row, column])
            
            #if that cell is flagged or questionmarked or a revealed bomb, don't change the color
            elif [row, column] in revealed_bomb_location:
                user_board[row][column] = '💣'
                if [row, column] in  flagged:
                    flagged.remove([row, column])
                elif [row, column] in  questioned:
                    questioned.remove([row, column])
            elif [row, column] in flagged:
                user_board[row][column] = '🚩'
            elif [row, column] in questioned:
                user_board[row][column] = '?'
            else:
                user_board[row][column] = ' '
    return user_board


#FLAG FUNCTION
def flag():
    row, column = validate_input('flag')
    if [row, column] in flagged:
        print('This cell is already flagged')
        time.sleep(2)
    elif [row, column] in revealed_bomb_location:
        print('\nYou cannot flag a revealed bomb')
        time.sleep(2)
    elif [row, column] not in checked:
        if [row, column] in questioned:
            questioned.remove([row, column])
        flagged.append([row, column])
    elif [row, column] in checked:
        print('You cannot flag a dug cell')
        time.sleep(2)

#UNFLAG FUNCTION
def unflag():
    row, column = validate_input('unflag') 

    if [row, column] in flagged:
        flagged.remove([row, column])
    else:
        print('There is no flag there')
        time.sleep(2)

#QUESTIONMARK FUNCTION
def question():
    row, column = validate_input('questionmark') 
    if [row, column] in questioned:
        print('This cell is already questionmarked')
        time.sleep(2)
    elif [row, column] in revealed_bomb_location:
        print('\nYou cannot questionmark a revealed bomb')
        time.sleep(2)
    elif [row, column] not in checked:
        #if user questionmarked a flag, automatically remove the flag, and questionmark the cell
        if [row, column] in flagged:
            flagged.remove([row, column])
        questioned.append([row, column])
    elif [row, column] in checked:
        print('You cannot Questionmark a dug cell')
        time.sleep(2)

#UNQUESTIONMARK FUNCTION
def unquestion():
    row, column = validate_input('unquestionmark') 

    if [row, column] in questioned:
        questioned.remove([row, column])
    else:
        print('There is no Questionmark there')
        time.sleep(2)

# to close 1 cell
def close_one_cell():
    unchecked = []
    for row in range(dimension):
        for column in range(dimension):
            if [row, column] in checked:
                continue
            else:
                unchecked.append([row, column]) #append to unchhecked (list of unrevealed cells)          
    while True :
        closed_cell_location = random.choice(unchecked)#randomly choose a unrevealed cell
        if closed_cell_location not in bomb_locations:
            break
    row, column = closed_cell_location[0], closed_cell_location[1]
    closed.append([row, column])

# to safely reveal one bomb for user
def reveal1bomb():
    if len(bomb_locations) > 0:          
        revealed_bomb = random.choice(bomb_locations)
        row, column = revealed_bomb[0], revealed_bomb[1]
        revealed_bomb_location.append([row, column])
        bomb_locations.remove([row, column])
    
def bomb_sweep(board):
    print('\nBombsweep: Clears a 3x3 area of the board without triggering any mines.')
    row, column = validate_input('bomb sweep')
    bombs_found = []

    # loop through the 3x3 area centered at (row, column)
    # max returns bigger number between 0 and row-1 or column-1 if it's is < 0 (negative)
    # min returns smaller number between dimension and row+2 or column+2 if it's is > dimension
    for r in range(max(0, row - 1), min(dimension, row + 2)):
        for c in range(max(0, column-1), min(dimension, column+2)):
            # check if there's a bomb at the current cell and add it to the list if true
            if board[r][c] == '💣':
                bombs_found.append([r, c])
                revealed_bomb_location.append([r, c])
                bomb_locations.remove([r, c])

            # mark the cell as checked to reveal it on the user board
            elif [r, c] not in checked:
                checked.append([r, c])

    # report any bombs found in the swept area
    if len(bombs_found) > 0:
        print("Bombs detected in the following locations: ", end='')
        for bomb in bombs_found:
            bombrow = chr(ord('A') + int(bomb[0]))
            bombcol = bomb[1] +1
            print(f"{bombrow}{bombcol}", end='')
            if bomb != bombs_found[-1]:
                print(', ', end='')
    else:
        print("No bombs found in the 3x3 area.")
    
    print()
    time.sleep(2)
            
def safe_dig(board):
    global user_board
    row, column = validate_input('immunity')
        
    # Check if the cell is a bomb
    if board[row][column] == '💣':
        print("\033[31mWarning\033[0m: This cell contains a bomb.")
        time.sleep(2)

    else:
        # Reveal the cell when it's safe
        if [row, column] not in checked: #if the cell is not a bomb
            checked.append([row, column])

def main():
    global dimension
    global second_life
    correct_input = False
    
    start_limited_digs = False
    extra_limited_digs = 0

    print('''
***********************************************************''')
    print(r'''  __        __   _                            _             
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
            remaining_time = 240
            correct_input = True
                  
        elif inp.lower() == 'hard':
            dimension = 15
            numbombs = 30
            remaining_time = 480
            correct_input = True

        else:#incorrect input
            print('''
Invalid input for difficulty!
Please try again
''')     
    #plant bombs randomly
    board = bomb_planting(numbombs)
    # check surrounding cells if it has bombs
    # basically board =  the key answer of the board, with the bombs and number of bombs surrounding that cell (hidden from the user)
    board = evaluate_board(board)
    
    #make user board with the size of dimension*dimension
    global user_board
    user_board = [[' ' for i in range(dimension)] for j in range(dimension)]

    #initialize remaining input
    remaining_digs = dimension * dimension

    #initialize game time
    game_time = time.time()

    #keeps the program going, while all cells except the bombs are not open yet
    while len(checked) < (dimension**2 - numbombs - len(closed)):
        correct_bombs = 0

        #if the number of flags = number of bombs, check if they are all correct(bombs)
        if len(flagged) == numbombs - len(revealed_bomb_location):
            for i in flagged:
                if board[i[0]][i[1]] == '💣':
                    correct_bombs += 1
            # if all flags are bombs, end game because they won
            if correct_bombs == numbombs - len(revealed_bomb_location):
                break
        
        if len(revealed_bomb_location) == numbombs:
            safe = True
            break
        
        #if limited input mystery effect is started
        if start_limited_digs == True:
            unrevealed = []
            for row in range(dimension):
                for column in range(dimension):
                    if [row, column] in checked:
                        continue
                    unrevealed.append([row, column]) #append to unchhecked (list of unrevealed cells) 
            remaining_digs = len(unrevealed) - 2 - numbombs - len(revealed_bomb_location) - extra_limited_digs #total remaining digs for the user = number closed cells + number of revealed bombs -2(from initialization)
        
        if remaining_digs < 0:
            print("""
🙀 Oh no! You are out of inputs! 💔
😢 Better luck next time! 😢
✨ Keep smiling and try again! ✨
    """)
            return 0 

        #if the user is out of time, or out of inputs end game
        if remaining_time <= 0:
            break
        
        print('')
        #generate user's board
        user_board = generateuser_board(board)

        printout(user_board)#call printout function to print the user's board
        
        #Print remaining time
        minutes = int(remaining_time // 60)  # Use integer division for minutes
        seconds = int(remaining_time % 60)    # Use modulus for seconds
        print(f"Remaining time: {minutes} minute{'s' if minutes != 1 else ''} {seconds} second{'s' if seconds != 1 else ''}")
        start_time = time.time()

        #display the number of bombs, = actual number of bombs for the difficulty - how many flags are on the board
        bomb_display = numbombs - len(flagged) - len(revealed_bomb_location)
        if flagged in revealed_bomb_location: #if the user flag a revealed bomb
            bomb_display += 1
        print('Bombs:', bomb_display)

        if second_life == True:
            print('Lives: ❤️❤️')
        
        if start_limited_digs == True: 
            print('Remaining digs:', remaining_digs)#after printing bombs and before displaying Modes

        #ask user to input what mode
        mode = input('''Modes: Dig (D), Flag (F), Unflag (UF), Questionmark (Q), Unquestionmark (UQ), End (E)
Choose (D, F, UF, Q, UQ, E): ''')

        #End game
        if mode.lower() == 'e' or mode.lower() == 'end':
            print('\nGame Ended')
            return 0

        #Dig mode
        if mode.lower() == 'd' or mode.lower() == 'dig':
            row, column = validate_input('dig')


            #if user digs a flag, automatically remove the flag, and dig the cell
            if [row, column] in flagged:
                flagged.remove([row, column])
            
            safe = mining(board, row, column)  
            #check for their input(dug cell), if they are safe or not
            
            #if user digs a bomb
            if safe == False:
                print("""
💔 Oh no! You lost! 💔
😢 Better luck next time! 😢
✨ Keep smiling and try again! ✨
""")
                time.sleep(2)
                #if the user digs a bomb, highlight the dug bomb
                board[row][column] = f'\033[48;5;196m💣\033[0m'
                printout(board)
                return 0

            #if the cell is > 0 and it's not a bomb
            if board[row][column] != '💣':
                if board[row][column] > 0:
                    if random.random() < 0.50:  #50% chance
                        #keep looping if the user doesn't input a valid answer
                        while True:
                            takeeffect = input('You got a random mystery effect. Take mystery effect? (yes/no): ')
                            if takeeffect.lower() == 'yes' or takeeffect.lower() == 'y' or takeeffect.lower() == 'no' or takeeffect.lower() == 'n':
                                break
                            print('Please enter a valid answer (yes/no)')
                            continue    

                        if takeeffect.lower() == 'yes' or takeeffect.lower() == 'y':
                            effect_list = ['reveal 1 bomb', 'second life', 'add time', 'bompsweep', 'immunity', 'limited digs', 'close 1 cell', 'reduce time']
                            weights = [15, 15, 20, 15, 20, 5, 5, 5]
                            chosen_effect = random.choices(effect_list, weights=weights, k = 1) #randomly choose mystery effect, with different probabilities(weight)
                            if chosen_effect[0] == 'reveal 1 bomb':
                                print('I will reveal one bomb for you! 🥳✨🌟')
                                time.sleep(2)
                                reveal1bomb()
                            elif chosen_effect[0] == 'second life':
                                if second_life == False:
                                    print('You got a second life! 🥳✨🌟')
                                elif second_life == True:
                                    print("""You got a second life! 🥳✨🌟
The maximum lives is 2. Use your second life to gain another! 😢""")
                                time.sleep(2)
                                second_life = True
                            elif chosen_effect[0] == 'add time':
                                print('Wohoo! You got extra 30s 🥳✨🌟')
                                time.sleep(2)
                                remaining_time += 30
                            elif chosen_effect[0] == 'bompsweep':
                                print('You got a bomb sweep! 🥳✨🌟')
                                time.sleep(2)
                                bomb_sweep(board)
                            elif chosen_effect[0] == 'immunity':
                                print('You got immunity! 🥳✨🌟!')
                                time.sleep(2)
                                safe_dig(board)
                            elif chosen_effect[0] == 'limited digs':
                                if start_limited_digs == False:
                                    print('You have limited digs! 😈😈😈')
                                elif start_limited_digs == True:
                                    print("You got limited digs again. Minus 2 extra dig! 😈😈")
                                    extra_limited_digs += 2
                                time.sleep(2)
                                start_limited_digs = True
                            elif chosen_effect[0] == 'close 1 cell':
                                print("I will close a cell, No inputs allowed to this cell! 😈😈")
                                time.sleep(2)
                                close_one_cell()
                            elif chosen_effect[0] == 'reduce time':
                                print('Your time got reduced by 30s! 😈😈')
                                time.sleep(2)
                                remaining_time -= 30                
            
        elif mode.lower() == 'f' or mode.lower() == 'flag':
            flag()

        elif mode.lower() == 'uf' or mode.lower() == 'unflag':
            unflag()

        elif mode.lower() == 'q' or mode.lower() == 'questionmark' or mode.lower() == 'question':
            question()

        elif mode.lower() == 'uq' or mode.lower() == 'unquestion' or mode.lower() == 'unquestionmark':
            unquestion()
                
        else:#Invalid input for mode
            print('''
Invalid input!
Please try again''')
            time.sleep(2)

        #Timer:  
        end_time = time.time()
        elapsed_time = end_time - start_time  # Calculate elapsed time
        remaining_time -= int(elapsed_time)  # Decrease remaintime by the elapsed time

    #outside of while loop
    #if the user is out of time, end game
    if remaining_time <= 0:
        print("\n⏰ Time was up! 💔 You Lose!!! 😢")
        return 0
    
    elif safe == True:
        print("""
🎉🎊 Hooray! You Win! 🎊🎉
🌟✨ You navigated the mines like a pro! ✨🌟
🥳 Congrats on your victory! 🥳
""")
        time.sleep(2)
        printout(board)
        time_won = time.time()
        time_taken = time_won - game_time
        minutes_won = int(time_taken // 60)
        seconds_won = int(time_taken % 60)
        print(f"You won in: {minutes_won} minute{'s' if minutes_won != 1 else ''} {seconds_won} second{'s' if seconds_won != 1 else ''}")    

main()
