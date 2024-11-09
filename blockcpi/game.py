from enum import Enum

class TILETYPE(Enum):
    VIDE = 0
    ATTACHE = 1
    INTERDIT = 2

class COLOR(Enum):
    NONE = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4

    @staticmethod
    def from_hex(hex_code):
        if hex_code == "#FF0000":
            return COLOR.RED
        if hex_code == "#00FF00":
            return COLOR.GREEN
        if hex_code == "#0000FF":
            return COLOR.BLUE
        if hex_code == "#FFFF00":
            return COLOR.YELLOW
        return COLOR.NONE

class ORIENTATION(str, Enum):
    UP = "UP"
    RIGHT = "RIGHT"
    DOWN = "DOWN"
    LEFT = "LEFT"



class Move:
    x:int
    y:int
    pieceId:int
    rotation: ORIENTATION

    def __init__(self, x, y, orientation, pieceID):
        self.x = x
        self.y = y
        self.pieceId = pieceID
        self.rotation = orientation

    def to_json(self):
        return {
            "x": self.x,
            "y": self.y,
            "orientation": self.rotation,
            "piece_id": self.pieceId
        }


class Piece:
    id: int
    count: int
    shape: list[list[int]]
    nbCases: int

    def __init__(self, id, count, shape):
        self.id = id
        self.count = count
        self.shape = shape
        self.nbCases = sum(1 for row in shape for value in row if value != 0)

    def get_piece_rotations(self):
        return [
            (self.shape, ORIENTATION.UP),
            (self.rotate_matrix(self.shape, ORIENTATION.DOWN), ORIENTATION.DOWN),
            (self.rotate_matrix(self.shape, ORIENTATION.RIGHT), ORIENTATION.RIGHT),
            (self.rotate_matrix(self.shape, ORIENTATION.LEFT), ORIENTATION.LEFT)
        ]

    def to_json(self):
        return {
            "id": self.id,
            "count": self.count,
            "shape": self.shape,
            "nbCases": self.nbCases,
        }


    @staticmethod
    def rotate_matrix(matrix, orientation = ORIENTATION.UP):
        if orientation == ORIENTATION.UP:
            return matrix
        elif orientation == ORIENTATION.RIGHT:
            return [list(row) for row in zip(*matrix[::-1])]
        elif orientation == ORIENTATION.DOWN:
            return [row[::-1] for row in matrix[::-1]]
        elif orientation == ORIENTATION.LEFT:
            return [list(row) for row in zip(*matrix)][::-1]
        else:
            raise ValueError("Invalid orientation")

class Game:
    (rows, cols) = (20, 20)
    board = [[0] * cols] * rows
    game_over: bool = False
    score: int = 0
    pieces: list[Piece]
    first_move: bool = True
    
    def __init__(self, color, board, pieces):
        self.color = COLOR.from_hex(color)
        self.board = board
        self.pieces = pieces

    def to_json(self):
        return {
            "board" : self.board,
            "game_over": self.game_over,
            "score": self.score,
            "pieces": self.pieces,
            "first_move": self.first_move,
            "color": self.color,
        }    
    
    def get_tile_type(self):
        tile_type_board = [[0] * self.cols] * self.rows
        for y in range(0, 20):
            for x in range(0, 20):
                #check si tile est deja occupe
                if self.board[y][x] != COLOR.NONE:
                    tile_type_board[y][x] = TILETYPE.INTERDIT
                    continue
                #check si voisin est toi meme, donc peux pas jouer la
                adjacents = self.get_adjacent(y, x)
                for (j, i) in adjacents:
                    if self.board[j][i] == self.color:
                        tile_type_board[y][x] = TILETYPE.INTERDIT
                        is_valid = False
                if tile_type_board[y][x] == TILETYPE.INTERDIT:
                    continue
                #check si coin
                corners = self.get_corners(y, x)
                for (j, i) in corners:
                    if self.board[j][i] == self.color:
                        print(f"Found a coin at {j}, {i}")
                        tile_type_board[y][x] = TILETYPE.ATTACHE
                        break
        return tile_type_board

    def get_adjacent(self, y, x):
        adjacent_coords = [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
        return [
            (ny, nx) 
            for ny, nx in adjacent_coords 
            if 0 <= ny < 20 and 0 <= nx < 20
        ]

    def get_corners(self, y, x):
        corner_coords = [(y + 1, x + 1), (y - 1, x - 1), (y - 1, x + 1), (y + 1, x - 1)]
        return [
            (ny, nx) 
            for ny, nx in corner_coords 
            if 0 <= ny < 20 and 0 <= nx < 20
        ]


    def get_possible_moves(self, tile_type_board):
        if self.first_move:
            self.first_move = False
            return self.get_first_move(tile_type_board)
        for y in range(0, 20):
            for x in range(0, 20):
                if tile_type_board[y][x] == TILETYPE.ATTACHE:
                    res = self.try_everything(y, x, tile_type_board)
                    if res != None:
                        return res
        return None
                                    
    def get_first_move(self, tile_type_board):
        for (y, x) in self.get_coins():
            res = self.try_everything(y, x, tile_type_board)
            if res != None:
                return res
        return None

    def get_coins(self):
        return  [(0, 0), (0, 19), (19, 0), (19, 19)]    

    def try_everything(self, y, x, tile_type_board):
        for p in sorted(self.pieces, key=lambda piece: piece.nbCases, reverse=True):
            orientations = p.get_piece_rotations()
            for s, o in orientations:
                # print(f"Trying out shape {s} with orientation {o}")
                #itérer sur tous les translations possible de la piece sur cette attache
                for j in range(0, len(s)):
                    for i in range(0, len(s[j])):
                        if s[j][i] == 0:
                            continue
                        #vérifier que les autres cases sont good
                        pos_initiale_x = x - j
                        pos_initiale_y = y - i
                        if self.is_valid(pos_initiale_x, pos_initiale_y, s, tile_type_board):
                            print(f"Found a valid move at {pos_initiale_x}, {pos_initiale_y}")
                            return Move(pos_initiale_x, pos_initiale_y, o, p.id)
        return None
                        
                        

    def is_valid(self, x, y, shape, tile_type_board):
        for j in range(0, len(shape)):
            for i in range(0, len(shape[j])):
                if shape[j][i] == 0:
                    continue
                if x + j >= 20 or y + i >= 20:
                    return False
                if x + j < 0 or y + i < 0:
                    return False
                if tile_type_board[y + i][x + j] == TILETYPE.INTERDIT:
                    return False
        return True
                        
