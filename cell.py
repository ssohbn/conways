import enum
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
