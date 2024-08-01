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
Find the best move based on material alone
'''
def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1 #if it is white's turn, then the multiplier is 1, if it is black
    maxScore = -CHECKMATE #initialize maxScore to the lowest possible score
    bestMove = None
    for playerMove in validMoves: #iterate through the valid moves
        gs.makeMove(playerMove) #make the move
        if gs.checkMate: #if the move results in a checkmate
            score = CHECKMATE #score the move based on the checkmate score
        elif gs.staleMate: #if the move results in a stalemate
            score = STALEMATE #score the move based on the stalemate score
        else:
            score = turnMultiplier * scoreMaterial(gs.board) #score the board based on material and whose turn it is
        if(score > maxScore): #based on maximizing the score, if the score is greater than the maxScore, then update the maxScore and bestMove
            score = maxScore
            bestMove = playerMove
        gs.undoMove() #undo the move, because we are only evaluating the move, not actually making it
    return bestMove

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