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
        self.speed = 10

        # direction and turning
        self.front = Direction()
        self.turn_speed = 20 # essentually a circle of radius 


    # 1 point direction eg 90 degrees would be (1, 0)
    def move_towards_player(self, player_pos):
        move_dir = Point(0,0)
        
        # division by zero error
        if (player_pos.x+player_pos.y-self.pos.x-self.pos.y) == 0:
            pass
        move_dir.x = (player_pos.x)/(BG_WIDTH) 
        move_dir.y = (player_pos.y-self.pos.y)/(BG_HEIGHT)
        return move_dir

