import pygame
import sys
import random
from pygame.locals import *

def doRectsOverlap(rect1, rect2):
    """Checks if two rectangles overlap at any point"""
    for a, b in [(rect1, rect2), (rect2, rect1)]:
        if ((isPointInsideRect(a.left, a.top, b)) or
            (isPointInsideRect(a.left, a.bottom, b)) or
            (isPointInsideRect(a.right, a.top, b)) or
            (isPointInsideRect(a.right, a.bottom, b))):
            return True

    return False

def isPointInsideRect(x, y, rect):
    """Checks if the coordinate (x, y) is within the bounds of the rectangle"""
    return (x > rect.left) and (x < rect.right) and (y > rect.top) and \
            (y < rect.bottom)


pygame.init()
main_clock = pygame.time.Clock()

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption('Collision Detection')

#Setup various constants
DOWN_LEFT = 1
DOWN_RIGHT = 3
UP_LEFT = 7
UP_RIGHT = 9

MOVE_SPEED = 4

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

#Setup the bouncer and food data structures
food_counter = 0
NEW_FOOD = 40
FOOD_SIZE = 20
bouncer = {'rect':pygame.Rect(300, 100, 50, 50), 'dir':UP_LEFT}
foods = []
for i in range(20):
    foods.append(pygame.Rect(random.randint(0, WINDOW_WIDTH - FOOD_SIZE),
                             random.randint(0, WINDOW_HEIGHT - FOOD_SIZE),
                             FOOD_SIZE, FOOD_SIZE))

#Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    food_counter += 1
    if food_counter >= NEW_FOOD:
        #Add new food
        food_counter = 0
        foods.append(pygame.Rect(random.randint(0, WINDOW_WIDTH - FOOD_SIZE),
                             random.randint(0, WINDOW_HEIGHT - FOOD_SIZE),
                             FOOD_SIZE, FOOD_SIZE))

    window_surface.fill(BLACK)

    #Move the bouncer data structure
    if bouncer['dir'] == DOWN_LEFT:
        bouncer['rect'].left -= MOVE_SPEED
        bouncer['rect'].top += MOVE_SPEED
    if bouncer['dir'] == DOWN_RIGHT:
        bouncer['rect'].left += MOVE_SPEED
        bouncer['rect'].top += MOVE_SPEED
    if bouncer['dir'] == UP_LEFT:
        bouncer['rect'].left -= MOVE_SPEED
        bouncer['rect'].top -= MOVE_SPEED
    if bouncer['dir'] == UP_RIGHT:
        bouncer['rect'].left += MOVE_SPEED
        bouncer['rect'].top -= MOVE_SPEED

    #Check if the bouncer has moved out of the window
    if bouncer['rect'].top < 0:
        if bouncer['dir'] == UP_LEFT:
            bouncer['dir'] = DOWN_LEFT
        if bouncer['dir'] == UP_RIGHT:
            bouncer['dir'] = DOWN_RIGHT
    if bouncer['rect'].bottom > WINDOW_HEIGHT:
        if bouncer['dir'] == DOWN_LEFT:
            bouncer['dir'] = UP_LEFT
        if bouncer['dir'] == DOWN_RIGHT:
            bouncer['dir'] = UP_RIGHT
    if bouncer['rect'].left < 0:
        if bouncer['dir'] == DOWN_LEFT:
            bouncer['dir'] = DOWN_RIGHT
        if bouncer['dir'] == UP_LEFT:
            bouncer['dir'] = UP_RIGHT
    if bouncer['rect'].right > WINDOW_WIDTH:
        if bouncer['dir'] == DOWN_RIGHT:
            bouncer['dir'] = DOWN_LEFT
        if bouncer['dir'] == UP_RIGHT:
            bouncer['dir'] = UP_LEFT

    pygame.draw.rect(window_surface, WHITE, bouncer['rect'])
    
    #Check if the bouncer has intersected with any food squares
    for food in foods[:]:
        if doRectsOverlap(bouncer['rect'], food):
            foods.remove(food)

    for i in range(len(foods)):
        pygame.draw.rect(window_surface, GREEN, foods[i])

    pygame.display.update()
    main_clock.tick(40)
