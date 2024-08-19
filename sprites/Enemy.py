import pygame
import random
import math
from classes.Point import Point
from classes.Direction import Direction
from config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super(Enemy, self).__init__()
        self.pos = Point(x, y)

        self.surf = pygame.image.load(image_path).convert_alpha()
        self.surf_base = self.surf
        self.hitbox_rect = self.surf.get_rect()
        self.rect = self.hitbox_rect.copy()
        
        # health and damage taken
        self.health = 5
        self.armour = 0
        self.immune = False

        # direction and turning
        self.front = Direction(0.0) 
        self.VARIATION = 50
        self.target_variation = random.uniform(-self.VARIATION, self.VARIATION)
        self.lock_on_dist = 70      

        # slightly random speed
        self.base_speed = 4
        self.speed = random.uniform(self.base_speed, self.base_speed+3)  

        # attacking
        self.hit_damage = 1
        self.attack_damage = 2

    # occurs when colliding with a player
    # if in an attck then does more damage
    def attack(self):
        return self.attack_damage

    def death(self):
        self.kill()

    # for taking damage
    def take_damage(self, damage):
        if self.immune:
            return

        self.health -= damage - damage*(self.armour * 0.01)
        if self.health <= 0:
            self.death()

    # 1 point direction eg 90 degrees would be (1, 0)
    def move_towards_player(self, player_pos):
        player_pos_cpy = Point(player_pos.x, player_pos.y)

        # target variation is until a certain distance the enemy will vary its approach
        magnitude_sq = (self.pos.x-player_pos_cpy.x)**2 + (self.pos.y-player_pos_cpy.y)**2
        if magnitude_sq > self.lock_on_dist**2:
            player_pos_cpy.x += self.target_variation
            player_pos_cpy.y += self.target_variation

        # make unit vector
        player_unit_vector = Point.unit_vector(player_pos_cpy, self.pos)
        # rotate to face player
        player_dir = Point.direction_to_point(player_pos, self.pos)
        self.surf = Direction.rotate(player_dir.dir + math.pi/2, self.surf_base)
        self.rect = self.surf.get_rect(center=self.hitbox_rect.center)
        self.front.dir = player_dir.dir
        return player_unit_vector



# old code might use later

    """
    # get angle from vector
    angle = math.atan2(player_unit_vector.y, player_unit_vector.x)
    
    # search for correct quadrant (y is reversed)
    if player_unit_vector.x > 0 and player_unit_vector.y < 0:
        pass
    elif player_unit_vector.x < 0 and player_unit_vector.y < 0:
        angle = math.pi - angle
    elif player_unit_vector.x < 0 and player_unit_vector.y > 0:
        angle = math.pi + angle
    elif player_unit_vector.x > 0 and player_unit_vector.y > 0:
        angle = math.pi*2 - angle
    
    player_dir.dir = angle
    print(player_dir.dir)

    turn_dir = player_dir.leftOrRight(self.front.dir)
    # base case nearly facing character
    if math.fabs(player_dir.dir - self.front.dir) < math.radians(self.turn_rate):
        self.front.dir = player_dir.dir
    else:
        self.front.dir += turn_dir*math.radians(self.turn_rate)
    self.front.normal()
    #print(self.front.dir)
    
    # calculate unit vector for front from angle
    move_dir = Point(0,0)
    move_dir.x = math.cos(self.front.dir)
    move_dir.y = math.sin(self.front.dir)
    magnitude = math.sqrt(move_dir.x*move_dir.x+move_dir.y*move_dir.y)
    move_dir.x = move_dir.x/magnitude
    move_dir.y = move_dir.y/magnitude
    """
