import pygame
import random
import math
from classes.Point import Point
from classes.Direction import Direction
from drops.Experiance import Experiance
from sprites.ItemHolder import ItemHolder
from config import *

# TODO impliment knoockbacl with target unnit vector and strength

class Enemy(ItemHolder):
    def __init__(self, pos, image_path, size, experiance_group):
        super(Enemy, self).__init__()
        # ---------------------- ITEM HOLDER ATTRIBUTES -------------------

        # dimensions
        self.width = self.max_width = size[0]
        self.height = self.max_height = size[1]

        # immunity frames
        self.immunity_frames_gained = 1

        # -----------------------------------------------------------------

        self.pos = pos.copy() 

        # base image
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (self.width, self.height))
        self.image_base = self.image
        self.hitbox_rect = self.image.get_rect()
        self.rect = self.hitbox_rect.copy()

        # direction and turning
        self.front = Direction(0.0) 
        self.dist_player = 0
        self.target_unit_vector = Point(0, 0)
        self.turn_pixels = 6
        self.VARIATION = 60
        self.target_variation = random.uniform(-self.VARIATION, self.VARIATION)
        self.lock_on_dist = 300
    
        # drops
        self.experiance_group = experiance_group

        # fire (for when to attack)
        self.fire = True

    # occurs when colliding with a player
    # if in an attck then does more damage
    def attack(self):
        return self.damage

    # death function
    # override
    def death(self):
        self.kill()
        
        # drop experiance
        exp = Experiance(self.pos, self.exp)
        self.experiance_group.add(exp)


    # 1 point direction eg 90 degrees would be (1, 0)
    def move_towards_player(self, player_pos):
        if self.immune:
            self.immunity_frames -= 1
            if self.immunity_frames == 0:
                self.immune = False

        player_pos_cpy = player_pos.copy()

        # target variation is until a certain distance the enemy will vary its approach
        self.dist_player = Point.euclidian_dist(player_pos_cpy, self.pos)
        if self.dist_player > self.lock_on_dist:
            player_pos_cpy.x += self.target_variation
            player_pos_cpy.y += self.target_variation

        # make unit vector for point to travel to
        player_unit_vector = Point.unit_vector(player_pos_cpy, self.pos)

        # rotate to face player
        player_dir = Point.direction_to_point(player_pos_cpy, self.pos)
        self.image = Direction.rotate(player_dir.dir + math.pi/2, self.image_base)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)
        self.front.dir = player_dir.dir + math.pi/2
        self.target_unit_vector = player_unit_vector.copy()
        return player_unit_vector
    
    # check for being hit
    def being_hit(self):
        self.time_refresh_currect -= 1
        if self.time_refresh_currect <= 0:
            self.being_hurt = False
            self.time_refresh_currect = self.time_refresh

    # update method (general) can be overriden
    def update(self, player, enemy_group):
        self.being_hit()
        
        unit_vector = self.move_towards_player(player.pos)

        if self.stunned:
            # stop from moveing and attacking
            if self.time_stunned <= 0:
                self.stunned = False
                self.time_stunned = self.recover_time
            else:
                self.time_stunned -= 1
                self.fire = False
        else:
            self.move(unit_vector)
                
        self.check_boundarys()        
        self.update_weapons(enemy_group)
        self.collisions(player)

    # move towards unit vector
    def move(self, unit_vector):
        self.pos.x += self.speed * unit_vector.x
        self.pos.y += self.speed * unit_vector.y

        
    # run checks to prevent going out of bounds
    def check_boundarys(self):
        # movement restriction (BG_WIDTH and BG_HEIGHT)
        if self.pos.x > BG_WIDTH - self.width/2:
            self.pos.x = BG_WIDTH - self.width/2
            return True
        if self.pos.x < self.width/2:
            self.pos.x = self.width/2
            return True
        if self.pos.y < -BG_HEIGHT + self.height/2:
            self.pos.y = -BG_HEIGHT + self.height/2
            return True
        if self.pos.y > -self.height/2:
            self.pos.y = -self.height/2
            return True
        
        return False
        
    # define basic collision_detect override for projectiles aswell (only does touch)
    def collisions(self, player):
        if pygame.Rect.colliderect(self.hitbox_rect, player.rect):
            player.take_damage(self.attack(), self.target_unit_vector, self.knockback)

    # define update weapons
    def update_weapons(self, enemy_group):
        for weapon in self.weapons:
            weapon.update(self.front, self.target_unit_vector, self.pos, enemy_group, self.fire, (self.projectile_speed, self.damage, self.attack_rate, self.knockback))

    # draw weapons
    def draw_weapons(self, screen, bg_pos):
        for weapon in self.weapons:
            weapon.draw(screen, bg_pos)

        

    

