# imports
import pygame
import functools

from cell import CellState
from cell import Cell

from random import randint

# helper functions
def draw_board(living: list[tuple[int, int]], dead: list[tuple[int,int]], width: int, height: int):

    list(map(lambda cell: pygame.draw.rect(screen, (255,255,255), pygame.Rect((cell[0]*width, cell[1]*height, width, height))), dead))

    list(map(lambda cell: pygame.draw.rect(screen, (0,0,0), pygame.Rect((cell[0]*width, cell[1]*height, width, height))), living))

def create_board(width, height):
    # cells dont need a position if they are dead.
    board= list(map(lambda _: list(map(lambda _: Cell(-1, -1), range(width))), range(height)))
    return board

@functools.cache
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

        elif cell.cellstate == CellState.ALIVE:
            if cell.neighbors == 2:
                life.append((x, y))
            else:
                # cell.neighbors < 2 or cell.neighbors > 3:
                death.append((x, y))

    for (y, row) in enumerate(board):
        list(map(lambda j: thing(j[1], j[0], y), enumerate(row)))

    return (life, death)

@functools.cache
def wrap_board(board_width: int, board_height: int, x: int, y: int):
    if y == board_height:
        y = 0

    if x == board_width:
        x = 0

    return (x, y)

#slow
def kill(board: list[list[Cell]], x, y): 
    board[y][x].cellstate = CellState.DEAD

    for neighbor_pos in neighboring_positions(x, y):
        nx = neighbor_pos[0]
        ny = neighbor_pos[1]

        (nx, ny) = wrap_board(len(board[0]), len(board), nx, ny)

        board[ny][nx].dec_neighbors()

#slow
def birth(board: list[list[Cell]], x: int, y: int):
    if board[y][x].cellstate == CellState.DEAD:
        for neighbor_pos in neighboring_positions(x, y):

            (nx, ny) = wrap_board(len(board[0]), len(board), neighbor_pos[0], neighbor_pos[1])

            board[ny][nx].inc_neighbors()

    board[y][x].cellstate = CellState.ALIVE

# slow
def purge(board: list[list[Cell]], life: list[tuple[int, int]], death: list[tuple[int, int]]):
    updated_life = []
    updated_death = []

    for cellpos in death:
        if board[cellpos[1]][cellpos[0]].cellstate != CellState.DEAD:
            updated_death.append(cellpos)
        kill(board, cellpos[0], cellpos[1])

    for cellpos in life:
        if board[cellpos[1]][cellpos[0]].cellstate != CellState.ALIVE:
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
BOARD_HEIGHT = 250
BOARD_WIDTH = 250
CHANCE = 4 # higher =  lower

SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1000
FPS = 30

CELL_WIDTH = int(SCREEN_WIDTH/BOARD_WIDTH)
CELL_HEIGHT = int(SCREEN_HEIGHT/BOARD_HEIGHT)

# program begin
board = create_board(BOARD_WIDTH, BOARD_HEIGHT)

screen = displaysurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("conways")

if CHANCE != 0:
    for _ in range(0, int((BOARD_WIDTH * BOARD_HEIGHT) / CHANCE)):
        randx = randint(0, BOARD_WIDTH-1)
        randy = randint(0, BOARD_HEIGHT-1)

        birth(board, randx, randy)

# create_glider(board, 5, 5)

screen.fill((255,255,255))
(life, death) = check_cells(board)
draw_board(life, death, CELL_WIDTH, CELL_HEIGHT)
pygame.display.update()

while True:
    (life, death) = check_cells(board)
    (updated_life, updated_death) = purge(board, life, death)
    draw_board(updated_life, updated_death, CELL_WIDTH, CELL_HEIGHT)

    clock.tick(FPS)
    pygame.display.update()

    print(clock.get_fps(), clock.get_rawtime())

