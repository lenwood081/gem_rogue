import pygame
import math
from classes.Point import Point
from classes.Direction import Direction
from config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, size_w, size_h):
        super(Enemy, self).__init__()
        self.pos = Point(x, y)
        self.surf = pygame.Surface((size_w, size_h))
        self.surf.fill(BLACK)
        self.rect = self.surf.get_rect()

        # direction and turning
        self.front = Direction(0.0)
        self.turn_speed = 20 # essentually a circle of radius 



    def move_towards_player(self, player_pos):
        
        pass

