

import random
import time
checked = []
flagged = []
questioned = []
row_description = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21}

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
        print(f'║ {chr(ord("a") + row)} ', end='')
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

def add_time(remaintime):
    remaintime -= 10
    return remaintime

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
    correct_input = False
    while correct_input == False:
        print("""Difficulty:
- Easy (9x9)
- Medium (15x15)
- Hard (22x22)""")
        inp = input('Choose difficulty: ')
        if inp.lower() == 'easy':
            dimension = 9 #9 rows and 9 columns
            numbombs = 8
            num_powerups = 5
            remaintime = 30
            correct_input = True
                  
        elif inp.lower() == 'medium':
            dimension = 16
            numbombs = 30
            num_powerups = 10
            correct_input = True
        
        elif inp.lower() == "hard":
            dimension = 22
            num_powerups = 30
            numbombs = 99
            correct_input = True
    
    board = bomb_planting(dimension, numbombs)
    #bombs planted randomly
    board = evaluate_bomb(board, dimension)
    # check surrounding cells if it has bombs
    # basically board = the key answer of the board, with the bombs and number of bombs surrounding that cell (hidden from the user)
    
    powerlocations = power_planting(board, dimension, num_powerups)
    print('Powerup locations: ', powerlocations)
    #location of powerups

    add_time(remaintime)
    #keeps the program going, while all cells except the bombs are not open yet
    while len(checked) < (dimension**2 - numbombs):
        while remaintime:
            if remaintime <= 0 :
                print("Time is up! You Lose")
                return
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
            
            #display the number of bombs, = actual number of bombs for the difficulty - how many flags are on the board
            bomb_display = numbombs - len(flagged)
            print('Bombs:', bomb_display)

            # start the time
            start_time = time.time()
            time.sleep(1)

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
                    cell_input = input('Where to dig (row, column): ').split(", ") #2, 3 = row 2 column 3
                    try: 
                        row, column = row_description[cell_input[0]], (int(cell_input[-1])-1)
                        if row >= dimension or row < 0 or column < 0 or column >= dimension:
                            print("Please enter a valid input.")
                            continue
                        if [row, column] in checked:
                            print("You cannot dig a dug cell")
                            continue
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid number in correct format.")
                        
                #if user digs a flag, automatically remove the flag, and dig the cell
                if output[row][column] == '🚩':
                    flagged.remove([row, column])
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

            remaintime -= elapsed_time  # Decrease remaintime by the elapsed time

            # Calculate minutes and seconds
            minutes = int(remaintime // 60)  # Use integer division for minutes
            seconds = int(remaintime % 60)    # Use modulus for seconds
            print(f"Remaining time: {minutes} minute{'s' if minutes != 1 else ''} {seconds} second{'s' if seconds != 1 else ''}")


    #outside of while loop
    if safe == True:
        print("""🎉🎊 Hooray! You Win! 🎊🎉
🌟✨ You navigated the mines like a pro! ✨🌟
🥳 Congrats on your victory! 🥳
""")
        time.sleep(3)#To allow the player to react that he has won
        printout(board, dimension)

main()


