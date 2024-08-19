import pygame
from config import *
from sprites.Background import Background
from sprites.Player import Player
from sprites.enemies.BlockFodder import BlockFodder
from sprites.HealthBar import HealthBar
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

# UI
health = HealthBar(player.max_health)

# enemies
enemies = pygame.sprite.Group()
b1 = BlockFodder(1000, -1500)
#b2 = BlockFodder(1000, -1200)
#b3 = BlockFodder(500, -1500)
#b4 = BlockFodder(1000, -300)
enemies.add(b1)
#enemies.add(b2)
#enemies.add(b3)
#enemies.add(b4)


# game loop
running = True
while running:
    keys_pressed = pygame.key.get_pressed()
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

    # blit calls
    screen.blit(bg.surf, (bg.location.x, bg.location.y))
    screen.blit(player.surf, player.rect)
    for em in enemies:
        em.hitbox_rect = em.surf.get_rect(center=(
            em.pos.x + bg.location.x, 
            -em.pos.y + bg.location.y))
        screen.blit(em.surf, em.hitbox_rect) 
    # health bar
    screen.blit(health.inner_surf, (health.screen_pos.x + 10, health.screen_pos.y))
    screen.blit(health.outer_surf, (health.screen_pos.x, health.screen_pos.y))
    
    # check collisions
    for em in enemies:
        if pygame.Rect.colliderect(em.hitbox_rect, player.rect):
            player.take_damage(em.attack())

    # updates
    player.update(keys_pressed)
    bg.update(player.pos)
    for em in enemies:
        em.update(player.pos)
    health.update(player.current_health, player.max_health)

    # display
    pygame.display.flip()

    # framerate
    clock.tick(30)

pygame.quit()