import pygame
from config import *
from classes.Point import Point

class ExpBar(pygame.sprite.Sprite):
    def __init__(self, player):
        super(ExpBar, self).__init__()

        # dimensions
        self._width = SCREEN_WIDTH/2
        self._height = 20
        self._pos = Point((SCREEN_WIDTH-self._width)/2, SCREEN_HEIGHT-100)

        # create image of fixed length
        #self._outer_surf = pygame.transform.scale(pygame.image.load("assets/HUD/BarOuter.png").convert_alpha(), (self._width, self._height))
        self._inner_surf = pygame.Surface((0, self._height))

        # create level varible and text feilds on either side
        self._current_level = player.level
        self._target_level = self._current_level + 1
        self._exp_to_level = player.exp_to_level
        self._exp_current = player.exp


    def draw(self, screen):
        screen.blit(self._inner_surf, (self._pos.x, self._pos.y))
        #screen.blit(self._outer_surf, (self._pos.x, self._pos.y))

    def update(self, player_level, player_exp_to_level, player_current_exp):
        changed = False

        # check if changed 
        if player_level != self._current_level or player_exp_to_level != self._exp_to_level:
            self._current_level = player_level  
            self._target_level = player_level + 1
            self._exp_to_level = player_exp_to_level
            changed = True

        # move bar
        if player_current_exp != self._exp_current or changed:
            self._exp_current = player_current_exp
            percentage = self._exp_current/self._exp_to_level
            self._inner_surf = pygame.Surface((percentage * self._width, self._height))
            self._inner_surf.fill((0,255, 0))

