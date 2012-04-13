import pygame
import sys
import time
from pygame.locals import *

pygame.init()

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption('Animation')

#Set up direction variables
DOWN_LEFT = 1
DOWN_RIGHT = 3
UP_LEFT = 7
UP_RIGHT = 9

OPPOSITES = {DOWN_LEFT:UP_LEFT, DOWN_RIGHT:UP_RIGHT, UP_LEFT:DOWN_LEFT,
             UP_RIGHT:DOWN_RIGHT}

MOVE_SPEED = 4

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#Setup the block data structure
b1 = {'rect':pygame.Rect(300, 80, 50, 100), 'color':RED, 'dir':UP_RIGHT}
b2 = {'rect':pygame.Rect(200, 200, 20, 20), 'color':GREEN, 'dir':UP_LEFT}
b3 = {'rect':pygame.Rect(100, 150, 60, 60), 'color':BLUE, 'dir':DOWN_LEFT}
blocks = [b1, b2, b3]

#Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    window_surface.fill(BLACK)

    #Move the block data structures
    for b in blocks:
        if b['dir'] == DOWN_LEFT:
            b['rect'].left -= MOVE_SPEED
            b['rect'].top += MOVE_SPEED
        if b['dir'] == DOWN_RIGHT:
            b['rect'].left += MOVE_SPEED
            b['rect'].top += MOVE_SPEED
        if b['dir'] == UP_LEFT:
            b['rect'].left -= MOVE_SPEED
            b['rect'].top -= MOVE_SPEED
        if b['dir'] == UP_RIGHT:
            b['rect'].left += MOVE_SPEED
            b['rect'].top -= MOVE_SPEED

        #Check if the block has move out of the window
        if b['rect'].top < 0:
            if b['dir'] == UP_LEFT:
                b['dir'] = DOWN_LEFT
            if b['dir'] == UP_RIGHT:
                b['dir'] = DOWN_RIGHT
        if b['rect'].bottom > WINDOW_HEIGHT:
            if b['dir'] == DOWN_LEFT:
                b['dir'] = UP_LEFT
            if b['dir'] == DOWN_RIGHT:
                b['dir'] = UP_RIGHT
        if b['rect'].left < 0:
            if b['dir'] == DOWN_LEFT:
                b['dir'] = UP_LEFT
