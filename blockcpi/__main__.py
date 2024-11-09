import sys

from blockcpi.api import start_game, send_move, end_game
from blockcpi.game import Move, ORIENTATION


def main():
    url = "http://" + sys.argv[1] + "/"
    game = start_game(url)
    while not game.game_over:
        # Program loop
        tile = game.get_tile_type()
        #logic

        move = game.get_possible_moves(tile) 
      
        if move is None:
            print("Could not find any move! Ending game")
            game = end_game(url, game)
            print(game.score)
            return

        print("Trying out move")
        print(move.to_json())
        game = send_move(url, game, move)


if __name__ == "__main__":
    main()

