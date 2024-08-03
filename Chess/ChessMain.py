import pygame as p
import ChessEngine, ChessAI
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

# creates a button on the screen
def create_button(screen, text, rect, hover=False):
    font = p.font.SysFont("Helvetica", 32)
    color = p.Color("DarkGray") if hover else p.Color("Gray")
    p.draw.rect(screen, color, rect)
    p.draw.rect(screen, p.Color("Black"), rect, 2)  # Border
    button_text = font.render(text, True, p.Color("Black"))
    text_rect = button_text.get_rect(center=rect.center)
    screen.blit(button_text, text_rect)

def create_back_button(screen):
    back_button_rect = p.Rect(10, 10, 100, 40)
    create_button(screen, "Back", back_button_rect)
    return back_button_rect

# Display the difficulty menu screen
def displayDifficultyMenu():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption('Select Difficulty')
    
    # Load the background image
    background_image = p.image.load("Chess/images/menu.png")
    background_image = p.transform.scale(background_image, (WIDTH, HEIGHT))
    
    button_easy_rect = p.Rect(WIDTH//2 - 150, HEIGHT//3 - 25, 300, 50)
    button_medium_rect = p.Rect(WIDTH//2 - 150, HEIGHT//2 - 25, 300, 50)
    button_hard_rect = p.Rect(WIDTH//2 - 150, HEIGHT*2//3 - 25, 300, 50)
    
    while True:
        screen.blit(background_image, (0, 0))
        
        mouse_pos = p.mouse.get_pos()
        
        back_button_rect = create_back_button(screen)
        
        create_button(screen, "Easy", button_easy_rect, button_easy_rect.collidepoint(mouse_pos))
        create_button(screen, "Medium", button_medium_rect, button_medium_rect.collidepoint(mouse_pos))
        create_button(screen, "Hard", button_hard_rect, button_hard_rect.collidepoint(mouse_pos))
        
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                return "quit"
            elif event.type == p.MOUSEBUTTONDOWN:
                if button_easy_rect.collidepoint(event.pos):
                    return "easy"
                elif button_medium_rect.collidepoint(event.pos):
                    return "medium"
                elif button_hard_rect.collidepoint(event.pos):
                    return "hard"
                elif back_button_rect.collidepoint(event.pos):
                    return "back"
        
        p.display.flip()



# Display the menu screen
def displayMenu():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption('Chess Menu')
    
    # Load the background image
    background_image = p.image.load("Chess/images/menu.png")
    background_image = p.transform.scale(background_image, (WIDTH, HEIGHT))
    
    button_1v1_computer_rect = p.Rect(WIDTH//2 - 150, HEIGHT//3 - 25, 300, 50)
    button_1v1_human_rect = p.Rect(WIDTH//2 - 150, HEIGHT//2 - 25, 300, 50)
    button_quit_rect = p.Rect(WIDTH//2 - 150, HEIGHT*2//3 - 25, 300, 50)
    
    while True:
        screen.blit(background_image, (0, 0))
        
        mouse_pos = p.mouse.get_pos()
        
        create_button(screen, "Play 1v1 (Computer)", button_1v1_computer_rect, button_1v1_computer_rect.collidepoint(mouse_pos))
        create_button(screen, "Play 1v1 (Human)", button_1v1_human_rect, button_1v1_human_rect.collidepoint(mouse_pos))
        create_button(screen, "Quit/Exit", button_quit_rect, button_quit_rect.collidepoint(mouse_pos))
        
        # Display "Created by Shafquat" text
        font = p.font.SysFont("Helvetica", 20)
        created_by_text = font.render("Created by Shafquat", True, p.Color("White"))
        screen.blit(created_by_text, (WIDTH - created_by_text.get_width() - 10, HEIGHT - created_by_text.get_height() - 10))
        
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                return "quit"
            elif event.type == p.MOUSEBUTTONDOWN:
                if button_1v1_computer_rect.collidepoint(event.pos):
                    return "computer"
                elif button_1v1_human_rect.collidepoint(event.pos):
                    return "human"
                elif button_quit_rect.collidepoint(event.pos):
                    p.quit()
                    return "quit"
        
        p.display.flip()

# Display the difficulty menu screen
def displayPauseMenu():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption('Pause Menu')
    
    # Load the background image
    background_image = p.image.load("Chess/images/menu.png")
    background_image = p.transform.scale(background_image, (WIDTH, HEIGHT))
    
    button_resume_rect = p.Rect(WIDTH//2 - 150, HEIGHT//3 - 25, 300, 50)
    button_main_menu_rect = p.Rect(WIDTH//2 - 150, HEIGHT//2 - 25, 300, 50)
    button_quit_rect = p.Rect(WIDTH//2 - 150, HEIGHT*2//3 - 25, 300, 50)
    
    while True:
        screen.blit(background_image, (0, 0))
        
        mouse_pos = p.mouse.get_pos()
        
        create_button(screen, "Resume", button_resume_rect, button_resume_rect.collidepoint(mouse_pos))
        create_button(screen, "Main Menu", button_main_menu_rect, button_main_menu_rect.collidepoint(mouse_pos))
        create_button(screen, "Quit", button_quit_rect, button_quit_rect.collidepoint(mouse_pos))
        
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                return "quit"
            elif event.type == p.MOUSEBUTTONDOWN:
                if button_resume_rect.collidepoint(event.pos):
                    return "resume"
                elif button_main_menu_rect.collidepoint(event.pos):
                    return "main_menu"
                elif button_quit_rect.collidepoint(event.pos):
                    return "quit"
        
        p.display.flip()



'''
The main driver for our code. This will handle user input and updating the graphics
'''
def main():
    while True:
        choice = displayMenu()
        if choice == "quit":
            return
        elif choice == "computer":
            difficulty = None
            while not difficulty:
                difficulty = displayDifficultyMenu()
                if difficulty == "back":
                    choice = "back"
                    break
                elif difficulty == "quit":
                    return
                elif difficulty == "easy":
                    ChessAI.DEPTH = 1
                elif difficulty == "medium":
                    ChessAI.DEPTH = 2
                elif difficulty == "hard":
                    ChessAI.DEPTH = 3
            if choice == "back":
                continue
            playerOne = True
            playerTwo = False
        elif choice == "human":
            playerOne = True
            playerTwo = True

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
            humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                #mouse handler
                elif e.type == p.MOUSEBUTTONDOWN:
                    if not gameOver and humanTurn:
                        sqSelected, playerClicks, moveMade, animate = handleMouseClick(e, sqSelected, playerClicks, gs, validMoves)
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z: #undo when 'z' is pressed
                        gs.undoMove() #undo the last move
                        moveMade = True
                        animate = False
                        gameOver = False
                    if e.key == p.K_r: #reset the board when 'r' is pressed
                        gs = ChessEngine.GameState() #reset the game state, instantiate a new game state
                        validMoves = gs.getValidMoves() #get the valid moves for the new game state
                        sqSelected = () #reset the square selected
                        playerClicks = [] #clear player clicks
                        moveMade = False
                        animate = False
                        gameOver = False
                    if e.key == p.K_ESCAPE: #pause the game when 'escape' is pressed
                        pause_choice = displayPauseMenu()
                        if pause_choice == "quit":
                            return
                        elif pause_choice == "main_menu":
                            running = False  # Exit the game loop to restart main menu
                        elif pause_choice == "resume":
                            continue  # resume the game

            #AI move finder logic
            if not gameOver and not humanTurn:
                AIMove = ChessAI.findBestMove(gs, validMoves)
                if AIMove is None: 
                    AIMove = ChessAI.findRandomMove(validMoves) #if the AI cannot find the best move, then make a random move 
                gs.makeMove(AIMove)
                moveMade = True
                animate = True

            if moveMade:
                if animate:
                    animateMove(gs.moveLog[-1], screen, gs.board, clock) #animate the last move made
                validMoves = gs.getValidMoves()
                moveMade = False
                animate = False

            drawGameState(screen, gs, validMoves, sqSelected)

            if gs.checkMate or gs.staleMate: 
                gameOver = True #the game is over
                text = 'Stalemate' if gs.staleMate else 'Black wins by checkmate' if gs.whiteToMove else 'White wins by checkmate' #if the game is over, then display the appropriate text
                drawText(screen, text) 
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
            if move.isEnpassantMove: #if it is an en passant move
                enPassantRow = (move.endRow + 1) if move.pieceCaptured[0] == 'b' else move.endRow - 1 #if it is an en passant move, then the captured piece is not on the end square, but on the square behind the pawn
                endSquare = p.Rect(move.endCol*SQ_SIZE, enPassantRow*SQ_SIZE, SQ_SIZE, SQ_SIZE) 
            screen.blit(IMAGES[move.pieceCaptured], endSquare) 
        #draw moving piece
        if move.pieceMoved != '--':
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
    if sqSelected == (row, col) or col >= 8: #the user clicked the same square twice or the user clicked outside the board
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