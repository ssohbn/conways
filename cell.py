import enum

class CellState(enum.Enum):
    DEAD = 0
    ALIVE = 1

class Cell():
    def __init__(self, x, y) -> None:

        self.neighbors = 0
        self.cellstate = CellState.DEAD
        self.x = x
        self.y = y

    def inc_neighbors(self):
        self.neighbors += 1

    def dec_neighbors(self):
        self.neighbors -= 1

        if self.neighbors < 0:
            self.neighbors = 0
