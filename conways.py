# imports
import enum
import os
# enum class stuff
class CellState(enum.Enum):
    DEAD = 0
    ALIVE = 1

class Cell():
    def __init__(self) -> None:
        self.neighbors = 0
        self.cellstate = CellState.DEAD

    def inc_neighbors(self):
        self.neighbors += 1

    def dec_neighbors(self):
        self.neighbors -= 1

        if self.neighbors < 0:
            self.neighbors = 0

# helper functions
def drawScreen(screen: list):
    for row in screen:
        for cell in row:
            if cell.cellstate == CellState.ALIVE:
                print("#", end = " ")
            else: 
                print(" ", end = " ")
        print()

def neighboringPositions(x: int, y: int) -> list[tuple[int, int]]:
    positions = [
            (x-1, y+1), (x, y+1), (x+1, y+1), 
            (x-1, y),             (x+1, y),
            (x-1, y-1), (x, y-1), (x+1, y-1)]
    return positions


def createScreen(width, height):
    screen = list(map(lambda x: list(map(lambda x: Cell(), range(width))), range(height)))
    return screen

# rules
#   Any live cell with fewer than two live neighbours dies, as if by underpopulation.
#   Any live cell with two or three live neighbours lives on to the next generation.
#   Any live cell with more than three live neighbours dies, as if by overpopulation.
#   Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

# condensed Any live cell with two or three live neighbours survives.
#   Any dead cell with three live neighbours becomes a live cell.
#   All other live cells die in the next generation. Similarly, all other dead cells stay dead.
def checkCells(screen: list[list[Cell]]):
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

def kill(screen, x, y): 
    screen[y][x].cellstate = CellState.DEAD

    for neighbor_pos in neighboringPositions(x, y):
        try:
            screen[neighbor_pos[1]][neighbor_pos[0]].dec_neighbors()
        except IndexError:
            pass

def birth(screen, x, y):

    if screen[y][x].cellstate == CellState.DEAD:
        for neighbor_pos in neighboringPositions(x, y):
            try:
                screen[neighbor_pos[1]][neighbor_pos[0]].inc_neighbors()
            except IndexError:
                pass

    screen[y][x].cellstate = CellState.ALIVE

def purge(screen: list[list[Cell]], life: list[tuple[int, int]], death: list[tuple[int, int]]):

    for cellpos in death:
        x = cellpos[0]
        y = cellpos[1]
        kill(screen, x, y)

    for cellpos in life:
        x = cellpos[0]
        y = cellpos[1]
        birth(screen, x, y)


def advance(screen):
    (life, death) = checkCells(screen)
    purge(screen, life, death)
    drawScreen(screen)

# constants
HEIGHT = 25
WIDTH = 25

# program begin
screen = createScreen(WIDTH, HEIGHT)

# flip flap ting
birth(screen, 1, 1)
birth(screen, 1, 2)
birth(screen, 1, 3)

# glider
birth(screen, 5,5)
birth(screen, 6,6)
birth(screen, 7,6)
birth(screen, 7,5)
birth(screen, 7,4)

drawScreen(screen)
while True:
    input("press a key")
    advance(screen)
