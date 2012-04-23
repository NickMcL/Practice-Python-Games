import pygame
import random
import sys
from pygame.locals import *

#Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)
FPS = 40
BADDIE_MIN_SIZE = 10
BADDIE_MAX_SIZE = 40
BADDIE_MIN_SPEED = 1
BADDIE_MAX_SPEED = 8
ADD_NEW_BADDIE_RATE = 6
PLAYER_MOVE_RATE = 5

def terminate():
    """Quits pygame and exits the program"""
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    """Loops until the player presses a key or exits the program"""
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

def playerHasHitBaddie(player_rect, baddies):
    """Check if the player has collided with a baddie"""
    for b in baddies:
        if player_rect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    """Draw text to the surface"""
    text_obj = font.render(text, 1, TEXT_COLOR)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

#Basic setup
pygame.init()
main_clock = pygame.time.Clock()
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

#Setup font
font = pygame.font.SysFont(None, 48)

#Setup sounds
pygame.mixer.music.load('resources/background.mid')

#Setup images
player_image = pygame.image.load('resources/player.png')
player_rect = player_image.get_rect()
baddie_image = pygame.image.load('resources/baddie.png')

#Display a "Start" screen
drawText('Dodger', font, window_surface, (WINDOW_WIDTH / 2), (WINDOW_HEIGHT /
                                                              3))
drawText('Press a key to start.', font, window_surface, (WINDOW_WIDTH / 2),
         (WINDOW_HEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()
