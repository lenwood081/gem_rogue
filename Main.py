# LONE MOON 

import pygame
from config import *
from Game import Game
from Menu import Menu

# --------------- TODO need to clean and normilise position -----------------------

# initate game
pygame.init()

# basic screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SCALED, vsync=1)
pygame.display.set_caption("Gem Rogue")

# main menu
main_menu = Menu()
main_menu.add_button("Enter", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, font_size=64)

# TODO main menu should have buttons to change starting run eventually


while True:
    if main_menu.start_menu(screen):
        # start game
        game = Game()
        game.run_game_loop(screen)
    else: 
        break

pygame.quit()