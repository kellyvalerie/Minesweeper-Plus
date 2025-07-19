import random
import time
import re
checked = []
flagged = []
questioned = []
row_description = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21}

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

#function to randomly plant powerups
def power_planting(board, dimension, numpower):
    powerups = 0
    powerlocations = []
    while powerups < numpower:
        location = random.randint(0, (dimension**2 - 1))
        #if 10 dimension, total number of cells are 100
        #for example if location = 62
        row = location // dimension
        #row = 6
        column = location % dimension
        #column = 2
        if board[row][column] == '💣' or [row, column] in powerlocations:
            continue
        powerlocations.append([row, column])
        powerups +=1
    return powerlocations

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
def mining(board, dimension, row, column, powerlocation):
    user_input = [row, column]
    checked.append(user_input)# the row and column will be append to checked(the data of user inputs)

    if board[row][column] == '💣':
        return False

    elif int(board[row][column]) > 0:
        return True

        
    #if there no neighbouring bombs yet / board[row][column] == 0
    for r in range(max(0, row-1), min(dimension, row+2)): # max and min to not be out of range
        for c in range(max(0, column-1), min(dimension, column+2)):
            if [r, c] in checked:
                continue
            if not mining(board, dimension, r, c, powerlocation):
                return False
    return True

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
def user_board(board, dimension): #user's board
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
        cell_input = input('Choose which cell to Flag (row, column): ').split(', ')
        try:
            row, column = row_description[cell_input[0]], (int(cell_input[-1])-1)
            if row >= dimension or row < 0 or column < 0 or column >= dimension:
                print("Please enter a valid input.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number in correct format.")
    if [row, column] not in checked:
        flagged.append([row, column])
        outputboard[row][column] = '🚩'
    elif [row, column] in checked:
        print('You cannot flag a dug cell')
        time.sleep(2)

#UNFLAG FUNCTION
def unflag(outputboard, dimension):
    row, column = int(), int()
    #loop until get the correct input format
    while True:
        cell_input = input('Choose which cell to Unflag (row, column): ').split(', ')
        try: 
            row, column = row_description[cell_input[0]], (int(cell_input[-1])-1)
            if row >= dimension or row < 0 or column < 0 or column >= dimension:
                print("Please enter a valid input.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number in correct format.")

    if outputboard[row][column] == '🚩':
        flagged.remove([row, column])
        outputboard[row][column] = ' '
    else:
        print('There is no flag there')
        time.sleep(2)

#QUESTIONMARK FUNCTION
def question(outputboard, dimension):
    row, column = int(), int()
    #loop until get the correct input format
    while True:
        cell_input = input('Choose which cell to Questionmark (row, column): ').split(', ')
        try: 
            row, column = row_description[cell_input[0]], (int(cell_input[-1])-1)
            if row >= dimension or row < 0 or column < 0 or column >= dimension:
                print("Please enter a valid input.")
                continue
            break
        except ValueError:
            print("Please enter a valid input in correct format.")

    if [row, column] not in checked:
        #if user questionmarked a flag, automatically remove the flag, and questionmark the cell
        if outputboard[row][column] == '🚩':
            flagged.remove([row, column])
        questioned.append([row, column])
        outputboard[row][column] = '?'
    elif [row, column] in checked:
        print('You cannot Questionmark a dug cell')
        time.sleep(2)

#UNQUESTIONMARK FUNCTION
def unquestion(outputboard, dimension):
    row, column = int(), int()
    
    #loop until get the correct input format
    while True:
        cell_input = input('Choose which cell to Unquestionmark (row, column): ').split(', ')
        try: 
            row, column = row_description[cell_input[0]], (int(cell_input[-1])-1)
            if row >= dimension or row < 0 or column < 0 or column >= dimension:
                print("Please enter a valid input.")
                continue
            break
        except ValueError:
            print("Please enter a valid input in correct format.")

    if outputboard[row][column] == '?':
        questioned.remove([row, column])
        outputboard[row][column] = ' '
    else:
        print('There is no Questionmark there')
        time.sleep(2)

def main():
    import time
    correct_input = False
    while correct_input == False:
        print("""Difficulty:
- Easy (9x9)
- Hard (15x15)""")
        inp = input('Choose difficulty: ')
        if inp.lower() == 'easy':
            dimension = 9 #9 rows and 9 columns
            numbombs = 8
            num_powerups = 5
            remaining_time = 30 #seconds
            correct_input = True
                  
        elif inp.lower() == 'hard':
            dimension = 16
            numbombs = 30
            num_powerups = 10
            remaining_time = 300 #second, 5 minute
            correct_input = True
    
    board = bomb_planting(dimension, numbombs)
    #bombs planted randomly
    board = evaluate_bomb(board, dimension)
    # check surrounding cells if it has bombs
    # basically board = the key answer of the board, with the bombs and number of bombs surrounding that cell (hidden from the user)
    
    powerlocations = power_planting(board, dimension, num_powerups)
    print('Powerup locations: ', powerlocations)
    #location of powerups
    #keeps the program going, while all cells except the bombs are not open yet
    while len(checked) < (dimension**2 - numbombs) or remaining_time > 0:
        if remaining_time <= 0:
            print("\nTime is Up! You Lose!!")
            return 0
        #output empty new minesweeper board for user
        print('')
        output = user_board(board, dimension)
        
        #if the number of flags = number of bombs, check if they are all correct(bombs)
        if len(flagged) == numbombs:
            correct_bombs = 0
            for i in flagged:
                if board[i[0]][i[-1]] == '💣':
                    correct_bombs += 1
            # if all flags are bombs, end game because they won
            if correct_bombs == numbombs:
                break

        printout(output, dimension)#call printout function
        minutes = int(remaining_time // 60)  # Use integer division for minutes
        seconds = int(remaining_time % 60)    # Use modulus for seconds
        print(f"\nRemaining time: {minutes} minute{'s' if minutes != 1 else ''} {seconds} second{'s' if seconds != 1 else ''}")
        start_time = time.time()

        #display the number of bombs, = actual number of bombs for the difficulty - how many flags are on the board
        bomb_display = numbombs - len(flagged)
        print('Bombs:', bomb_display)

        #ask user for input
        mode = input('''Modes: Dig (d), Flag (f), Unflag (uf), Questionmark (q), Unquestionmark (uq), Restart(r)
Choose (d, f, uf, q, uq, r): ''')

        #end game
        if mode.lower() == 'r' or mode.lower() == 'restart':
            return 0

        #if dig mode
        if mode.lower() == 'd' or mode.lower() == 'dig':
            row, column = int(), int()

            #loop until get the correct input format
            while True:
                cell_input = input('Where to dig (example: A1): ')
        
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
                else:
                    print("\nPlease enter a valid input.")
                    
            #if user digs a flag, automatically remove the flag, and dig the cell
            if output[row][column] == '🚩':
                flagged.remove([row, column])
            elif [row, column] in powerlocations:
                print("yes")

            #if user input same cell, then continue the loop
            if [row, column] in checked:
                continue
            
            #check for their input(dug cell), if they are safe or not
            safe = mining(board, dimension, row, column, powerlocations)
            if safe == False:
                print("""💔 Oh no! You lost! 💔
😢 Better luck next time! 😢
✨ Keep smiling and try again! ✨
""")
                time.sleep(3)#To allow the player to react that he has lost
                printout(board, dimension)#Call printout function
                break

            if int(board[row][column]) > 0:
                if [row, column] in powerlocations:
                    valid_powerup_input = False
                    #loop while the input format is incorrect
                    while valid_powerup_input == False:
                        takepowerup = input('You got a random powerup, take powerup? (yes/no): ')
                        if takepowerup.lower() == 'yes' or takepowerup.lower() == 'no' or takepowerup.lower() == 'y' or takepowerup.lower() == 'n':
                            valid_powerup_input = True
                            break
                        print('Please input a valid answer (yes/no)')
                    #call power_roullete function, to generate random power up for the user
                    #powerup = power_roulette()
            
        elif mode.lower() == 'f' or mode.lower() == 'flag':
            flag(output, dimension)

        elif mode.lower() == 'uf' or mode.lower() == 'unflag':
            unflag(output, dimension)

        elif mode.lower() == 'q' or mode.lower() == 'questionmark' or mode.lower() == 'question':
            question(output, dimension)

        elif mode.lower() == 'uq' or mode.lower() == 'unquestion' or mode.lower() == 'unquestionmark':
            unquestion(output, dimension)
                
        else:#If the player's input for mode is invalid
            print('''
Invalid input!
Please try again''')
            time.sleep(2)#To allow the player to react that he has an invalid input for mode
        end_time = time.time()
        elapsed_time = end_time - start_time  # Calculate elapsed time
        remaining_time -= elapsed_time  # Decrease remaintime by the elapsed time
    #outside of while loop
    if safe == True:
        print("""🎉🎊 Hooray! You Win! 🎊🎉
🌟✨ You navigated the mines like a pro! ✨🌟
🥳 Congrats on your victory! 🥳
""")
        time.sleep(3)#To allow the player to react that he has won
        printout(board, dimension)

main()


