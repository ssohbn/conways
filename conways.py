# imports
import os

from cell import CellState
from cell import Cell

from random import randint

# helper functions
def drawScreen(screen: list[list[Cell]]):
    def stuff(row):
        list(map(lambda cell: print(cell.neighbors if cell.cellstate == CellState.ALIVE else " ", end=" "), row))
        print()

    list(map(lambda row: stuff(row), screen))

def create_screen(width, height):
    screen = list(map(lambda _: list(map(lambda _: Cell(), range(width))), range(height)))
    return screen

def neighboring_positions(x: int, y: int) -> list[tuple[int, int]]:
    positions = [
            (x-1, y+1), (x, y+1), (x+1, y+1), 
            (x-1, y),             (x+1, y),
            (x-1, y-1), (x, y-1), (x+1, y-1)]
    return positions

def check_cells(screen: list[list[Cell]]):
    death = []
    life = []

    for (y, row) in enumerate(screen):
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

def wrap_screen(screen, x, y):
    if x == len(screen):
        x = 0

    if y == len(screen[0]):
        y = 0
    return (x, y)

def kill(screen: list[list[Cell]], x, y): 
    screen[y][x].cellstate = CellState.DEAD

    for neighbor_pos in neighboring_positions(x, y):
        nx = neighbor_pos[0]
        ny = neighbor_pos[1]

        (nx, ny) = wrap_screen(screen, nx, ny)

        screen[ny][nx].dec_neighbors()

def birth(screen: list[list[Cell]], x: int, y: int):
    if screen[y][x].cellstate == CellState.DEAD:
        for neighbor_pos in neighboring_positions(x, y):

            (nx, ny) = wrap_screen(screen, neighbor_pos[0], neighbor_pos[1])

            screen[ny][nx].inc_neighbors()

    screen[y][x].cellstate = CellState.ALIVE

def purge(screen: list[list[Cell]], life: list[tuple[int, int]], death: list[tuple[int, int]]):
    for cellpos in death:
        kill(screen, cellpos[0], cellpos[1])

    for cellpos in life:
        birth(screen, cellpos[0], cellpos[1])


def advance(screen):
    (life, death) = check_cells(screen)
    purge(screen, life, death)
    drawScreen(screen)

def create_glider(screen, x, y):
    birth(screen, x,y)
    birth(screen, x+1, y+1)
    birth(screen, x+2,y+1)
    birth(screen, x+2,y)
    birth(screen, x+2,y-1)

# constants
HEIGHT = 10
WIDTH = 10
CHANCE = 0

# program begin
screen = create_screen(WIDTH, HEIGHT)

if CHANCE != 0:
    for _ in range(int((WIDTH * HEIGHT) / CHANCE)):
        birth(screen, randint(0, WIDTH-1), randint(0, HEIGHT-1))

# glider
create_glider(screen, 5, 5)

drawScreen(screen)
while True:
    input("press a key")
    os.system("clear") # demolishing windows with a single line. im sure theres a better way to do this
    advance(screen)

