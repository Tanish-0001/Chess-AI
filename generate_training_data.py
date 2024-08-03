import numpy as np
import chess.pgn
from chess_board import get_chess_board
from torch.utils.data import Dataset


def generate_next_sample(batch_size):
    """
    :param batch_size: integer, size of batch
    :return: list of games in PGN format
    """
    games = []
    for i in range(batch_size):
        if pgn:
            games.append(chess.pgn.read_game(pgn))
        else:  # we have run out of games in the file
            break
    return games


def featurize_game(pgn_game):
    """
    :param pgn_game: PGN representation of the game
    :return: a list states which has the features the board in every turn
    """
    board = chess.Board()
    states = []
    for number, curr_move in enumerate(pgn_game.mainline_moves()):
        x = get_chess_board(board)  # featurize the current board
        y = np.array([curr_move.from_square, curr_move.to_square])  # actual moves played - source square, destination square of the pieces
        states.append((x, y))
        board.push(curr_move)  # update the board

    return states


def load_dataset(batch_size):
    """
    :param batch_size: integer, size of batch
    :return: featurized games along with labels
    """
    games = generate_next_sample(batch_size)
    inputs = []
    labels = []
    for game in games:
        game_state = featurize_game(game)
        for x, y in game_state:
            inputs.append(x)
            labels.append(y)

    return np.array(inputs), labels


class ChessDataset(Dataset):
    """
    Creates the dataset of chess games using PyTorch's Dataset class inorder to use Dataloader
    """
    def __init__(self, num_examples):
        super(ChessDataset, self).__init__()
        self.num_examples = num_examples
        self.x, self.y = load_dataset(num_examples)

    def __len__(self):
        return self.num_examples

    def __getitem__(self, idx):
        return self.x[idx].astype(np.float32), self.y[idx].astype(np.int64)


pgn = open("lichess_db_standard_rated_2013-02.pgn")  # has 123,961 games

if __name__ == "__main__":
    train_data = load_dataset(1)
    print(type(train_data[0]))
