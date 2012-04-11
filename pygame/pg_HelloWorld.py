#Made with guidance from Invent with Python

import sys
import pygame
from pygame.locals import *

#Set up pygame
pygame.init()

#Set up the window
window_surface = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption('Hello world!')

#Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#Set up fonts
basic_font = pygame.font.SysFont(None, 48)

#Set up the text
text = basic_font.render('Hello world!', True, WHITE, BLUE)
text_rect = text.get_rect()
text_rect.centerx = window_surface.get_rect().centerx
text_rect.centery = window_surface.get_rect().centery

#Draw the white background onto the surface
window_surface.fill(WHITE)

#Draw a green polygon onto the surface
pygame.draw.polygon(window_surface, GREEN, ((146, 0), (291, 106), (236, 277),
                                            (56, 277), (0, 106)))

#Draw some blue lines onto the surface
pygame.draw.line(window_surface, BLUE, (60, 60), (120, 60), 4)
pygame.draw.line(window_surface, BLUE, (120, 60), (60, 120))
pygame.draw.line(window_surface, BLUE, (60, 120), (120, 120), 4)

#Draw a blue circle onto the surface
pygame.draw.circle(window_surface, BLUE, (300, 50), 20, 0)

#Draw a red ellipse onto the surface
pygame.draw.ellipse(window_surface, RED, (300, 250, 40, 80), 1)

#Draw the text's background rectangle onto the surface
pygame.draw.rect(window_surface, RED, (text_rect.left - 20, text_rect.top - 20,
                                        text_rect.width + 40, text_rect.height +
                                        40))

#Get a pixel array of the surface
pix_array = pygame.PixelArray(window_surface)
pix_array[480][380] = BLACK
del pix_array

#Draw the text onto the surface
window_surface.blit(text, text_rect)

#Draw the window onto the screen
pygame.display.update()

#Run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
