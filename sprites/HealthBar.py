import pygame
from classes.Point import Point
from config import (
    SCREEN_WIDTH,
)

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, health):
        super(HealthBar, self).__init__()
        
        self.width = 128 + health * 0.1
        self.height = 32
        self.outer_surf = pygame.transform.scale(pygame.image.load("assets/healthbar/HealthOuter.png").convert_alpha(), (self.width, self.height))
        self.inner_surf = pygame.Surface((self.width-10, self.height))
        self.inner_surf.fill((255, 0, 0))

        self.percentage = 1
        self.screen_pos = Point(20, 20)
        self.max_health = health
        self.health = health

    def draw(self, screen):
        screen.blit(self.inner_surf, (self.screen_pos.x + 10, self.screen_pos.y))
        screen.blit(self.outer_surf, (self.screen_pos.x, self.screen_pos.y))


    def update(self, health, max_health):
        if self.width > SCREEN_WIDTH - 40:
            self.max_health = max_health
            self.width = SCREEN_WIDTH - 40
            self.percentage = health/max_health
            self.inner_surf = pygame.Surface((self.percentage * self.width-10, self.height))
            self.outer_surf = pygame.transform.scale(pygame.image.load("assets/healthbar/HealthOuter.png").convert_alpha(), (self.width, self.height))
        elif self.max_health != max_health:
            self.max_health = max_health
            self.width = 128 + self.max_health * 0.1
            self.percentage = health/max_health
            self.inner_surf = pygame.Surface((self.percentage * self.width -10, self.height))
            self.outer_surf = pygame.transform.scale(pygame.image.load("assets/healthbar/HealthOuter.png").convert_alpha(), (self.width, self.height))
            print("increaseign")

        if health != self.health:
            self.health = health
            self.percentage = health/max_health
            if self.percentage < 0:
                self.percentage == 0
            self.inner_surf = pygame.Surface((self.percentage * self.width, self.height))

        self.inner_surf.fill((255, 0, 0))







