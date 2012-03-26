import random
import sys

def drawBoard(board):
	"""This function prints out the board that it was passed. returns None."""
	HLINE = '  +---+---+---+---+---+---+---+---+'
	VLINE = '  |   |   |   |   |   |   |   |   |'

	print '    1   2   3   4   5   6   7   8',
	print HLINE,
	for y in range(8):
		print VLINE,
		print y+1+' ',
		for x in range(8):
			print '| %s ' % (board[x][y]),
		print '|'
		print VLINE
		print HLINE
	

def resetBoard(board):
	"""Blanks out the board it is passed, except for the original starting position."""
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
	If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
	"""
	if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
		return False

	board[xstart][ystart] = tile #temporarily set tile on the board

	if tile == 'X'
		other_tile = 'O'
	else:
		other_tile = 'X'

	tiles_to_flip = []
	for xdirection, ydirection in [[0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0], [-1, 1]]:
		x, y = xstart, ystart
		x += xdirection #first step in the direction
		y += ydirection #first step in the direction
		if not isOnBoard(x, y):
			continue
		while board[x][y] == other_tile:
			x += xdirection
			y += ydirection
			if not isOnBoard(x, y): #break out of while loop, then continue in for loop
				break
		if not isOnBoard(x, y):
			continue
		if board[x][y] == tile:
			#There are pieces to flip over. Go in the reverse direction until we reach 
			#the original space, noting all the tiles along the way
			while True:
				x -= xdirection
				y -= ydirection
				if x == xstart and y == ystart:
					break
				tiles_to_flip.append([x,y])
	
	board[xstart][ystart] = ' ' #restore the empty space
	return tiles_to_flip


def isOnBoard(x, y):
	"""Returns True if the coordinates are located on the board."""
	return x >= 0 and x <= 7 and y >= 0 and y <= 7



