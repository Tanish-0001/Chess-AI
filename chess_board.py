import chess
import numpy as np
import chess.pgn


def square_to_index(square):
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

    chess_board = np.zeros((14, 8, 8), dtype=np.int32)

    for piece in chess.PIECE_TYPES:
        for square in board.pieces(piece, chess.WHITE):
            i = np.unravel_index(square, (8, 8))
            chess_board[piece - 1, 7 - i[0], i[1]] = 1

        for square in board.pieces(piece, chess.BLACK):
            i = np.unravel_index(square, (8, 8))
            chess_board[piece + 5, 7 - i[0], i[1]] = 1

    if board.turn == chess.WHITE:
        for move in board.legal_moves:
            i, j = square_to_index(move.to_square)
            chess_board[12, i, j] = 1

    else:
        for move in board.legal_moves:
            i, j = square_to_index(move.to_square)
            chess_board[13, i, j] = 1

    return chess_board


def square_to_coord(position: int):
    rank = position // 8  # a number
    file = position % 8  # a letter
    mapping = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    return mapping[file] + str(rank + 1)


if __name__ == '__main__':
    pgn = open("lichess_db_standard_rated_2013-02.pgn")
    first_game = chess.pgn.read_game(pgn)

    move_number = 1
    curr_board = chess.Board()

    for number, curr_move in enumerate(first_game.mainline_moves()):
        curr_board.push(curr_move)

        # Remember that number starts from 0
        if number == move_number:
            break

    print(curr_board)
    print(get_chess_board(curr_board))