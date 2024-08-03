import chess
import numpy as np
import chess.pgn


def square_to_index(square):
    """
    :param square: integer between 0 and 63
    :return: coordinates in array indices
    """
    mapping = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    position = chess.square_name(square)  # ex: e4
    return 8 - int(position[1]), mapping[position[0]]


def get_chess_board(board):
    """
    :param board: chess board
    :return: 14x8x8 numpy array comprised of 14 8x8 arrays which store the presence of pieces. The first 6 arrays store
            white pieces, the next 6 store black pieces, and the remaining 2 store the valid moves
            order: pawn, knight, bishop, rook, queen, king
    """

    chess_board = np.zeros((12, 8, 8), dtype=np.int32)
    for square, piece in board.piece_map().items():
        piece_type = piece.piece_type
        piece_index = (6 + piece_type - 1) if piece.color == chess.BLACK else (piece_type - 1)
        chess_board[piece_index, 7 - square // 8, square % 8] = -1  # actual piece is represented by a -1

    turn = board.turn
    board.turn = chess.WHITE
    for move in board.legal_moves:
        piece = board.piece_at(move.from_square)
        piece_type = piece.piece_type
        if piece is not None:
            piece_index = 6 + piece_type - 1 if piece.color == chess.BLACK else piece_type - 1
            chess_board[piece_index, 7 - move.to_square // 8, move.to_square % 8] = 1  # legal moves of a piece are represented by a 1
    board.turn = chess.BLACK
    for move in board.legal_moves:
        piece = board.piece_at(move.from_square)
        piece_type = piece.piece_type
        if piece is not None:
            piece_index = 6 + piece_type - 1 if piece.color == chess.BLACK else piece_type - 1
            chess_board[piece_index, move.to_square // 8, move.to_square % 8] = 1
    board.turn = turn

    return chess_board


def square_to_uci(position: int):
    """
    :param position: integer between 0 and 63
    :return: string representing a uci square, ex: e4, a6, etc
    """
    rank = position // 8  # a number
    file = position % 8  # a letter
    mapping = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    return mapping[file] + str(rank + 1)


if __name__ == "__main__":
    # print(square_to_index(0))
    # print(square_to_uci(0))
    new_board = chess.Board()
    new_board.push_uci("e2e4")
    print(get_chess_board(new_board))

