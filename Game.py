import pygame
from config import *
from sprites.Background import Background
from sprites.Player import Player
from sprites.enemies.BlockFodder import BlockFodder
from sprites.HealthBar import HealthBar
from Menu import Menu
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    QUIT,
)


class Game:
    def __init__(self):
        pass
    
    @staticmethod
    def run_game_loop():
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

        # HUD
        health = HealthBar(player.max_health)

        # enemies
        enemies = pygame.sprite.Group()
        b1 = BlockFodder(1000, -1500)
        enemies.add(b1)

        # main menu
        main_menu = Menu()
        main_menu.add_button("assets/UI/buttons/Enter.png", 500, 500, 300, 100)

        # ----------------------------------- code for functions that run in main loop -----------------------------------
        
        def quit_handler():
            for event in pygame.event.get():
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
            screen.blit(bg.surf, (bg.location.x, bg.location.y))
            screen.blit(player.surf, player.rect)
            for em in enemies:
                em.draw(screen, bg.location)
            # health bar
            health.draw(screen)
            
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
            running = quit_handler()

            # blit to screen
            blit_entiites()
            
            # collisions
            colliosions()

            # updates
            updates()

            # TESTING for menu
            if player.current_health < player.max_health:
                running = main_menu.start_menu(screen)

            # display
            pygame.display.update()

            # framerate
            clock.tick(FRAMERATE)
        Game.close_game_instance()

    @staticmethod
    def close_game_instance():
        pygame.quit()