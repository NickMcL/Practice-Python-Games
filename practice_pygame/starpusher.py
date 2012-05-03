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

    #Main game loop. Runs a single level, then loads the next level once the
    #current one is finished
    while True:
        result = runLevel(levels, current_level_index)

        if result in ('solved', 'next'):
            current_level_index += 1
            if current_level_index >= len(levels):
                current_level_index = 0
        elif result == 'back':
            current_level_index -= 1
            if current_level_index < 0:
                current_level_index = len(levels) - 1
        elif result == 'reset':
            pass


def runLevel(levels, level_num):
    #Inializing variables for the level
    global current_image
    level_obj = levels[level_num]
    map_obj = decorateMap(level_obj['map_obj'],
                          level_obj['start_state']['player'])
    game_state_obj = copy.deepcopy(level_obj['start_state'])
    map_needs_redraw = True
    level_surf = BASIC_FONT.render('Level %s of %s' % 
                                   (level_obj['level_num'] + 1, 
                                    total_num_of_levels), 1, TEXT_COLOR)
    level_rect = level_surf.get_rect()
    level_rect.bottomleft = (20, WIN_HEIGHT - 35)
    map_width = len(map_obj) * TILE_WIDTH
    map_height = len(map_obj[0] - 1) * (TILE_HEIGHT - TILE_FLOOR_HEIGHT) +\
            TILE_HEIGHT
    MAX_CAM_X_PAN = abs(HALF_WIN_HEIGHT - int(map_height / 2)) + TILE_WIDTH
    MAX_CAM_Y_PAN = abs(HALF_WIN_HEIGHT - int(map_width / 2)) + TILE_HEIGHT

    level_is_complete = False
    camera_offset_x = 0
    camera_offset_y - 0
    camera_up = False
    camera_down = False
    camera_left = False
    camera_right = False
    
    #Game loop
    while True:
        #Reset these variables
        player_move_to = None
        key_pressed = False

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                key_pressed = True
                #Movement
                if event.key == K_LEFT:
                    player_move_to = LEFT
                elif event.key == K_RIGHT:
                    player_move_to = RIGHT
                elif event.key == K_UP:
                    player_move_to = UP
                elif event.key == K_DONW:
                    player_move_to = DOWN

                #Camera
                elif event.key == K_a:
                    camera_left = True
                elif event.key == K_d:
                    camera_right = True
                elif event.key == K_w:
                    camera_up = True
                elif event.key == K_s:
                    camera_down = True
                
                #Various other commands
                elif event.key == K_n:
                    return 'next'
                elif event.key == K_b:
                    return 'back'

                elif event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_BACKSPACE:
                    return 'reset'
                elif event.key == K_p:
                    #Change avatar
                    current_image += 1
                    if current_image >= len(PLAYER_IMAGES):
                        current_image = 0
                    map_needs_redraw = True

            elif event.type == KEYUP:
                #Unset camera move mode
                if event.key == K_a:
                    camera_left = False
                elif event.key == K_d:
                    camera_right = False
                elif event.key == K_w:
                    camera_up = False
                elif event.key == K_s:
                    camera_down = False

        if player_move_to != None and not level_is_complete:
            moved = makeMove(map_obj, game_state_obj, player_move_to)

            if moved:
                game_state_obj['step_counter'] += 1
                map_needs_redraw = True

            if isLevelFinished(level_obj, game_state_obj):
                level_is_complete = True
                key_pressed = False

        DISPLAY_SURF.fill(BG_COLOR)

        if map_needs_redraw:
            map_surf = drawMap(map_obj, game_state_obj, level_obj['goals'])
            map_needs_redraw = False

        if camera_up and camera_offset_y < MAX_CAM_X_PAN:
            camera_offset_y += CAM_MOVE_SPEED
        elif camera_down and camera_offset_y > -MAX_CAM_X_PAN:
            camera_offset_y -= CAM_MOVE_SPEED
        if camera_left and camera_offset_x < MAX_CAM_Y_PAN:
            camera_offset_x += CAM_MOVE_SPEED
        elif camera_right and camera_offset_x < -MAX_CAM_Y_PAN:
            camera_offset_x -= CAM)MOVE_SPEED

        #Adjust map_surf's Rect based on the camera offset
        map_surf_rect = map_surf.get_rect()
        map_surf_rect.center = (HALF_WIN_WIDTH + camera_offset_x,
                                HALF_WIN_HEIGHT + camera_offset_y)

        DISPLAY_SURF.blit(map_surf, map_surf_rect)

        DISPLAY_SURF.blit(level_surf, level_rect)
        step_surf = BASIC_FONT.render('Steps: %s' %
                                      (game_state_obj['step_counter']), 1,
                                      TEXT_COLOR)
        step_rect = step_surf.get_rect()
        step_rect.bottomleft = (20, WIN_HEIGHT - 10)
        DISPLAY_SURF.blit(step_surf, step_rect)

        if level_is_complete:
            solved_rect = IMAGES_DICT['solved'].get_rect()
            solved_rect.center = (HALF_WIN_WIDTH, HALF_WIN_HEIGHT)
            DISPLAY_SURF.blit(step_surf, step_rect)

            if key_pressed:
                return 'solved'
            
        pygame.display.update()
        FPS_CLOCK.tick()


def decorateMap(map_obj, start_xy):
   """Makes a copy of the given map object and modifies it.
    Here is what is done to it:
         * Walls that are corners are turned into corner pieces.
         * The outside/inside floor tile distinction is made.
         * Tree/rock decorations are randomly added to the outside tiles.
     
    Returns the decorated map object."""

    startx, starty = start_xy

    #Copy map object to avoid modifying the original
    map_obj_copy = copy.deepcopy(map_obj)

    #Remove non-wall characters
    for x in range(len(map_obj_copy)):
        for y in range(len(map_obj_copy[0])):
            if map_obj_copy[x][y] in ('$', '.', '@', '+', '*'):
                map_obj_copy[x][y] = ''

    #Flood fill to determine inside/outside floor tiles
    floodFill(map_obj_copy, startx, starty, '', 'o')

    #Convert the adjoined walls into corner tiles
    for x in range(len(map_obj_copy)):
        for y in range(len(map_obj_copy[0])):

            if mapObjCopy[x][y] == '#':
                if (isWall(mapObjCopy, x, y-1) and isWall(mapObjCopy, x+1, y)) or \
                    (isWall(mapObjCopy, x+1, y) and isWall(mapObjCopy, x, y+1)) or \
                    (isWall(mapObjCopy, x, y+1) and isWall(mapObjCopy, x-1, y)) or \
                    (isWall(mapObjCopy, x-1, y) and isWall(mapObjCopy, x, y-1)):
                     map_obj_copy[x][y] = 'x'
            
            elif map_obj_copy[x][y] == '' and random.randint(0, 99) <
            OUTSIDE_DECORATION_PCT:
                map_obj_copy[x][y] =\
                        random.choice(list(OUTSIDE_DECO_MAPPING.keys()))
    
    return map_obj_copy


def isBlocked(map_obj, game_state_obj, x, y):
    """Returns True if the (x,y) position on the map is blocked by a wall or
    star, otherwise return False"""

    if isWall(map_obj, x, y):
        return True

    elif x < 0 or x >= len(map_obj) or y < 0 or y >= len(map_obj[x]):
        return True

    elif (x, y) in game_state_obj['stars']:
        return True

    return False


def makeMove(map_obj, game_state_obj, player_move_to):
    """Given a map and game state object, see if it is possible for the
    player to make the given move. If it is, then change the player's
    position (and the position of any pushed star). If not, do nothing.
    
    Returns True if the player moved, otherwise False."""

    playerx, playery = game_state_obj['player']
    stars = game_state_obj['stars']

    if player_move_to == UP:
        x_offset = 0
        y_offset = -1
    elif player_move_to == RIGHT:
        x_offset = 1
        y_offset = 0
    elif player_move_to == DOWN:
        x_offset = 0
        y_offset = 1
    elif player_move_to == LEFT:
        x_offset = -1
        y_offset = 0

    #See if the player can move in that direction
    if isWall(map_obj, playerx + x_offset, playery + y_offset):
        return False
    else:
        if (playerx + x_offset, playery + y_offset) in stars:
            if not isBlocked(map_obj, game_state_obj, playerx + (x_offset*2),
                             playery + (y_offset*2)):
                ind = stars.index((playerx + x_offset, playery + y_offset))
                stars[ind] = (stars[ind][0] + x_offset, stars[ind][1] +
                              y_offset)
            else:
                return False

        game_state_obj['player'] = (playerx + x_offset, playery + y_offset)
        return True


def startScreen():
    """Display the start screen (which has the title and instruction) until the
    player presses a key. Returns None."""

    #Position of title image
    title_rect = IMAGES_DICT['title'].get_rect()
    top_coord = 50
    title_rect.top = top_coord
    title_rect.centerx = HALF_WIN_WIDTH
    top_coord += title_rect.height

    instruction_text = ['Push the starts over the marks.', 'Arrow keys to move,
                        WASD for camera control, P to change avatar.',
                        'Backsapce to reset level, Esc to quit.', 'N for next
                        level, B to go back a level.']

    DISPLAY_SURF.fill(BG_COLOR)
    DISPLAY_SURF.blit(IMAGES_DICT['title'], title_rect)

    for i in range(len(instruction_text)):
        inst_surf = BASIC_FONT.render(instruction_text[i], 1, TEXT_COLOR)
        inst_rect = inst_surf.get_rect()
        top_coord += 10
        inst_rect.top = top_coord
        inst_rect.centerx = HALF_WIN_WIDTH
        top_coord += inst_rect.height
        DISPLAY_SURF.blit(inst_surf, inst_rect)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

        pygame.display.update()
        FPS_CLOCK.tick()


def readLevelsFile(filename):

