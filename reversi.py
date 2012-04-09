import random
import sys

def drawBoard(board):
    """This function prints out the board that it was passed. returns None."""
    HLINE = '  +---+---+---+---+---+---+---+---+'
    VLINE = '  |   |   |   |   |   |   |   |   |'

    print '    1   2   3   4   5   6   7   8'
    print HLINE
    for y in range(8):
        print VLINE
        print str(y+1),
        for x in range(8):
            print '| %s' % (board[x][y]),
        print '|'
        print VLINE
        print HLINE
    

def resetBoard(board):
    """Blanks out the board it is passed, except for the original 
    starting position.
    """
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '
    
    #Starting pieces
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'

    return board


def getNewBoard():
    """Creates a brand new, blank board data structure."""
    board = []
    for i in range(8):
        board.append([' '] * 8)
    
    return board


def isValidMove(board, tile, xstart, ystart):
    """Returns False if the player's move on space xstart, ystart is invalid.
    If it is a valid move, returns a list of spaces that would become the 
    player's if they made a move here.
    """
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False
    
    board[xstart][ystart] = tile #temporarily set tile on the board

    if tile == 'X':
        other_tile = 'O'
    else:
        other_tile = 'X'
    
    tiles_to_flip = []
    for xdirection, ydirection in [[0,1], [1,1], [1,0], [1,-1], [0,-1], 
                                [-1,-1], [-1,0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection #first step in the direction
        y += ydirection #first step in the direction
        if not isOnBoard(x, y):
            continue
        while board[x][y] == other_tile:
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y): 
                #break out of while loop, then continue in for loop
                break
        if not isOnBoard(x, y):
            continue
        if board[x][y] == tile:
            #There are pieces to flip over. Go in the reverse direction 
            #until we reach the original space, noting all the tiles 
            #along the way.
            while True:
                x -= xdirection
                y -= ydirection
                if x == xstart and y == ystart:
                    break
                tiles_to_flip.append([x,y])
    
    board[xstart][ystart] = ' ' #restore the empty space
    if tiles_to_flip == []:
        return False
    return tiles_to_flip


def isOnBoard(x, y):
    """Returns True if the coordinates are located on the board."""
    return x >= 0 and x <= 7 and y >= 0 and y <= 7


def getBoardWithValidMoves(board, tile):
    """Returns a new board with . marking the valid moves the given player 
    can make.
    """
    dupe_board = getBoardCopy(board)

    for x, y in getValidMoves(dupe_board, tile):
        dupe_board[x][y] = '.'
    return dupe_board


def getValidMoves(board, tile):
    """Returns a list of [x,y] lists of valid moves for the given player on the
    given board.
    """
    valid_moves = []

    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                valid_moves.append([x, y])
    return valid_moves


def getScoreOfBoard(board):
    """Determine the score by counting the tiles. Returns a dictionary with keys
    'X' and 'O'.
    """
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X':xscore, 'O':oscore}


def enterPlayerTile():
    """Let's the player type which tile they want to be.
    Returns a list with the player's tile as the first item, and the computer's
    tile as the second.
    """
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        tile = raw_input('Do you want to be X or O? ').upper()

    #The first element in the tuple is the player's tile, the second is the
    #computer's tile.
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def whoGoesFirst():
    """Randomly choose the player who goes first."""
    if random.randint(0,1) == 0:
        return 'computer'
    else:
        return 'player'


def playAgain():
    """This function returns True if the player wants to play again, otherwise
    it returns False.
    """
    return raw_input('Do you want to play again? (yes or no) \
                     ').lower().startswith('y')


def makeMove(board, tile, xstart, ystart):
    """Place the tile on the board at xstart, ystart, and flip any of the
    opponent's pieces.
    Returns False if this is an invalid move, True if it is valid.
    """
    tiles_to_flip = isValidMove(board, tile, xstart, ystart)

    if tiles_to_flip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tiles_to_flip:
        board[x][y] = tile
    return True


def getBoardCopy(board):
    """Make a duplicate of the board list and return the duplicate."""
    dupe_board = getNewBoard()

    for x in range(8):
        for y in range(8):
            dupe_board[x][y] = board[x][y]

    return dupe_board


def isOnCorner(x, y):
    """Returns True if the position is in one of the four corners."""
    return ((x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or
            (x == 7 and y == 7))


def getPlayerMove(board, player_tile):
    """Let the player type in their move.
    Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
    """
    DIGITS_1_TO_8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        move = raw_input('Enter your move, or type quit to end the game, ' +\
                         'or hints to turn off/on hints. ').lower()
        if move == 'quit':
            return 'quit'
        if move == 'hints':
            return 'hints'

        if len(move) == 2 and move[0] in DIGITS_1_TO_8 and move[1] in \
        DIGITS_1_TO_8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, player_tile, x, y) == False:
                continue
            else:
                break
        else:
            print 'That is not a valid move. Type the x digit (1-8), then ' + \
                    'the y digit (1-8).'
            print 'For example, 81 will be the top-right corner.'

    return [x, y]


def getComputerMove(board, computer_tile):
    """Given a board and the computer's tile, determine where to move.
    Returns the move as a [x, y] list.
    """
    possible_moves = getValidMoves(board, computer_tile)

    #Randomize the order of the possible moves
    random.shuffle(possible_moves)

    #Always go for a corner if available.
    for x, y in possible_moves:
        if isOnCorner(x, y):
            return [x, y]

    #Go through all the possible moves and remember the best scoring move
    best_score = -1
    for x, y in possible_moves:
        dupe_board= getBoardCopy(board)
        makeMove(dupe_board, computer_tile, x, y)
        score = getScoreOfBoard(dupe_board)[computer_tile]
        if score > best_score:
            best_move = [x, y]
            best_score = score
    return best_move


def showPoints(player_tile, computer_tile):
    """Prints out the current score."""
    scores = getScoreOfBoard(main_board)
    print ('You have %s points. The computer has %s points.' %
           (scores[player_tile], scores[computer_tile]))


#Main game loop
print 'Welcome to Reversi!'

while True:
    #Reset the board and game
    main_board = getNewBoard()
    resetBoard(main_board)
    player_tile, computer_tile = enterPlayerTile()
    show_hints = False
    turn = whoGoesFirst()
    print 'The ' + turn + ' will go first.'

    while True:
        if turn == 'player':
            #Player's turn
            if show_hints:
                valid_moves_board = getBoardWithValidMoves(main_board,
                                                         player_tile)
                drawBoard(valid_moves_board)
            else:
                drawBoard(main_board)
            showPoints(player_tile, computer_tile)
            move = getPlayerMove(main_board, player_tile)
            if move == 'quit':
                print 'Thanks for playing!'
                sys.exit()
            elif move == 'hints':
                show_hints = not show_hints
                continue
            else:
                makeMove(main_board, player_tile, move[0], move[1])

            if getValidMoves(main_board, computer_tile) == []:
                break
            else:
                turn = 'computer'

        else:
            #Computer's turn
            drawBoard(main_board)
            showPoints(player_tile, computer_tile)
            raw_input('Press Enter to see the computer\'s move. ')
            x, y = getComputerMove(main_board, computer_tile)
            makeMove(main_board, computer_tile, x, y)

            if getValidMoves(main_board, player_tile) == []:
                break
            else:
                turn = 'player'

    # Display the final score.
    drawBoard(main_board)
    scores = getScoreOfBoard(main_board)
    print 'X scored %s points. O scored %s points.' % (scores['X'], scores['O'])
    if scores[player_tile] > scores[computer_tile]:
        print 'You beat the computer by %s points! Congratulations!' % \
                (scores[player_tile] - scores[computer_tile])  
    elif scores[player_tile] < scores[computer_tile]:
        print 'You lost. The computer beat you by %s points.' % \
                (scores[computer_tile] - scores[player_tile])
    else:
        print 'The game was a tie!' 
    if not playAgain():
        break
