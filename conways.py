# imports
from connect import connect

from cell import Cell

from random import randint


# helper functions
def draw_board(living: list[tuple[int, int]], dead: list[tuple[int,int]]):

    list(map(lambda cell: framebuffer.pixel(cell[0], cell[1], 0x000000), dead))

    list(map(lambda cell: framebuffer.pixel(cell[0], cell[1], 0xFF0000), living))

def create_board(width, height):
    # cells dont need a position if they are dead.
    board= list(map(lambda _: list(map(lambda _: Cell(-1, -1), range(width))), range(height)))
    return board

def neighboring_positions(x: int, y: int) -> list[tuple[int, int]]:
    positions = [
            (x-1, y+1), (x, y+1), (x+1, y+1), 
            (x-1, y),             (x+1, y),
            (x-1, y-1), (x, y-1), (x+1, y-1)]
    return positions

# slow
def check_cells(board: list[list[Cell]]):
    life = []
    death = []

    def thing(cell: Cell, x: int, y: int):
        if cell.neighbors == 3:
            life.append((x, y))

        elif cell.cellstate == True:
            if cell.neighbors == 2:
                life.append((x, y))
            else:
                # cell.neighbors < 2 or cell.neighbors > 3:
                death.append((x, y))

    for (y, row) in enumerate(board):
        list(map(lambda j: thing(j[1], j[0], y), enumerate(row)))

    return (life, death)

def wrap_board(board_width: int, board_height: int, x: int, y: int):
    if y == board_height:
        y = 0

    if x == board_width:
        x = 0

    return (x, y)

#slow
def kill(board: list[list[Cell]], x, y): 
    board[y][x].cellstate = False

    for neighbor_pos in neighboring_positions(x, y):
        nx = neighbor_pos[0]
        ny = neighbor_pos[1]

        (nx, ny) = wrap_board(len(board[0]), len(board), nx, ny)

        board[ny][nx].dec_neighbors()

#slow
def birth(board: list[list[Cell]], x: int, y: int):
    if board[y][x].cellstate == False:
        for neighbor_pos in neighboring_positions(x, y):

            (nx, ny) = wrap_board(len(board[0]), len(board), neighbor_pos[0], neighbor_pos[1])

            board[ny][nx].inc_neighbors()

    board[y][x].cellstate = True

# slow
def purge(board: list[list[Cell]], life: list[tuple[int, int]], death: list[tuple[int, int]]):
    updated_life = []
    updated_death = []

    for cellpos in death:
        if board[cellpos[1]][cellpos[0]].cellstate != False:
            updated_death.append(cellpos)
        kill(board, cellpos[0], cellpos[1])

    for cellpos in life:
        if board[cellpos[1]][cellpos[0]].cellstate != True:
            updated_life.append(cellpos)
        birth(board, cellpos[0], cellpos[1])

    return (updated_life, updated_death)

def create_glider(board, x, y):
    birth(board, x,y)
    birth(board, x+1, y+1)
    birth(board, x+2,y+1)
    birth(board, x+2,y)
    birth(board, x+2,y-1)

# constants
BOARD_WIDTH = 16
BOARD_HEIGHT = 16
CHANCE = 8 # higher =  lower

FPS = 30

# program begin
neopixel, framebuffer, size = connect()

board = create_board(BOARD_WIDTH, BOARD_HEIGHT)


if CHANCE != 0:
    for _ in range(0, int((BOARD_WIDTH * BOARD_HEIGHT) / CHANCE)):
        randx = randint(0, BOARD_WIDTH-1)
        randy = randint(0, BOARD_HEIGHT-1)

        birth(board, randx, randy)

# create_glider(board, 5, 5)

framebuffer.fill(0)

(life, death) = check_cells(board)
draw_board(life, death)
framebuffer.display()

while True:
    (life, death) = check_cells(board)
    (updated_life, updated_death) = purge(board, life, death)

    draw_board(updated_life, updated_death)

    framebuffer.display()

