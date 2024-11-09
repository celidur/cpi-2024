import requests

from blokcpi.game import Game, Piece
from blokcpi.map import to_2d_arr

BASE_URL = "localhost:5000/"

def start_game() -> Game:
    resp = requests.post(
        BASE_URL + "start_game",
    )

    js = resp.json()

    pieces = []
    for pc in js['pieces']:
        pieces.append(
            Piece(
                id=pc['id'],
                count=pc['count'],
                shape=pc['shape']
            )
        )

    return Game(
        color=js['color'],
        board=to_2d_arr(js['board']),
        pieces=pieces
    )

def send_move(x: int, y: int, orientation: str, )