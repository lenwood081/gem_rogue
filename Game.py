import pygame
from config import *
import random
from sprites.Background import Background
from sprites.Player import Player
from sprites.enemies.BlockFodder import BlockFodder
from drops.ExperianceControl import ExperianceControl
from HUD.HealthBar import HealthBar
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

        # experiance
        experiance = ExperianceControl(players)

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
                    # for debugging
                    # elif event.key == pygame.K_c:
                    #    experiance.clear()
                elif event.type == QUIT:
                    return False
            return True

        def blit_entiites():
            # screen
            screen.fill(BLACK)

            # blit calls
            bg.draw(screen)

            experiance.draw(screen, bg.location)
            
            for em in enemies:
                em.draw(screen, bg.location)

            # health bar bg and player
            player.draw(screen)

            # after rendering effects
            bg.draw_after(screen)
            
            # hud
            health.draw(screen)
                    
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

            experiance.update()
            health.update(player.current_health, player.max_health)

        def spawn_enemies(count):
            if count > 2 * FRAMERATE:
                count = 0
                new_enemy = BlockFodder(random.randint(0, BG_WIDTH), random.randint(-BG_HEIGHT, 0), experiance.get_group())
                enemies.add(new_enemy)
            count += 1
            return count
        # ----------------------------------- main loop ------------------------------------------------------------------
        
        while running:
            # get inputs
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
