import random

pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1} #dictionary to store the value of each piece
CHECKMATE = 1000 #checkmate score, highest possible score 
STALEMATE = 0 #stalemate score, lowest possible score

'''
Pick a random move from the list of valid moves
'''
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)] #return a random move

'''
Find the best move for the current player utilizing the minimax algorithm
'''
def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1 #if it is white's turn, then the multiplier is 1, if it is black
    # we are trying to minimize our opponent's best move, that is minimize their max score
    opponentMinMaxScore = CHECKMATE #initialize the opponent's minmax score to the highest possible score
    bestPlayerMove = None #initialize the best player move to None
    random.shuffle(validMoves) #shuffle the valid moves to randomize the order of the moves to prevent the AI from making the same moves every time
    #we are looking 2 moves ahead, so we need to iterate through the valid moves twice
    for playerMove in validMoves: #iterate through the valid moves
        gs.makeMove(playerMove) #make the move
        opponentsMoves = gs.getValidMoves() #get the valid moves for the opponent
        opponentMaxScore = -CHECKMATE #initialize the opponent's max score to the lowest possible score
        #finds the best move for the opponent and highest score they can get
        for opponentsMove in opponentsMoves:
            gs.makeMove(opponentsMove)
            if gs.checkMate: #if the move results in a checkmate
                score = -turnMultiplier * CHECKMATE #score the move based on the checkmate score
            elif gs.staleMate: #if the move results in a stalemate
                score = STALEMATE #score the move based on the stalemate score
            else:
                score = -turnMultiplier * scoreMaterial(gs.board) #score the board based on material and whose turn it is
            if score > opponentMaxScore: #based on maximizing the score, if the score is greater than the maxScore, then update the maxScore and bestMove
                opponentMaxScore = score
            gs.undoMove() #undo the move, because we are only evaluating the move, not actually making it
        if opponentMaxScore < opponentMinMaxScore: #based on minimizing the opponent's best move, if the opponent's max score is less than the opponent's minmax score, then update the opponent's minmax score and the best player move
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove() #undo the move, because we are only evaluating the move, not actually making it
    return bestPlayerMove

'''
Score the board based on material
'''
def scoreMaterial(board):
    score = 0 
    for row in board: #iterate through the board
        for square in row: #iterate through the squares
            if square[0] == 'w': #if the piece is white
                score += pieceScore[square[1]] #add the value of the piece to the score
            elif square[0] == 'b': #if the piece is black
                score -= pieceScore[square[1]] #subtract the value of the piece from the score
    return score