from enum import Enum

class Piece:
    id: int
    count: int
    shape: list[list[int]]

    def __init__(self, id, count, shape):
        self.id = id
        self.count = count
        self.shape = shape


class Game:
    (rows, cols) = (20, 20)
    board = [[0] * cols] * rows
    
    def __init___(self, ):
        ...
    
    def get_tiletype(self, color):
        for y in range(0, 20):
            for x in range(0, 20):
                if self.board[0][0] != COLONONE:
                    

class COLOR(Enum):
    NONE = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4

class TILETYPE(Enum):
    VIDE = 0
    ATTACHE = 1
    INTERDIT = 2
    