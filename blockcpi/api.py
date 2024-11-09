import requests

from blockcpi.game import Game, Piece, Move
from blockcpi.map import to_2d_arr


def start_game(url) -> Game:
    resp = requests.post(
        url + "start_game",
    )
    resp = resp.json()

    pieces = []
    for pc in resp['pieces']:
        pieces.append(
            Piece(
                id=pc['id'],
                count=pc['count'],
                shape=pc['shape']
            )
        )

    print(f"Game started with color: {resp['color']}")
    print(resp['board'])
    return Game(
        color=resp['color'],
        board=to_2d_arr(resp['board']),
        pieces=pieces
    )

def send_move(url, game: Game, move: Move) -> Game:
    resp = requests.post(
        url + "send_move",
        json=move.to_json()
    )
    resp = resp.json()
    print(f"Got message from server: {resp['message']}")
    print(resp['board'])
    game.score = resp['score']
    game.game_over = resp['game_over']
    game.pieces[move.pieceId].count = game.pieces[move.pieceId].count - 1
    game.board = to_2d_arr(resp['board'])
    return game

def end_game(url, game: Game):
    resp = requests.post(url + "end_game")
    resp = resp.json()
    print(resp['board'])

    game.game_over = resp['game_over']
    game.score = resp['score']
    game.board = to_2d_arr(resp['board'])
    return game


