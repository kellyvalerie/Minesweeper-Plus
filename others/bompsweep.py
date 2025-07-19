def bomb_sweep(board, dimension):
    try:
        cell_input = input("Choose the center for Bomb Sweep (row, column): ").split(", ")
        center_row, center_column = int(cell_input[0]), int(cell_input[-1])

        if center_row <= 0 or center_row >= dimension - 1 or center_column <= 0 or center_column >= dimension - 1:
            print("Invalid center! It should not be on the edge of the board. Please choose a valid center.")
            return

        bombs_found = []
        for r in range(center_row - 1, center_row + 2):
            for c in range(center_column - 1, center_column + 2):
                if board[r][c] == '*':
                    bombs_found.append((r, c))
                if [r, c] not in checked:
                    checked.append([r, c])  # Mark the cell as dug/revealed

        if bombs_found:
            print("Bombs detected in the following locations:")
            for bomb in bombs_found:
                print(f"Bomb at row {bomb[0]}, column {bomb[1]}")
        else:
            print("No bombs found in the 3x3 area.")

    except ValueError:
        print("Invalid input. Please enter valid numbers for row and column.")

    print(f"Bomb Sweep used at center: ({center_row}, {center_column})")

