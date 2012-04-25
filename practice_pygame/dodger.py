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

def drawText(text, font, surface, x, y, ref_point):
    """Draw text to the surface"""
    text_obj = font.render(text, 1, TEXT_COLOR)
    text_rect = text_obj.get_rect()
    if ref_point == 0:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x,y)
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
                                                              3), 0)
drawText('Press a key to start.', font, window_surface, (WINDOW_WIDTH / 2),
         (WINDOW_HEIGHT / 3) + 50, 0)
pygame.display.update()
waitForPlayerToPressKey()

#Game loop
top_score = 0
while True:
    #Initialization
    baddies = []
    score = 0
    player_rect.topleft = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)
    move_left = move_right = move_up = move_down = False
    reverse_cheat = slow_cheat = False
    baddie_add_counter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True:
        if not reverse_cheat and not slow_cheat:
            score += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverse_cheat = True
                if event.key == ord('x'):
                    slow_cheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    move_right = False
                    move_left = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    move_left = False
                    move_right = True
                if event.key == K_UP or event.key == ord('w'):
                    move_donw = False
                    move_up = True
                if event.key == K_DOWN or event.key == ord('s'):
                    move_up = False
                    move_down = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverse_cheat = False
                if event.key == ord('x'):
                    slow_cheat = False
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_LEFT or event.key == ord('a'):
                    move_left = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    move_right = False
                if event.key == K_UP or event.key == ord('w'):
                    move_up = False
                if event.key == K_DOWN or event.key == ord('s'):
                    move_down = False

            if event.type == MOUSEMOTION:
                player_rect.move_ip(event.pos[0] - player_rect.centerx,
                                    event.pos[1] - player_rect.centery)

        #Add baddies at the top of the screen
        if not reverse_cheat and not slow_cheat:
            baddie_add_counter += 1
        if baddie_add_counter == ADD_NEW_BADDIE_RATE:
            baddie_add_counter = 0
            baddie_size = random.randint(BADDIE_MIN_SIZE, BADDIE_MAX_SIZE)
            new_baddie = {'rect': pygame.Rect(random.randint
                                              (0, WINDOW_WIDTH-baddie_size),
                                              0 - baddie_size, baddie_size,
                                              baddie_size),
                          'speed': random.randint(BADDIE_MIN_SPEED,
                                                  BADDIE_MAX_SPEED),
                          'surface': pygame.transform.scale(baddie_image,
                                                            (baddie_size,
                                                             baddie_size)),
                         }

            baddies.append(new_baddie)

        #Move player
        if move_left and player_rect.left > 0:
            player_rect.move_ip(-1 * PLAYER_MOVE_RATE, 0)
        if move_right and player_rect.right < WINDOW_WIDTH:
            player_rect.move_ip(PLAYER_MOVE_RATE, 0)
        if move_up and player_rect.top > 0:
            player_rect.move_ip(0, -1 * PLAYER_MOVE_RATE)
        if move_down and player_rect.bottom < WINDOW_HEIGHT:
            player_rect.move_ip(0, PLAYER_MOVE_RATE)

        #Move the mouse cursor to match the player.
        pygame.mouse.set_pos(player_rect.centerx, player_rect.centery)

        #Move the baddies down
        for b in baddies:
            if not reverse_cheat and not slow_cheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverse_cheat:
                b['rect'].move_ip(0, -5)
                score = 0
            elif slow_cheat:
                b['rect'].move_ip(0, 1)
                score = 0

        #Delete baddies that have fallen past the bottom
        for b in baddies[:]:
            if b['rect'].top > WINDOW_HEIGHT:
                baddies.remove(b)

        window_surface.fill(BACKGROUND_COLOR)

        #Draw the score and top score
        drawText('Score: %s' % (score), font, window_surface, 10, 0, 1)
        drawText('Top Score: %s' % (top_score), font, window_surface, 10,
                 40, 1)

        #Draw the player's rectangle
        window_surface.blit(player_image, player_rect)

        #Draw each baddie
        for b in baddies:
            window_surface.blit(b['surface'], b['rect'])

        pygame.display.update()

        #Check if any of the baddies have hit the player
        if playerHasHitBaddie(player_rect, baddies):
            if score > top_score:
                top_score = score
            break

        main_clock.tick(FPS)

    #Stop the game and show the "Game Over" screen
    pygame.mixer.music.stop()

    drawText('GAME OVER', font, window_surface, (WINDOW_WIDTH / 2),
             (WINDOW_HEIGHT / 3), 0)
    drawText('Press a key to play again.', font, window_surface,
             (WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 3) + 50, 0)
    pygame.display.update()
    waitForPlayerToPressKey()
