class Cell():
    def __init__(self) -> None:
        self.neighbors = 0
        self.cellstate: bool = False
#        self.x = x
#        self.y = y

    def inc_neighbors(self):
        self.neighbors += 1

    def dec_neighbors(self):
        self.neighbors -= 1

        if self.neighbors < 0:
            self.neighbors = 0
