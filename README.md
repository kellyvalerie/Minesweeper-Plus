# Minesweeper-Plus
### What is Minesweeper?

Minesweeper is a logic puzzle game. 
The game features a grid of tiles, with hidden "mines" randomly distributed throughout the board.
The game's objective is to clear the board without detonating any mines, with help from clues about the number of neighboring mines in each cell.

(Source: Wikipedia)

---------------------------------------------------------------------------------------------------------------------------------------------------

### Cells can have one of the four states:

    1. Unopened  
    2. Dugged 
    3. Flagged
    4. Questioned

---------------------------------------------------------------------------------------------------------------------------------------------------

### How to play the Classic Minesweeper (not our version of minesweeper)?

1. The player selects a unopened cell to open it.
2. If a player opens a mined cell, the game ends. Otherwise, the opened cell will displays either a number (which indicating the number of mines the 8 surrounding cells have) or a blank tile.
3. All adjacent non-mined cells will be open automatically.
4. The player can also flag a cell, to denote that they are confident that a mine is in that place. Moreover, the player can question a cell, to denote that they are unsure whether that cell is mined or not.
5. The player wins by opening all non-mine cells without opening a mine or by flagging all the mined cells.

(Source: Wikipedia)

---------------------------------------------------------------------------------------------------------------------------------------------------

### How to play Minesweeper Plus (our version of minesweeper)?

- After starting the game, the player choose the difficulty (easy or hard) that he wants to play.
- For easy mode, the player will play the game in a 9x9 grid with 8 bombs and a time limit of 4 minutes.
- For hard mode, the player will play the game in a 15x15 grid with 30 bombs and a time limit of 8 minutes.
- After selecting the difficulty, the player can choose what to do next (Dig (D), Flag (F), Unflag (UF), Questionmark (Q), Unquestionmark (UQ), End (E)).

- Dig (D): Insert an unopened cell's coordinate to dig the cell.
- Flag (F): Insert an unflagged cell's coordinate to flag the cell.
- Unflag (UF): Insert a flagged cell's coordinate to unflag the cell.
- Questionmark (Q): Insert the coordinate of a cell that doesn't contain questionmark to questionmark the cell.
- Unquestionmark (UQ): Insert the coordinate of a cell that contains questionmark to unquestionmark the cell.
- End (E): To end the game without finishing playing


Everytime you dig a cell, there is a 50% chance to encounter a mystery effect. You can choose to take the mystery effect or not because the mystery effect isn't always something beneficial.


#### List of mystery effects:

    1. Reveal 1 bomb: Revealing one bomb's location to the player. This will help player to not choose a cell that contains a bomb.
    2. Second life: The player gets an extra life. If the player hits a bomb, he still will have one life left and can continue to play.
    3. Add time: Add 30 seconds to the time limit.
    4. Bompsweep: The player first selects any unopened cell, then all surrounding cells (includes the selected cell) will be swept, showing the status of the cells.
    5. Immunity: The player will be able to dig any undug cell without activating any bomb(if the selected cell is mined).
    6. Limited digs: The number of times to dig a cell will be limited.
    7. Close 1 cell: A random cell will be closed. The player can't take any action for the cell. Furthermore, if the surrounding of the cell has a bomb, it will not show any number.
    8. Reduce time: Minus 30 seconds to the time limit.

- Winning condition: A player wins by digging all the non-mined cells or by flagging all the bombs.
- Losing condition: A player loses by digging a bomb or running out of time.
