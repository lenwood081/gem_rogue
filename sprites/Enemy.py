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
        self.speed = 2

        # direction and turning
        self.front = Direction(0.0) 
        self.turn_rate = 2 # degrees


    # 1 point direction eg 90 degrees would be (1, 0)
    def move_towards_player(self, player_pos):
        self.front.normal()
        player_dir = Direction(0.0)
        
        # make unit vector
        player_unit_vector = Point.unit_vector(player_pos, self.pos)

        # get angle from vector
        angle = math.atan2(player_unit_vector.y, player_unit_vector.x)
        # search for correct quadrant
        if player_unit_vector.x > 0 and player_unit_vector.y > 0:
            pass
        elif player_unit_vector.x < 0 and player_unit_vector.y > 0:
            angle = math.pi - angle
        elif player_unit_vector.x < 0 and player_unit_vector.y < 0:
            angle = math.pi + angle
        elif player_unit_vector.x > 0 and player_unit_vector.y < 0:
            angle = math.pi*2 - angle
        
        player_dir.dir = angle

        turn_dir = player_dir.leftOrRight(self.front.dir)
        # base case nearly facing character
        if math.fabs(player_dir.dir - self.front.dir) < math.radians(self.turn_rate):
            self.front.dir = player_dir.dir
        else:
            self.front.dir += turn_dir*math.radians(self.turn_rate)
        self.front.normal()
        print(self.front.dir)
        
        # calculate unit vector for front from angle
        move_dir = Point(0,0)
        move_dir.x = math.cos(self.front.dir)
        move_dir.y = math.sin(self.front.dir)
        magnitude = math.sqrt(move_dir.x*move_dir.x+move_dir.y*move_dir.y)
        move_dir.x = move_dir.x/magnitude
        move_dir.y = move_dir.y/magnitude
        
        return move_dir

