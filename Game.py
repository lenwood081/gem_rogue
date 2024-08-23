import pygame
from config import *
import random
from sprites.Background import Background
from sprites.Player import Player
from sprites.enemies.BlockFodder import BlockFodder
from sprites.HealthBar import HealthBar
from sprites.weapons.BasicGun import BasicGun
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    QUIT,
)


class Game:
    def __init__(self):
        #self.modifiers
        pass

    # main game loop
    def run_game_loop(self, screen):
        # game loop
        running = True

        # game clock
        clock = pygame.time.Clock()

        # background
        bg = Background()

        # player
        players = pygame.sprite.Group()
        player = Player(bg.location)
        players.add(player)

        # HUD
        health = HealthBar(player.max_health)

        # enemies
        enemies = pygame.sprite.Group()
        b1 = BlockFodder(1000, -1500)
        enemies.add(b1)

        # count
        count = 0

        # event varibles
        events = pygame.event.get()
        keys_pressed = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()

        # ----------------------------------- code for functions that run in main loop -----------------------------------
        
        def quit_handler():
            for event in events:
                # quit checks
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return False
                elif event.type == QUIT:
                    return False
            return True

        def blit_entiites():
            # screen
            screen.fill(BLACK)

            # blit calls
            bg.draw(screen)
            
            for em in enemies:
                em.draw(screen, bg.location)

            # health bar bg and player
            bg.draw_after(screen)
            health.draw(screen)
            player.draw(screen)
                    
        def colliosions():
            # player being attacked
            for em in enemies:
                if pygame.Rect.colliderect(em.hitbox_rect, player.rect):
                    player.take_damage(em.attack())

        def updates():
            # player and background 
            
            player.update(keys_pressed)
            bg.update(player.pos)
            player.update_after_background(keys_pressed, mouse_pressed, bg.location, enemies)

            for em in enemies:
                em.update(player.pos)
            health.update(player.current_health, player.max_health)

        def spawn_enemies(count):
            if count > 3 * FRAMERATE:
                count = 0
                new_enemy = BlockFodder(random.randint(0, BG_WIDTH), random.randint(-BG_HEIGHT, 0))
                enemies.add(new_enemy)
            count += 1
            return count
        # ----------------------------------- main loop ------------------------------------------------------------------
        
        while running:
            events = pygame.event.get()
            keys_pressed = pygame.key.get_pressed()
            mouse_pressed = pygame.mouse.get_pressed()

            # event handeler
            running = quit_handler()

            # blit to screen
            blit_entiites()
            
            # collisions
            colliosions()

            # updates
            updates()

            # spawn enemies
            count = spawn_enemies(count)

            # player death
            if len(players) == 0:
                running = False

            # display
            pygame.display.update()

            # framerate
            clock.tick(FRAMERATE)
