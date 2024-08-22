import pygame
from config import *
from Game import Game
from Menu import Menu

# --------------- TODO need to clean and normilise position -----------------------

# initate game
pygame.init()

# basic screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gem Rogue")

# main menu
main_menu = Menu()
main_menu.add_button("assets/UI/buttons/Enter.png", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 300, 100)

# TODO main menu should have buttons to change starting run eventually

# game
game = Game()

while True:
    if main_menu.start_menu(screen):
        # start game
        game.run_game_loop(screen)
    else: 
        break