import pygame
import time
from config import *
from Background.Background import Background
from sprites.Player import Player
from drops.ExperianceControl import ExperianceControl
from Directors.Enemy_Director_Continous import Enemy_Director_Continous
from Directors.Enemy_Director_Instant import Enemy_Director_Instant
from menus.Menu import PauseMenu
from Camera.Camera import Camera
from HUD.HealthBar import HealthBar
from HUD.ExpBar import ExpBar
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    QUIT,
    K_p
)


class Game:
    def __init__(self):
        #self.modifiers 1 - alot (gonna scale with time)
        self.difficulty_coeff = 1
        self.difficulty_factor = 3
        self.time = 0
        self.pause = False

    # main game loop
    def run_game_loop(self, screen):
        # sleep to prevent game events from the start menu from carrying
        pygame.time.wait(100)

        # game loop
        running = True

        # menu manager
        menu = PauseMenu()

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
        instant_director = Enemy_Director_Instant(150, enemies, experiance.get_group(), projectiles, players, camera.get_offset())
        fast_director = Enemy_Director_Continous(enemies, 5, experiance.get_group(), projectiles, players, camera.get_offset())
        slow_director = Enemy_Director_Continous(enemies, 15, experiance.get_group(), projectiles, players, camera.get_offset())
        big_wave_director = Enemy_Director_Continous(enemies, 60, experiance.get_group(), projectiles, players, camera.get_offset())

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
                        self.pause = True
                        print("pasuing")
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

            # menu if paused
            if self.pause:
                menu.draw(screen)

        def updates(dt):
            
            # player and camera
            player.update(keys_pressed, mouse_pressed, boundary, dt)
            camera.update(player.pos)
            bg.update(camera.get_offset())
            player.update_after_camera(camera.get_offset(), enemies)

            # director
            fast_director.update(self.difficulty_coeff, player.pos, camera.get_offset())
            slow_director.update(self.difficulty_coeff, player.pos, camera.get_offset())
            big_wave_director.update(self.difficulty_coeff, player.pos, camera.get_offset())

            # enemies
            for em in enemies:
                em.update(player, camera.get_offset(), boundary, dt)

            # projectiles
            for proj in projectiles:
                proj.update(camera.get_offset(), boundary, dt)

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
        
        last_time = time.time()

        while running:
            dt = time.time() - last_time
            dt *= FRAMERATE
            last_time = time.time()

            # get inputs
            events = pygame.event.get()
            keys_pressed = pygame.key.get_pressed()
            mouse_pressed = pygame.mouse.get_pressed()

            # event handeler if game is running
            if self.pause == False:
                running = quit_handler()

            # updates
            if self.pause == False:
                updates(dt)
            else:
                if menu.update(events) == False:
                    self.pause = False

            # blit to screen
            blit_entiites()
            

            # increase enemy difficulty
            coeff_calculate()

            # player death
            if len(players) == 0:
                running = False

            # display
            pygame.display.update()

            # framerate
            clock.tick(FRAMERATE)
