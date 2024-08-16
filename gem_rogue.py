import pygame
from config import *
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    QUIT,
)

# initiate game
pygame.init()

# game clock
clock = pygame.time.Clock()

# basic screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# background
bg = pygame.Surface((2000, 2000))
x = 0
y = 0

# game loop
running = True
while running:
    # event handeler
    for event in pygame.event.get():
        # quit checks
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    
    # background
    bg.fill(BG_COLOR)

    screen.fill(BLACK)

    screen.blit(bg, (x, y))
    x -= 10
    y -= 10
    # display
    pygame.display.flip()

    # framerate
    clock.tick(30)

pygame.quit()