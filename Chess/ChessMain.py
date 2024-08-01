import pygame as p
import ChessEngine
WIDTH = HEIGHT = 680 #400 is another option
DIMENSION = 8  #dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #for animations later on
IMAGES = {}

# this class is responsible for storing all the information about the current state of a chess game. It will also be responsible for determining the valid moves at the current state. It will also keep a move log.

'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''
def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # we can access an image by saying 'IMAGES['wp']'

'''
The main driver for our code. This will handle user input and updating the graphics
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    animate = False #flag variable for when we should animate a move
    loadImages() #only do this once, before the while loop
    running = True
    sqSelected = () #no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = [] #keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    gameOver = False #flag variable for when the game is over
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    sqSelected, playerClicks, moveMade, animate = handleMouseClick(e, sqSelected, playerClicks, gs, validMoves)
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gs.undoMove() #undo the last move
                    moveMade = True
                    animate = False
                if e.key == p.K_r: #reset the board when 'r' is pressed
                    gs = ChessEngine.GameState() #reset the game state, instantiate a new game state
                    validMoves = gs.getValidMoves() #get the valid moves for the new game state
                    sqSelected = () #reset the square selected
                    playerClicks = [] #clear player clicks
                    moveMade = False
                    animate = False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock) #animate the last move made
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate')
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Highlight square selected and moves for piece selected
'''
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sqSelected is a piece that can be moved, this is a nested loop
            #highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE)) #the square that will be highlighted
            s.set_alpha(100) #transparency value -> 0 transparent; 255 opaque
            s.fill(p.Color('purple4')) # color the square red
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE)) # draw the square for the selected piece
            #highlight moves from that square
            s.fill(p.Color('plum')) # color the square orange
            for move in validMoves:
                if move.startRow == r and move.startCol == c: #the move is from the selected square
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE)) # draw the square for the valid move

'''
Responsible for all the graphics within a current game state.
'''
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen) #draw squares on the board
    highlightSquares(screen, gs, validMoves, sqSelected) #highlight square selected and moves for piece
    drawPieces(screen, gs.board) #draw pieces on top of those squares

'''
Draw the squares on the board. The top left square is always light
'''

def drawBoard(screen):
    global colors
    colors = [p.Color("burlywood"), p.Color("burlywood4")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw the pieces on the board using the current GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Animating a move
'''
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow #change in row, delta row
    dC = move.endCol - move.startCol #change in column, delta column
    framesPerSquare = 10 #frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare #total number of frames for a move
    for frame in range(frameCount + 1): # +1 to ensure the last frame is the end square
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount) #calculate the current row and column for the piece
        drawBoard(screen) #draw squares on the board for each frame
        drawPieces(screen, board) #draw pieces on top of those squares for each frame
        #erase the piece from its ending square
        color = colors[(move.endRow + move.endCol) % 2] #color of the square
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE) #rectangle for the end square
        p.draw.rect(screen, color, endSquare) #draw a rectangle on the end square
        #draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare) #draw the captured piece on the end square
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))  
        p.display.flip() #update the screen for each frame
        clock.tick(60) #speed of the animation, 60 frames per second

'''
Draw the text on the screen
'''
def drawText(screen, text):
    font = p.font.SysFont('Helvitca', 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2) #center the text
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))


'''
Handling mouse clicks/user input
'''
def handleMouseClick(e, sqSelected, playerClicks, gs, validMoves):
    location = p.mouse.get_pos() #(x, y) location of the mouse
    col = location[0]//SQ_SIZE
    row = location[1]//SQ_SIZE
    if sqSelected == (row, col): #the user clicked the same square twice
        sqSelected = () #deselect
        playerClicks = [] #clear player clicks
    else:
        sqSelected = (row, col)
        playerClicks.append(sqSelected) #append for both 1st and 2nd clicks
    moveMade = False
    animate = False
    if len(playerClicks) == 2: #after 2nd click
        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
        for i in range(len(validMoves)):
            if move == validMoves[i]:
                gs.makeMove(validMoves[i])
                moveMade = True
                animate = True
                sqSelected = () #reset user clicks
                playerClicks = []
            if not moveMade: #if the move is not valid
                playerClicks = [sqSelected] #only one click, keep the latest one
    return sqSelected, playerClicks, moveMade, animate

if __name__ == "__main__":
    main()