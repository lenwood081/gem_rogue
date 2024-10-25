import pygame
import time
from config import *
from Background.StageManager import StageManager
from Background.Stage import Stage 
from Background.Path import Path
from utility.Point import Point
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
        self.time_to_end = 4 * FRAMERATE
        self.alpha_increase = self.time_to_end / 255
        self.alpha_current = 0
        self.dead = False

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

        # activiators
        activators = pygame.sprite.Group()

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
        stages = StageManager(boundary, activators, paritcles, enemies, experiance.get_group(), projectiles, players, camera.get_offset())
        player.set_position(stages.active_stage.player_start_pos)
        
        
        # for effects
        self.surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surf.fill((50, 50, 50))

        # fade out screen
        fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade.fill((0, 0, 0))        
        #fade.fill((255, 255, 255))        

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
                elif event.type == QUIT:
                    return False
            return True

        def blit_entiites():
            # screen
            screen.fill(BLACK)

            # blit calls
            stages.draw(screen, camera.get_offset())
            
            #path.draw(screen, camera.get_offset())

            experiance.draw(screen, camera.get_offset())
            
            for em in enemies:
                em.draw(screen)

            # add darkness
            screen.blit(self.surf, (0,0), special_flags=pygame.BLEND_RGBA_SUB)

            
            # player
            if self.dead == False:
                player.draw(screen)

            # projectiles
            for proj in projectiles:
                proj.draw(screen)

            # particles
            for particle in paritcles:
                particle.draw(screen, camera.get_offset())  

            # after rendering effects
            #stages.draw_after(screen)
            
            # hud
            if self.dead == False:
                health.draw(screen)
                exp.draw(screen)

            # menu if paused
            if self.pause:
                menu.draw(screen)

        def updates(dt):
            # player and camera
            player.update(keys_pressed, mouse_pressed, boundary, activators, dt)
            camera.update(player.pos)

            # stage
            stages.update(camera.get_offset(), dt, self.difficulty_coeff)
            
            #path.update(camera.get_offset(), dt)

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
            print(dt)
            last_time = time.time()

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
            if self.pause == False and self.dead == False:
                updates(dt)
            elif self.pause:
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
                # turn off enemy 
                # fade to black
                self.dead = True
                
                self.alpha_current += self.alpha_increase
                self.alpha_current = min(self.alpha_current, 255)
                
                fade.set_alpha((int)(self.alpha_current))
                
                screen.blit(fade, (0, 0))
                
                self.time_to_end -= 1
                if (self.time_to_end <= 0):
                    running = False

            # display
            pygame.display.update()

            # framerate
            clock.tick(FRAMERATE)
