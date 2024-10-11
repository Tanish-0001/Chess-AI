# Chess-AI

Link to dataset: https://database.lichess.org/
Games were taken from february 2013

How the model works:
-	First a chess board is featurized into a 12x8x8 tensor. There are 12 different 8x8 tensors that capture the position of each piece for both white and black separately (6 pieces – pawn, knight, bishop, rook, queen, king). In each array, the piece is represented by a "-1" and the legal moves with “1”. 
-	The training data of this was gathered from Lichess’ open database (https://database.lichess.org/#standard_games). I used the games from February 2013. It contains a total of 123,961 chess games played.
-	Network has one output layer which gives the source square scores and another that gives destination square scores.
-	After the model finished learning from the labelled set, then came the reinforcement learning part.
