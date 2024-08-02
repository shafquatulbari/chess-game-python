import random

pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1} #dictionary to store the value of each piece
CHECKMATE = 1000 #checkmate score, highest possible score 
STALEMATE = 0 #stalemate score, lowest possible score
DEPTH = 3 #depth of the recursive function, if you have difficulty settings, you can change this value
'''
Pick a random move from the list of valid moves
'''
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)] #return a random move

'''
Find the best move for the current player without recursively looking ahead
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
        if gs.staleMate: #if the move results in a stalemate
            opponentMaxScore = STALEMATE #score the move based on the stalemate score
        elif gs.checkMate: #if the move results in a checkmate
            opponentMaxScore = -CHECKMATE #score the move based on the checkmate score
        else:
            #finds the best move for the opponent and highest score they can get
            opponentMaxScore = -CHECKMATE #initialize the opponent's max score to the lowest possible score
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                gs.getValidMoves()
                if gs.checkMate: #if the move results in a checkmate
                    score = CHECKMATE #score the move based on the checkmate score
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
helper method to make the first recursive call
'''
def findBestMoveMinMax(gs, validMoves):
    global nextMove
    nextMove = None 
    findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    return nextMove

'''
Recursive function to find the best move for the current player utilizing MinMax
'''
def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0: #if we have reached the depth limit 
        return scoreMaterial(gs.board) #return the score of the board
    if whiteToMove: #if it is white's turn
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move) #make the move
            nextMoves = gs.getValidMoves() #get the valid moves for the next player
            score = findMoveMinMax(gs, nextMoves, depth-1, False) #recursively call the function to find the best move for the next player
            if score > maxScore: #based on maximizing the score, if the score is greater than the maxScore, then update the maxScore and the nextMove
                maxScore = score
                if depth == DEPTH: #if we have reached the depth limit
                    nextMove = move 
            gs.undoMove() #undo the move, because we are only evaluating the move, not actually making it
        return maxScore
    else:  #if it is black
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves() 
            score = findMoveMinMax(gs, nextMoves, depth-1, True) #recursively call the function to find the best move for the next player
            if score < minScore: #based on minimizing the score, if the score is less than the minScore, then update the minScore and the nextMove
                minScore = score
                if depth == DEPTH: #if we have reached the depth limit
                    nextMove = move
            gs.undoMove() #undo the move, because we are only evaluating the move, not actually making it
        return minScore
    
'''
Score the board based on the game state, a positive score is good for white, a negative score is good for black
'''
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE #if it is white's turn and there is a checkmate, then return the negative checkmate score, black wins
        else:
            return CHECKMATE #if it is black turn and there is a checkmate, then return the checkmate score, white wins
    elif gs.staleMate:
        return STALEMATE
    score = scoreMaterial(gs.board)
    return score
    

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