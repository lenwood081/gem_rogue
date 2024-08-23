import pygame
import random
import math
from classes.Point import Point
from classes.Direction import Direction
from config import *

# TODO impliment knoockbacl with target unnit vector and strength

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, width, height):
        super(Enemy, self).__init__()
        self.pos = Point(x, y)  

        # base image
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (width, height))
        self.image_base = self.image
        self.hitbox_rect = self.image.get_rect()
        self.rect = self.hitbox_rect.copy()

        # hurt image
        self.being_hurt = False
        self.time_refresh_currect = self.time_refresh = 7

        # health and damage taken
        self.health = 10
        self.armour = 0
        self.immune = False

        # direction and turning
        self.front = Direction(0.0) 
        self.pos_to_player = Point(self.pos.x, self.pos.y)
        self.turn_pixels = 6
        self.VARIATION = 60
        self.target_variation = random.uniform(-self.VARIATION, self.VARIATION)
        self.lock_on_dist = 100      

        # slightly random speed
        self.base_speed = 4
        self.speed = random.uniform(self.base_speed, self.base_speed+3)  

        # attacking
        self.hit_damage = 1
        self.attack_damage = 2

        # width and height
        self.width = width
        self.height = height

    # occurs when colliding with a player
    # if in an attck then does more damage
    def attack(self):
        return self.attack_damage

    # death function
    def death(self):
        self.kill()

    # for taking damage
    def take_damage(self, damage):
        if self.immune:
            return

        self.health -= damage - damage*(self.armour * 0.01)
        self.being_hurt = True
        self.time_refresh_currect = self.time_refresh
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

        # make unit vector for point to travel to
        player_unit_vector = Point.unit_vector(player_pos_cpy, self.pos)

        # rotate to face player
        player_dir = Point.direction_to_point(player_pos_cpy, self.pos)
        self.image = Direction.rotate(player_dir.dir + math.pi/2, self.image_base)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)
        self.front.dir = player_dir.dir + math.pi/2
        return player_unit_vector
    
    # check for being hit
    def being_hit(self):
        self.time_refresh_currect -= 1
        if self.time_refresh_currect <= 0:
            self.being_hurt = False
            self.time_refresh_currect = self.time_refresh
