import pygame
import time
from config import *
from Background.Stage import Stage
from sprites.Player import Player
from drops.ExperianceControl import ExperianceControl
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
        self.difficulty_factor = 10
        self.time = 0
        self.pause = False

    # main game loop
    def run_game_loop(self, screen):
        # sleep to prevent game events from the start menu from carrying
        pygame.time.wait(100)

        # game loop
        running = True

        # particles
        paritcles = pygame.sprite.Group()
        
        # game clock
        clock = pygame.time.Clock()
        
        # boundary collider
        boundary = pygame.sprite.Group()

        # projectiles group
        projectiles = pygame.sprite.Group()

        # player
        players = pygame.sprite.Group()
        player = Player(projectiles, paritcles)
        players.add(player)
        
        # menu manager
        menu = PauseMenu(player)

        # camera
        camera = Camera(player.pos)

        # HUD
        health = HealthBar(player.max_health)
        exp = ExpBar(player)

        # experiance
        experiance = ExperianceControl(players)
        
        # enemies
        enemies = pygame.sprite.Group()
        
        # background
        stage1 = Stage(boundary, paritcles, enemies, experiance.get_group(), projectiles, players, camera.get_offset(), self.difficulty_coeff)
        player.set_position(stage1.player_start_pos)
        stage1.iniciate(1)

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
            stage1.draw(screen, camera.get_offset())

            experiance.draw(screen, camera.get_offset())
            
            for em in enemies:
                em.draw(screen)

            # player
            player.draw(screen)

            # projectiles
            for proj in projectiles:
                proj.draw(screen)

            # particles
            for particle in paritcles:
                particle.draw(screen, camera.get_offset())  

            # after rendering effects
            stage1.draw_after(screen)
            
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

            # stage
            stage1.update(camera.get_offset(), dt, self.difficulty_coeff)

            player.update_after_camera(camera.get_offset(), enemies)

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

            # particles
            for particle in paritcles:
                particle.update(dt)

        def coeff_calculate(dt):
            self.time += 1 + dt
            equivalent_secounds = self.time / FRAMERATE
            self.difficulty_coeff = equivalent_secounds/60 * (self.difficulty_factor) * 0.2 + 1

        # ----------------------------------- main loop ------------------------------------------------------------------
        
        last_time = time.time()

        while running:
            dt = time.time() - last_time
            dt *= FRAMERATE
            last_time = time.time()
            self.
            # increase enemy difficulty if not paused
            if self.pause == False:
                coeff_calculate(dt)

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
                ret_val = menu.update(events)
                if ret_val == menu.EXIT_GAME:
                    self.pause = False
                    return False
                elif ret_val == menu.BACK or ret_val == menu.EXIT_MENU:
                    self.pause = False
                
            # blit to screen
            blit_entiites()

            # player death
            if len(players) == 0:
                running = False

            # display
            pygame.display.update()

            # framerate
            clock.tick(FRAMERATE)
