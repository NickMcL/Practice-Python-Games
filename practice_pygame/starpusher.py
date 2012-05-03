#Star Pusher (made with guidance from Invent with Python

import random
import sys
import copy
import os
import pygame
from pygame.locals import *

#Constants
FPS = 30
WIN_WIDTH = 800
WIN_HEIGHT = 600
HALF_WIN_WIDTH = int(WIN_WIDTH / 2)
HALF_WIN_HEIGHT = int(WIN_HEIGHT / 2)

TILE_WIDTH = 50
TILE_HEIGHT = 85
TILE_FLOOR_HEIGHT = 45

CAM_MOVE_SPEED = 5

OUTSIDE_DECORATION_PCT = 20

BRIGHT_BLUE = (0, 170, 255)
WHITE = (255, 255, 255)
BG_COLOR = BRIGHT_BLUE
TEXT_COLOR = WHITE

R_PATH = 'resources/starpusher/'

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def main():
    """Initialize pygame, game resources, and the main game loop"""
    global FPS_CLOCK, DISPLAY_SURF, IMAGES_DICT, TILE_MAPPING,
    OUTSIDE_DECO_MAPPING, BASIC_FONT, PLAYER_IMAGES, current_image

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Star Pusher')
    BASIC_FONT = pygame.font.Font(R_PATH + 'freesansbold.ttf', 18)
    
    IMAGES_DICT = {'star': pygame.image.load(R_PATH + 'star.png'),
            'uncovered goal': pygame.image.load(R_PATH + 'RedSelector.png'),
            'covered goal': pygame.image.load(R_PATH + 'Selector.png'),
            'corner': pygame.image.load(R_PATH + 'Wall Block Tall.png'),
            'wall': pygame.image.load(R_PATH + 'Wood Block Tall.png'),
            'inside floor': pygame.image.load(R_PATH + 'Plain Block.png'),
            'outside floor': pygame.image.load(R_PATH + 'Grass Block.png'),
            'title': pygame.image.load(R_PATH + 'star_title.png'),
            'solved': pygame.image.load(R_PATH + 'star_solved.png'),
            'princess': pygame.image.load(R_PATH + 'princess.png'),
            'boy': pygame.image.load(R_PATH + 'boy.png'),
            'catgirl': pygame.image.load(R_PATH + 'catgirl.png'),
            'horngirl': pygame.image.load(R_PATH + 'horngirl.png'),
            'pinkgirl': pygame.image.load(R_PATH + 'pinkgirl.png'),
            'rock': pygame.image.load(R_PATH + 'Rock.png'),
            'short tree': pygame.image.load(R_PATH + 'Tree_Short.png'),
            'tall tree': pygame.image.load(R_PATH + 'Tree_Tall.png'),
            'ugly tree': pygame.image.load(R_PATH + 'Tree_Ugly.png')}

    #Map the character that appears in the level file to the Surface object it
    #represents
    TILE_MAPPING = {'x': IMAGES_DICT['corner'],
                    '#': IMAGES_DICT['wall'].
                    'o': IMAGES_DICT['inside floor'],
                    '': IMAGES_DICT['outside floor']}
    OUTSIDE_DECO_MAPPING = {'1': IMAGES_DICT['rock'],
                            '2': IMAGES_DICT['short tree'],
                            '3': IMAGES_DICT['tall tree'],
                            '4': IMAGES_DICT['ugly tree']}

    startScreen()

    #Read in levels from the text file. Can make my own levels later.
    levels = readLevelsFile(R_PATH + 'starPusherLevels.txt')
    current_level_index = 0
