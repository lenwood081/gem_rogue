import pygame
from config import *
from sprites.Background import Background
from sprites.Player import Player
from drops.ExperianceControl import ExperianceControl
from Directors.Enemy_Director_Continous import Enemy_Director_Continous
from Directors.Enemy_Director_Instant import Enemy_Director_Instant
from Camera.Camera import Camera
from HUD.HealthBar import HealthBar
from HUD.ExpBar import ExpBar
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    QUIT,
)


class Game:
    def __init__(self):
        #self.modifiers 1 - alot (gonna scale with time)
        self.difficulty_coeff = 1.2

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

        # camera
        camera = Camera(player.pos)

        # HUD
        health = HealthBar(player.max_health)
        exp = ExpBar(player)

        # enemies
        enemies = pygame.sprite.Group()

        # experiance
        experiance = ExperianceControl(players)

        # enemey directors
        instant_director = Enemy_Director_Instant(70, enemies, experiance.get_group())
        fast_director = Enemy_Director_Continous(enemies, 9, experiance.get_group())
        slow_director = Enemy_Director_Continous(enemies, 15, experiance.get_group())

        # spawn first enemys
        instant_director.activate(self.difficulty_coeff, player.pos)

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
            bg.draw(screen, camera.get_offset())

            experiance.draw(screen, camera.get_offset())
            
            for em in enemies:
                em.draw(screen, camera.get_offset())

            # health bar bg and player
            player.draw(screen)

            # after rendering effects
            bg.draw_after(screen)
            
            # hud
            health.draw(screen)
            exp.draw(screen)

        def updates():
            # director
            fast_director.update(self.difficulty_coeff, player.pos)
            slow_director.update(self.difficulty_coeff, player.pos)

            # player and background 
            
            player.update(keys_pressed)
            #bg.update(player.pos)
            camera.update(player.pos)
            player.update_after_background(keys_pressed, mouse_pressed, camera.get_offset(), enemies)

            for em in enemies:
                em.update(player, players)

            experiance.update()
            health.update(player.health, player.max_health)
            exp.update(player.level, player.exp_to_level, player.exp)

        def coeff_calculate(count):
            if count > 3 * FRAMERATE:
                count = 0
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
           
            # updates
            updates()

            # spawn enemies
            count = coeff_calculate(count)

            # player death
            if len(players) == 0:
                running = False

            # display
            pygame.display.update()

            # framerate
            clock.tick(FRAMERATE)
