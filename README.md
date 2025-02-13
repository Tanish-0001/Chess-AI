# Chess-AI

This is still a work in progress - the RL part needs a major rework.\
\
Link to dataset: https://database.lichess.org/. Games were taken from february 2013

How the model works:
-	First a chess board is featurized into a 12x8x8 tensor. There are 12 different 8x8 tensors that capture the position of each piece for both white and black separately (6 pieces – pawn, knight, bishop, rook, queen, king). In each array, the piece is represented by a "-1" and the legal moves with “1”. 
-	The training data of this was gathered from Lichess’ open database (https://database.lichess.org/#standard_games). I used the games from February 2013. It contains a total of 123,961 chess games played.
-	The network has one output layer of size 4096 (64 * 64) which represents the probabilities over all possible moves at given state of the board.
-	After the supervised learning comes the reinforcement learning part.
