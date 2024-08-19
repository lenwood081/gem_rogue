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

# game loop
running = True

# game clock
clock = pygame.time.Clock()

# basic screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gem Rogue")

# background
bg = Background()

# player
player = Player()

# UI
health = HealthBar(player.max_health)

# enemies
enemies = pygame.sprite.Group()
b1 = BlockFodder(1000, -1500)
enemies.add(b1)

# ----------------------------------- code for functions that run in main loop -----------------------------------

def event_handler():
    for event in pygame.event.get():
        # quit checks
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

def blit_entiites():
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
    
def colliosions():
    # player being attacked
    for em in enemies:
        if pygame.Rect.colliderect(em.hitbox_rect, player.rect):
            player.take_damage(em.attack())

def updates():
    keys_pressed = pygame.key.get_pressed()
    player.update(keys_pressed)
    bg.update(player.pos)
    for em in enemies:
        em.update(player.pos)
    health.update(player.current_health, player.max_health)

# ----------------------------------- main loop ------------------------------------------------------------------

while running:
    # event handeler
    event_handler()

    # blit to screen
    blit_entiites()
    
    # collisions
    colliosions()

    # updates
    updates()

    # display
    pygame.display.update()

    # framerate
    clock.tick(FRAMERATE)

pygame.quit()