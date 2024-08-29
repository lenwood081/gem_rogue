import pygame
from config import *
from Background.Background import Background
from sprites.Player import Player
from drops.ExperianceControl import ExperianceControl
from Directors.Enemy_Director_Continous import Enemy_Director_Continous
from Directors.Enemy_Director_Instant import Enemy_Director_Instant
from sprites.Projectile import Projectile
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
        self.difficulty_coeff = 1
        self.difficulty_factor = 3
        self.time = 0

    # main game loop
    def run_game_loop(self, screen):
        # sleep to prevent game events from the start menu from carrying
        pygame.time.wait(100)

        # game loop
        running = True

        # game clock
        clock = pygame.time.Clock()
        
        # boundary collider
        boundary = pygame.sprite.Group()

        # projectiles group
        projectiles = pygame.sprite.Group()

        # background
        bg = Background(boundary)

        # player
        players = pygame.sprite.Group()
        player = Player(projectiles)
        players.add(player)

        # camera
        camera = Camera(player.pos)

        # HUD
        health = HealthBar(player.max_health)
        exp = ExpBar(player)

        # experiance
        experiance = ExperianceControl(players)
        
        
        # enemies
        enemies = pygame.sprite.Group()
    
        # enemey directors
        instant_director = Enemy_Director_Instant(150, enemies, experiance.get_group(), projectiles, player)
        fast_director = Enemy_Director_Continous(enemies, 5, experiance.get_group(), projectiles, player)
        slow_director = Enemy_Director_Continous(enemies, 15, experiance.get_group(), projectiles, player)
        big_wave_director = Enemy_Director_Continous(enemies, 60, experiance.get_group(), projectiles, player)

        # spawn first enemys
        instant_director.activate(self.difficulty_coeff, player.pos)

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
                em.draw(screen)

            # player
            player.draw(screen)

            # projectiles
            for proj in projectiles:
                proj.draw(screen)

            # after rendering effects
            bg.draw_after(screen, camera.get_offset())
            
            # hud
            health.draw(screen)
            exp.draw(screen)

        def updates():
            # director
            fast_director.update(self.difficulty_coeff, player.pos)
            slow_director.update(self.difficulty_coeff, player.pos)
            big_wave_director.update(self.difficulty_coeff, player.pos)

            # player and camera
            player.update(keys_pressed, boundary)
            camera.update(player.pos)
            bg.update(camera.get_offset())
            player.update_after_camera(keys_pressed, mouse_pressed, camera.get_offset(), enemies, boundary)

            # enemies
            for em in enemies:
                em.update(player, players, camera.get_offset(), boundary)

            # projectiles
            for proj in projectiles:
                proj.update(camera.get_offset(), boundary)

            # exp
            experiance.update()

            # HUD
            health.update(player.health, player.max_health)
            exp.update(player.level, player.exp_to_level, player.exp)

        def coeff_calculate():
            self.time += 1
            equivalent_secounds = self.time / FRAMERATE
            self.difficulty_coeff = equivalent_secounds/60 * (self.difficulty_factor) * 0.2 + 1


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

            

            # increase enemy difficulty
            coeff_calculate()

            # player death
            if len(players) == 0:
                running = False

            # display
            pygame.display.update()

            # framerate
            clock.tick(FRAMERATE)
