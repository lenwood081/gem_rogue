import pygame
from config import *
from sprites.Background import Background
from sprites.Player import Player
from sprites.enemies.BlockFodder import BlockFodder
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
bg = Background()

# player
player = Player()

# enemies
enemies = pygame.sprite.Group()
bl = BlockFodder(10, 10)
enemies.add(bl)

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
    
    # screen
    screen.fill(BLACK)

    # add player and background
    screen.blit(bg.surf, (bg.location.x, bg.location.y))
    screen.blit(player.surf, player.rect)
    # blit enemies
    for em in enemies:
        screen.blit(em.surf, (em.pos.x + bg.location.x, em.pos.y + bg.location.y)) 
    

    # player and background upadting and movement
    keys_pressed = pygame.key.get_pressed()
    player.update(keys_pressed=keys_pressed)
    bg.update(player_pos=player.pos)

    # display
    pygame.display.flip()

    # framerate
    clock.tick(30)

pygame.quit()