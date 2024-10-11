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
    :return: 12x8x8 numpy array comprised of 12 8x8 arrays which store the presence of pieces. The first 6 arrays store
            white pieces, the next 6 store black pieces. In each 8x8 array, the actual piece is denoted by -1 and its
            legal moves by 1
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


def get_board_from_featurization(featurized_board):
    """
    :param featurized_board: 12x8x8 numpy array, where the first 6 layers are white pieces and the next 6 layers are black pieces.
                             The actual pieces are denoted by -1 and the legal moves are represented by 1.
    :return: a chess.Board() object reconstructed from the featurization
    """

    board = chess.Board()
    board.clear()  # Clear the board to set up pieces from scratch

    piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]

    for piece_index in range(12):
        for rank in range(8):
            for file in range(8):
                if featurized_board[piece_index, rank, file] == -1:
                    square = chess.square(file, 7 - rank)

                    piece_type = piece_types[piece_index % 6]
                    color = chess.BLACK if piece_index >= 6 else chess.WHITE

                    board.set_piece_at(square, chess.Piece(piece_type, color))

    return board


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
    print(get_board_from_featurization(get_chess_board(new_board)))

