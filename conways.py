# imports
import pygame

from cell import CellState
from cell import Cell

from random import randint



# helper functions
def draw_board(screen: pygame.surface.Surface, living: list[tuple[int, int]], width, height):
    screen.fill((255,255,255))
#    tpool.map(lambda cell: pygame.draw.rect(screen, (0,0,0), pygame.Rect((cell[0]*width, cell[1]*height, width, height))), living)
#    list(executor.map(lambda cell: pygame.draw.rect(screen, (0,0,0), pygame.Rect((cell[0]*width, cell[1]*height, width, height))), living))
#    list(executor.map(lambda cell: pygame.draw.rect(screen, (0,0,0), pygame.Rect((cell[0]*width, cell[1]*height, width, height))), living))
    list(map(lambda cell: pygame.draw.rect(screen, (0,0,0), pygame.Rect((cell[0]*width, cell[1]*height, width, height))), living))

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

def check_cells(board: list[list[Cell]]):
    death = []
    life = []

    for (y, row) in enumerate(board):
        for (x, cell) in enumerate(row):
            if cell.neighbors == 3:
                life.append((x, y))
            elif cell.cellstate == CellState.ALIVE:
                if cell.neighbors == 2:
                    life.append((x, y))
                else:
                    # cell.neighbors < 2 or cell.neighbors > 3:
                    death.append((x, y))

    return (life, death)

def wrap_board(board, x, y):
    if y == len(board):
        y = 0

    if x == len(board[0]):
        x = 0

    return (x, y)

def kill(board: list[list[Cell]], x, y): 
    board[y][x].cellstate = CellState.DEAD

    for neighbor_pos in neighboring_positions(x, y):
        nx = neighbor_pos[0]
        ny = neighbor_pos[1]

        (nx, ny) = wrap_board(board, nx, ny)

        board[ny][nx].dec_neighbors()

def birth(board: list[list[Cell]], x: int, y: int):
    if board[y][x].cellstate == CellState.DEAD:
        for neighbor_pos in neighboring_positions(x, y):

            (nx, ny) = wrap_board(board, neighbor_pos[0], neighbor_pos[1])

            board[ny][nx].inc_neighbors()

    board[y][x].cellstate = CellState.ALIVE

def purge(board: list[list[Cell]], life: list[tuple[int, int]], death: list[tuple[int, int]]):
    for cellpos in death:
        kill(board, cellpos[0], cellpos[1])

    for cellpos in life:
        birth(board, cellpos[0], cellpos[1])



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

# program begin
board = create_board(BOARD_WIDTH, BOARD_HEIGHT)

clock = pygame.time.Clock()
screen = displaysurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("conways")

if CHANCE != 0:
    for _ in range(0, int((BOARD_WIDTH * BOARD_HEIGHT) / CHANCE)):
        randx = randint(0, BOARD_WIDTH-1)
        randy = randint(0, BOARD_HEIGHT-1)

        birth(board, randx, randy)

create_glider(board, 5, 5)

while True:
    screen.fill((255,255,255))
    (life, death) = check_cells(board)
    purge(board, life, death)
    draw_board(screen, life, SCREEN_WIDTH/BOARD_WIDTH, SCREEN_HEIGHT/BOARD_HEIGHT)

    pygame.display.update()
    clock.tick(FPS)

    print(clock.get_fps())
