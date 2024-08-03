import random

pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1} #dictionary to store the value of each piece

knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

rookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
                [4, 4, 4, 4, 4, 4, 4, 4],
                [1, 1, 2, 3, 3, 2, 1, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 1, 2, 3, 3, 2, 1, 1],
                [4, 4, 4, 4, 4, 4, 4, 4],
                [4, 3, 4, 4, 4, 4, 3, 4]]

piecePositionScores = {"N": knightScores , "B": bishopScores, "R": rookScores} #dictionary to store the positional score of each piece

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
def findBestMoveMinMaxNoRecursion(gs, validMoves): #depth is 2
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
def findBestMove(gs, validMoves, returnQueue):
    global nextMove
    nextMove = None 
    random.shuffle(validMoves) #shuffle the valid moves to randomize the order of the moves to prevent the AI from making the same moves every time
    #findMoveMinMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1) #call the recursive function to find the best move
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH,-CHECKMATE,CHECKMATE, 1 if gs.whiteToMove else -1) #call the recursive function to find the best move, instead of the function findMoveMinMax
    returnQueue.put(nextMove) #put the best move in the queue

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
This is just shorter to write than findMoveMinMax, but it is the same thing
'''
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0: #if we have reached the depth limit
        return turnMultiplier * scoreBoard(gs) #return the score of the board
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)  
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier) #negative because we are looking at the opponent's score, whatever is best score for opponent is worst score for us
        if score > maxScore: #based on maximizing the score, if the score is greater than the maxScore, then update the maxScore and the nextMove
            maxScore = score
            if depth == DEPTH: 
                nextMove = move
        gs.undoMove() 
    return maxScore

'''
Recursive function to find the best move for the current player utilizing MinMax with Alpha Beta Pruning
'''
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier): #alpha is the best score that the maximizing player can guarantee at that level or above, beta is the best score that the minimizing player can guarantee at that level or above
    global nextMove
    if depth == 0: #if we have reached the depth limit
        return turnMultiplier * scoreBoard(gs) #return the score of the board
    
    #move ordering - implement later 
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)  
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier) #negative because we are looking at the opponent's score, whatever is best score for opponent is worst score for us
        if score > maxScore: #based on maximizing the score, if the score is greater than the maxScore, then update the maxScore and the nextMove
            maxScore = score
            if depth == DEPTH: 
                nextMove = move
        gs.undoMove() 
        #alpha beta pruning
        if maxScore > alpha: #if the maximizing player has found a move that is better than the best move the minimizing player has available, then update the best move the minimizing player has available
            alpha = maxScore
        if alpha >= beta: #if the maximizing player has found a move that is as good as or better than the best move the minimizing player has available, then break
            break #we won't look at any more moves  
    return maxScore  
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
    for row in range(len(board)): #iterate through the rows
        for col in range(len(board[row])): #iterate through the columns
            square = board[row][col]
            if square != "--": #if the square is not empty
                #score it positionally
                piecePositionScore = 0
                if square[1] in piecePositionScores:
                    if square[1] == "N":
                        piecePositionScore = piecePositionScores[square[1]][row][col] * .1
                    elif square[1] == "B":
                        piecePositionScore = piecePositionScores[square[1]][row][col] * .1
                    elif square[1] == "R":
                        piecePositionScore = piecePositionScores[square[1]][row][col] * .1
                if square[0] == 'w': #if the piece is white
                    score += pieceScore[square[1]] + piecePositionScore * .1 #add the value of the piece to the score
                elif square[0] == 'b': #if the piece is black
                    score -= pieceScore[square[1]] + piecePositionScore * .1 #subtract the value of the piece from the score
    return score