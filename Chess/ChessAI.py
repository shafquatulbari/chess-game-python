import random

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)] #return a random move

def findBestMove(gs, validMoves):
    return findRandomMove(validMoves) #temporary