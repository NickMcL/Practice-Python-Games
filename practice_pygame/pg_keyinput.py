import pygame
import sys
import random
from pygame.locals import *

pygame.init()
main_clock = pygame.time.Clock()

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption('Keyboard Input')

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

food_counter = 0
NEW_FOOD = 40
FOOD_SIZE = 20
player = pygame.Rect(300, 100, 50, 50)
foods = []
for i in range(20):
    foods.append(pygame.Rect(random.randint(0, WINDOW_WIDTH - FOOD_SIZE),
                             random.randint(0, WINDOW_HEIGHT - FOOD_SIZE),
                             FOOD_SIZE, FOOD_SIZE))

#Setup movement variables
move_left = False
move_right = False
move_up = False
move_down = False

MOVE_SPEED = 6


#Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            #Change the keyboard variables
            if event.key == K_LEFT or event.key == ord('a'):
                move_right = False
                move_left = True
            if event.key == K_RIGHT or event.key == ord('d'):
                move_left = False
                move_right = True
            if event.key == K_UP or event.key == ord('w'):
                move_down = False
                move_up = True
            if event.key == K_DOWN or event.key == ord('s'):
                move_up = False
                move_down = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == ord('a'):
                move_left = False
            if event.key == K_RIGHT or event.key == ord('d'):
                move_right = False
            if event.key == K_UP or event.key == ord('w'):
                move_up = False
            if event.key == K_DOWN or event.key == ord('s'):
                move_down = False
            if event.key == ord('x'):
                #Moves player to a random position in the window
                player.top = random.randint(0, WINDOW_HEIGHT - player.height)
                player.left = random.randint(0, WINDOW_WIDTH - player.width)

        if event.type == MOUSEBUTTONUP:
            #Creates a food square at the clicked position
            foods.append(pygame.Rect(event.pos[0], event.pos[1], FOOD_SIZE,
                                     FOOD_SIZE))

    food_counter += 1
    if food_counter >= NEW_FOOD:
        #Add new food
        food_counter = 0
        foods.append(pygame.Rect(random.randint(0, WINDOW_WIDTH - FOOD_SIZE),
                             random.randint(0, WINDOW_HEIGHT - FOOD_SIZE),
                             FOOD_SIZE, FOOD_SIZE))

    window_surface.fill(BLACK)

    #Move the player
    if move_down and player.bottom < WINDOW_HEIGHT:
        player.top += MOVE_SPEED
    if move_up and player.top > 0:
        player.top -= MOVE_SPEED
    if move_left and player.left > 0:
        player.left -= MOVE_SPEED
    if move_right and player.right < WINDOW_WIDTH:
        player.left += MOVE_SPEED

    pygame.draw.rect(window_surface, WHITE, player)

    #Check if the player has intersected with any food squares
    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food)

    for i in range(len(foods)):
        pygame.draw.rect(window_surface, GREEN, foods[i])

    pygame.display.update()
    main_clock.tick(40)
