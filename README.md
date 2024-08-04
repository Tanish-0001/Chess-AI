# Chess-AI

Link to dataset: https://database.lichess.org/
Games were taken from february 2013

This is a model that is intended to play chess. I am submitting two models – a plain NN and a CNN.
The models do not play chess perfectly. The best they have done is 12 moves before giving me an illegal move. However, I believe there is a huge scope of improvement for this model.

How the model works:
-	First a chess board is featurized into a 12x8x8 tensor. There are 12 different 8x8 tensors that capture the position of each piece for both white and black separately (6 pieces – pawn, knight, bishop, rook, queen, king). In each array, the piece is represented by a -1 and the legal moves with “1”. 
-	The training data of this was gathered from Lichess’ open database (https://database.lichess.org/#standard_games). I used the games from February 2013. It contains a total of 123,961 chess games played.
-	From this dataset, a sample of 8,192 games were chosen (twice) for the CNN and 32,768 for the Linear NN. They were used to pre-train the model. For each game, every move was fed into the Neural Network along with the labels. The label were two numbers – the source square and the destination square (for examples the move pawn from e2 to e4 is represented by (12, 28 [0-indexed]). This is also what the model tries to predict.
-	Both networks have one output layer which gives the source square scores and one that gives destination square scores.
-	Loss function used was cross entropy loss and the loss of each output layer was added to give the final loss.
-	After the model finished learning from the labelled set, then came the reinforcement learning part.
-	There were 10,000 episodes (2000 for CNN). In each turn, the model has a 20% chance to choose one of the legal uniformly at random. The other 80% of the time, it predicts a move using the pre-trained model. 
-	After the game is over, the RL step takes place. It randomly selects some states, rewards, etc from memory and using the bellman equation, optimizes the model using MSE loss between target q values vs actual q values.

Things I tried but could not get to work / would not work:
-	I thought of simply reading the FEN and algorithmically finding the list of all possible moves. Then pass this to a NN which returns a move from that list. I rejected this because the size of that input list can be variable – it can vary from 0 moves to maybe a few tens of moves possible. 
-	I first tried a 14x8x8 featurization of the board but after it made many illegal moves, I tried other methods. First a 15x8x8 featurization and finally settled on the 12x8x8 array representation.
-	I had also considered to keep the model simple and only have it play white, but I had to  reject this because I figured self-play would be easier if it was capable of playing both white and black.
-	I had added one more FC hidden layer to the model but it took so much longer in the RL step that I got a TimeoutError.
-	I also tried using more training data but using 65536 examples gives memory error.
-	I tried different activation functions such as ReLU, Leaky ReLU, SELU, tanh, sigmoid and the one which worked best was ReLU.
-	I tried an entirely different approach where first, the model is trained by a RL algorithm about move legality. Then it is trained in a supervised manner from the Lichess' dataset and finally plays against itself repeatedly in an RL algorithm.

Scope of Improvement:
-	More training data. I have only used ~25% of the data in the lichess database. More training data is almost always better so I believe using more should help the model perform better.
-	PyTorch was not able to use cuda, so this entire model worked on the CPU which led to significant issues with time. If GPU processing was available, the model could learn much faster allowing for more finetuning of hyperparameters and architecture. As such, I barely scratched the surface.
-	Adding more hidden layer / increasing size of existing layers might help the model do better. I was not able to test this properly because of some technical issued which made PyTorch unable to use the GPU.
-	The games in the dataset were games played by random people and random time controls (which means there are games of 1min/3min in which players don’t play very well due to time pressure), not necessarily grand masters’ games. Using a dataset of professional games as well as dataset which consists of a variety of openings should definitely help the model learn better.
-	Can use fancier techniques like dropout or prioritized experience replay to improve model performance.


