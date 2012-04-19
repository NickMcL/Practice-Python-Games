import pygame
import sys
import time
import random
from pygame.locals import *

#Initial setup
pygame.init()
main_clock = pygame.time.Clock()

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption('Sprites and Sound')

BLACK = (0, 0, 0)

#Block data structue
player = pygame.Rect(300, 100, 40, 40)
player_image = pygame.image.load('resources/player.png')
player_stretched_image = pygame.transform.scale(player_image, (40, 40))
food_image = pygame.image.load('resources/cherry.png')
foods = []
for i in range(20):
    foods.append(pygame.Rect(random.randint(0, WINDOW_WIDTH - 20),
                             random.randint(0, WINDOW_HEIGHT - 20), 20, 20))
food_counter = 0
NEW_FOOD = 40

#Keyboard variables
move_left = False
move_right = False
move_up = False
move_down = False

MOVE_SPEED = 6

#Sound setup
pygame.mixer.music.load('resources/background.mid')
pygame.mixer.music.play(-1, 0.0)
music_playing = True

#Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
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
                player.top = random.randint(0, WINDOW_HEIGHT - player.height)
                player.left = random.randint(0, WINDOW_WIDTH - player.width)
            if event.key == ord('m'):
                if music_playing:
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.play(-1, 0.0)
                music_playing = not music_playing

        if event.type == MOUSEBUTTONUP:
            foods.append(pygame.Rect(event.pos[0] - 10, event.pos[1] - 10, 20,
                                     20))

    food_counter += 1
    if food_counter >= NEW_FOOD:
        food_counter = 0
        foods.append(pygame.Rect(random.randint(0, WINDOW_WIDTH - 20), 
                                 random.randint(0, WINDOW_HEIGHT - 20), 20, 20))

    window_surface.fill(BLACK)

    if move_down and player.bottom < WINDOW_HEIGHT:
        player.top += MOVE_SPEED
    if move_up and player.top > 0:
        player.top -= MOVE_SPEED
    if move_left and player.left > 0:
        player.left -= MOVE_SPEED
    if move_right and player.right < WINDOW_WIDTH:
        player.right += MOVE_SPEED

    window_surface.blit(player_stretched_image, player)

    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food)
            player = pygame.Rect(player.left, player.top, player.width + 2,
                               player.height + 2)
            player_stretched_image = pygame.transform.scale(player_image,
                                                            (player.width,
                                                             player.height))

    for food in foods:
        window_surface.blit(food_image, food)

    pygame.display.update()
    main_clock.tick(40)
