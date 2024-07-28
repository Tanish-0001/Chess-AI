import numpy as np
import chess.pgn
from chess_board import get_chess_board


def generate_next_sample(batch_size):
    games = []
    for i in range(batch_size):
        if pgn:
            games.append(chess.pgn.read_game(pgn))
        else:
            break
    return games


def featurize_game(pgn_game):
    board = chess.Board()
    states = []
    for number, curr_move in enumerate(pgn_game.mainline_moves()):
        x = get_chess_board(board)
        y = np.array([curr_move.from_square, curr_move.to_square])
        states.append((x, y))
        board.push(curr_move)

    return states


def load_dataset(batch_size):
    games = generate_next_sample(batch_size)
    inputs = []
    labels = []
    for game in games:
        game_state = featurize_game(game)
        for x, y in game_state:
            inputs.append(x)
            labels.append(y)

    return np.array(inputs), labels


pgn = open("lichess_db_standard_rated_2013-02.pgn")  # has 123,961 games

if __name__ == "__main__":
    train_data = load_dataset(1)
    print(type(train_data[0]))
