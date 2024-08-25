import pygame
from classes.Point import Point
from config import (
    SCREEN_WIDTH,
)

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, max_health):
        super(HealthBar, self).__init__()
        
        self._width = 128 + max_health * 0.1
        self._height = 32
        self._outer_surf_base = pygame.image.load("assets/HUD/BarOuter.png").convert_alpha()
        self._outer_surf = pygame.transform.scale(self._outer_surf_base, (self._width, self._height))
        self._inner_surf = pygame.Surface((self._width, self._height))
        self._inner_surf.fill((255, 0, 0))

        self._percentage = 1
        self._screen_pos = Point(20, 20)
        self._max_health = max_health
        self._health = max_health

    def draw(self, screen):
        screen.blit(self._inner_surf, (self._screen_pos.x, self._screen_pos.y))
        screen.blit(self._outer_surf, (self._screen_pos.x, self._screen_pos.y))


    def update(self, health, max_health):
        self._width = 128 + max_health * 0.1

        # scaling 
        if self._width > SCREEN_WIDTH/2 - 100:
            self._width = SCREEN_WIDTH/2 - 100
            self._percentage = health/max_health
            self._outer_surf = pygame.transform.scale(self._outer_surf_base, (self._width, self._height))
        elif self._max_health != max_health:
            self._percentage = health/max_health
            self._outer_surf = pygame.transform.scale(self._outer_surf_base, (self._width, self._height))

        if health != self._health or self._max_health != max_health:
            self._max_health = max_health
            self._health = health
            self._percentage = health/max_health
            if self._percentage < 0:
                self._percentage = 0
            self._inner_surf = pygame.Surface((self._percentage * self._width, self._height))

        self._inner_surf.fill((255, 0, 0))







