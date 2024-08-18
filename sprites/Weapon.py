import pygame
from classes.Point import Point

class Weapon(pygame.sprite.Sprite):
    def __init__(self, parent_pos):
        super(Weapon, self).__init__()
        self.pos = Point(parent_pos.x, parent_pos.y)