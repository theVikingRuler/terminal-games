import random, os, time
NUM_ROWS = 6 # number of rows in the BOARD
NUM_COLS = 7 # number of columns in the BOARD
NUM_PLAYERS = 2 # number of players, min: 2, max: 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']
NORMAL_CELL = " "
GAME_POINT = 4 # number of matches required to win the game
COL_IDS = [ chr(65+idx) for idx in range(NUM_COLS) ] # ['A', 'B', 'C', ...]
CURRENT_TURN = int()
BOARD = list()



"""
______________________________________________________________

            CORE PROGRAM LOGIC
______________________________________________________________
"""


def pre():
    """
        clears screen
        can be extended to include welcome message at the start of game
    """
    is_board_possible() # checks if the board is within the dimensions
    is_player_count_possible() # checks if 4 checkers can be formed
    is_game_possible() # checks if player count exceeds or fall shorts of the boundary NUM_PLAYERS in [2, 5]
    clear_screen()


def is_board_possible() -> None:
    """
        cols in the board has a boundary condition: max(NUM_COLS) = 26
        min(rows) and min(cols) are covered by is_game_possible()
    """
    if NUM_COLS > 26:
        print("Invalid board. A board can have a maximum of 26 columns.")
        quit()
    return None

def is_game_possible() -> None:
    """
        a connect4 is possible if the first player is theoretically able to make a connect
    """
    if NUM_ROWS*NUM_COLS < GAME_POINT * NUM_PLAYERS:
        print("Play is not possible. Please either increase the board size or reduce the player count.")
        quit()
    return None

def is_player_count_possible():
    """
        NUM_PLAYERS has boundary conditions:
            a) min(NUM_PLAYERS) = 2
            b) max(NUM_PLAYERS) = 5 
    """
    if 2 <= NUM_PLAYERS <= 5:
        return None
    print("Invalid player count:", NUM_PLAYERS)
    print("Minimum 2 players required!" if NUM_PLAYERS < 2 else "Maximum 5 players allowed!")
    quit()


def change_turn() -> None:
    # changes player's turn
    global CURRENT_TURN
    CURRENT_TURN = (CURRENT_TURN + 1) % NUM_PLAYERS
    return None


def checker_present(coords: list(), checker: str) -> bool:
    # checks if the desired checker is present on the given coordinate
    return True if BOARD[coords[0]][coords[1]] == checker else False

def place_checker(col: int = 2) -> list():
    global BOARD
    row = 0 # start on the first row
    change = True # initiate the condition of the loop
    while change:
        change = False # assume that the loop cannot move forward
        if row < NUM_ROWS-1 and BOARD[row+1][col] == NORMAL_CELL: # the column is partially filled
            row = row + 1
            change = True
        elif BOARD[0][col] != NORMAL_CELL: # the column is already filled
            handle_filled_col()
            return []
    # place the checker on the required row
    BOARD[row][col] = CHECKERS[CURRENT_TURN]
    return [row, col] # return the [row, col]


def is_game_over(count):
    """
        the game is over when the sequential count of checkers is equal to 4
    """
    return True if count == GAME_POINT else False



"""
______________________________________________________________

            INPUT & INPUT VALIDATION FUNCTIONS
______________________________________________________________
"""


def input_col() -> str:
    """
        inputs column from the user, validates and returns the column
    """
    col_str = input(f"Player {CURRENT_TURN + 1}, please enter a column: ") # user-entered value for column
    while not validate_col(col_str):
        col_str = input("Invalid input. Please enter a column: ")
    return col_str

def validate_col(col_str: str) -> bool:
    if col_str not in COL_IDS:
        return False
    return True

def handle_filled_col():
    """
        switches player turn if an already-filled column is entered
    """
    print("Turn skipped. Avoid entering a completely filled column.")
    wait_time(2)
    change_turn()
    game_status()


"""
______________________________________________________________

                OUTPUT FUNCTIONS
______________________________________________________________
"""

def clear_screen():
    """
        calls the clear command on terminal
        useful during debugging by commenting os.system('clear') and instead adding pass
    """
    os.system("clear")


def wait_time(seconds: int = 2):
    """
        freezes the terminal for the desired seconds
        useful to show the changes to the user
    """
    time.sleep(seconds)


# prints horizontal line of the form +--+--+--...
def horizontal_line() -> None:
    print("\n+", end="")
    for j in range(NUM_COLS):
        print("---+", end="")
    print()
    return None

# prints the column headers
def header_row() -> None:
    print(" ", end="")
    for char in COL_IDS:
        print(" ", char, " ", sep="", end=" ")
    return None

def show_board(BOARD_list: list()) -> None:
    """
        prints any rowxcol gridBOARD with rowsxcols
    """
    header_row() # prints the header row A B C ...
    horizontal_line() # prints a horizontal line immediately after
    for row in range(NUM_ROWS):
        print("|", end="")
        for col in range(NUM_COLS):
            print(" ", BOARD_list[row][col] , " ", sep="", end="|")
        horizontal_line()
    return None

def game_status():
    """
        displays game status that includes cleaning the screen, displaying the board, and player's turn
    """
    clear_screen()
    show_board(BOARD)


def game_round():
    """
        handles the logic for each game round
        conditions:
            a) search_for_connect is called only when a connect is theoretically possible, i.e., first player has played at least four moves
            b) a game ends in a draw when moves equals the number of cells (NUM_ROWS * NUM_COLS)
    """
    moves = 1
    
    while moves <= NUM_ROWS*NUM_COLS: # runs until draw
        col_str = input_col() # inputs a column
        
        curr_coords = place_checker(COL_IDS.index(col_str)) # places checker, if possible, and returns coordinates

        if curr_coords == []: # fully filled column: if the checker was not placed
            continue

        game_status() # prints the board

        if moves > NUM_PLAYERS * (GAME_POINT - 1) and search_for_connect(curr_coords): # checks for connect
            print("Player", CHECKERS[CURRENT_TURN], "won!") # display winner
            quit() # stops all operations and exits
        else:
            change_turn() # changes player's turn
            moves = moves + 1 # increases move
    print("Game over! It is a draw!")



"""
______________________________________________________________

            MOVEMENT AND SEARCH FUNCTIONS
______________________________________________________________

    we define movements in four directions. diagonal can be found by a combination of any two of (up, down) and (left, right)
    abbreviation:
        lu: left and up -> shifts to diagonal to the upper left
        ru: right and up -> shifts to diagonal to the upper right
        lb: left and down -> shifts to diagonal to the lower left
        rb: right and down -> shifts to diagonal to the lower right
"""

def right(row: int, col: int) -> list():
    return [row, col+1]

def left(row: int, col: int) -> list():
    return [row, col-1]

def up(row: int, col: int) -> list():
    return [row-1, col]

def down(row: int, col: int) -> list():
    return [row+1, col]

def diagonal_lu(row: int, col: int) -> list():
    return [row-1, col-1]

def diagonal_lb(row: int, col: int) -> list():
    return [row+1, col-1]

def diagonal_ru(row: int, col: int) -> list():
    return [row-1, col+1]

def diagonal_rb(row: int, col: int) -> list():
    return [row+1, col+1]

def move_to_lu(coords: list(), checker) -> list():
    """
        travels to the leftmost upper diagonal as long as a checker is found
    """
    prev_coords = coords
    row = coords[0]
    col = coords[1]
    new_coords = coords
    while row >= 0 and col >= 0 and checker_present(new_coords, checker):
        prev_coords = [row, col]
        new_coords = diagonal_lu(row, col)
        row = new_coords[0]
        col = new_coords[1]
    return prev_coords

def move_to_ru(coords: list(), checker) -> list():
    """
        travels to the rightmost upper diagonal as long as a checker is found
    """
    prev_coords = coords
    new_coords = coords
    row = coords[0]
    col = coords[1]
    while row >= 0 and col < NUM_COLS and checker_present(new_coords, checker):
        prev_coords = [row, col]
        new_coords = diagonal_ru(row, col)
        row = new_coords[0] # may be at location where the id doesn't match the current player
        col = new_coords[1]
    return prev_coords

def move_to_left(coords: list(), checker) -> list():
    """
        moves to the leftmost col in the same row as long as a checker is found
    """
    row = coords[0]
    col = coords[1]
    prev_coords = [row, col]
    while col >= 0 and checker_present([row, col], checker):
        prev_coords = [row, col]
        new_coords = left(row, col)
        row = new_coords[0]
        col = new_coords[1]
    return prev_coords


def search_ltr(coords: list(), checker: str) -> bool:
    """
        initial: leftmost col having the same checker
        final: rightmost col having the same checker
        condition: all cells must have the same checker
        counts: number of cells
        game is over if count = 4 else continues
    """
    new_coords = move_to_left(coords, checker)
    count = 0
    row = new_coords[0]
    col = new_coords[1]
    while col < NUM_COLS and BOARD[row][col] == CHECKERS[CURRENT_TURN]:
        new_coords = right(row, col)
        row = new_coords[0]
        col = new_coords[1]
        count = count + 1
    return is_game_over(count)

def search_utd(coords: list(), checker: str) -> bool:
    """
        we begin our search from the current coords as checkers are always placed from the top
    """
    count = 0
    row = coords[0]
    col = coords[1]
    new_coords = coords
    while row < NUM_ROWS and checker_present(new_coords, checker):
        new_coords = down(row, col)
        row = new_coords[0]
        col = new_coords[1]
        count = count + 1
    return is_game_over(count)
    

def search_lutrb(coords: list(), checker: str) -> bool:
    new_coords = move_to_lu(coords, checker)
    count = 0
    row = new_coords[0]
    col = new_coords[1]
    while row < NUM_ROWS and col < NUM_COLS and BOARD[row][col] == CHECKERS[CURRENT_TURN]:
        new_coords = diagonal_rb(row, col)
        row = new_coords[0]
        col = new_coords[1]
        count = count + 1
    return is_game_over(count)


def search_rutlb(coords: list(), checker: str) -> bool:
    new_coords = move_to_ru(coords, checker)
    count = 0
    row = new_coords[0]
    col = new_coords[1]
    while row < NUM_ROWS and col >= 0 and checker_present(new_coords, checker):
        new_coords = diagonal_lb(row, col)
        row = new_coords[0]
        col = new_coords[1]
        count = count + 1
    return is_game_over(count)


def search_for_connect(coords: list()):
    """
        we search if four checkers connect in the following directions:
            a) left to right
            b) up to down
            c) upper left diagonal to lower right diagonal
            d) upper right diagonal to lower left diagonal

        to speed search, we can rank the searches
            a) in the first search, we give each an equal rank and hence, the order is: ltr, utd, lutrb, rutlb
            b) if any direction has 3 checkers, we insert it to the first position of the list potential_connects[['ltr', 'lutrb', 'utd', 'rutlb']]
            c) subsequent searches are based on priority as defined in potential_connects
    """
    checker = CHECKERS[CURRENT_TURN]
    if search_ltr(coords, checker):
        return True
    if search_utd(coords, checker):
        return True
    if search_lutrb(coords, checker):
        return True
    if search_rutlb(coords, checker):
        return True
    return False



"""
______________________________________________________________

                    MAIN GAME BLOCK
______________________________________________________________
"""

def main():
    global BOARD, CURRENT_TURN
    BOARD = [ [ NORMAL_CELL for col in range(NUM_COLS) ] for row in range(NUM_ROWS) ] # create a 2D BOARD with NUM_ROWS*NUM_COLS cells, each cell representing " "
    CURRENT_TURN = random.randint(0,NUM_PLAYERS-1)
    pre()
    show_board(BOARD)
    game_round()

main()
