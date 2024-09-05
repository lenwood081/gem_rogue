import pygame
import random
import math
from utility.Point import Point
from utility.Direction import Direction
from drops.Experiance import Experiance
from sprites.ItemHolder import ItemHolder
from Actions.CollideAttack import CollideAttack
from config import *

# TODO impliment knoockbacl with target unnit vector and strength

class Enemy(ItemHolder):
    def __init__(self, pos, animimations, size, experiance_group, projectile_group, enemy_group, particle_group, cam_offset):
        super(Enemy, self).__init__()
        # ---------------------- ITEM HOLDER ATTRIBUTES -------------------

        # dimensions
        self.width = self.max_width = size[0]
        self.height = self.max_height = size[1]

        # immunity frames
        self.immunity_frames_gained = 0 / FRAMERATE

        # -----------------------------------------------------------------

        self.pos = pos.copy() 
        self.move_animation = animimations[0]
        self.hurt_animation = animimations[1]

        # base image
        self.image = self.move_animation.animate(self.dt)
        self.image_base = self.image
        self.hitbox_rect = self.image_base.get_rect()
        self.boundary_rect = self.hitbox_rect.copy()
        self.rect = self.hitbox_rect.copy()

        # direction and turning
        self.dist_player = 0
        self.turn_pixels = 6
        self.VARIATION = 60
        self.target_variation = random.uniform(-self.VARIATION, self.VARIATION)
        self.lock_on_dist = 300
    
        # drops
        self.experiance_group = experiance_group
        self.projectile_group = projectile_group
        self.particle_group = particle_group

        self.cam_offset = cam_offset
        self.enemy_group = enemy_group
        self.enemy = None
        # select an enemy to target (always last)
        for enemy in enemy_group:
            self.enemy = enemy

        # add collidattack action
        self.actions.append(CollideAttack(0.5, 1, self, enemy))

     # draw method
    def draw(self, screen):
        screen.blit(self.image, self.rect) 
        
        for action in self.actions:
            action.draw(screen)

        # debugging
        #pygame.draw.rect(screen, "red", self.hitbox_rect, width=2)
        #pygame.draw.rect(screen, "blue", self.rect, width=2)

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
 
    
    # check for being hit
    def being_hit(self):
        # also controlls animations
        if self.being_hurt:
            self.time_refresh_currect -= 1 * self.dt
            self.image_base = self.hurt_animation.animate(self.dt) 
        else:
            # general move animation
            self.image_base = self.move_animation.animate(self.dt)

        if self.time_refresh_currect <= 0:
            self.being_hurt = False
            

    # update method (general) can be overriden
    def update(self, player, cam_offset, boundary, dt):
        self.velocity = Point(0, 0)

        self.update_with_dt(dt)
        self.cam_offset = cam_offset

        self.being_hit()
        self.move_towards_player(player.pos)
        if self.stunned:
            # stop from moveing and attacking
            self.velocity = Point(0, 0)
            if self.time_stunned <= 0:
                self.stunned = False
                self.time_stunned = self.recover_time
                self.can_attack = True
            else:
                self.time_stunned -= 1 * dt
                self.can_attack = False

        # actions
        for action in self.actions:
                # for basic self activated actions such as CollideAttack
                action.use(dt)
                action.update(dt)
        
        
        if self.move_normal:
            self.move(self.target_unit_vector)

        # known error where moveing side ways causes an error 
        self.boundary_collision(boundary, self.pos.x + cam_offset.x, -self.pos.y + cam_offset.y)

        self.hitbox_rect.center = (self.pos.x + cam_offset.x, -self.pos.y + cam_offset.y)
        self.rect.center = self.hitbox_rect.center

    # update velocity towards unit vector
    def move(self, unit_vector):
        self.velocity.x = self.speed * unit_vector.x * self.dt
        self.velocity.y = self.speed * unit_vector.y * self.dt

        
    # run checks to prevent going out of bounds 
    def check_boundarys(self, boundary, cam_offset):
        # check against tiles
        ret_val = False
        for tile in boundary:   
            self.boundary_rect.center = (self.pos.x + cam_offset.x, -self.pos.y + cam_offset.y)
            if pygame.Rect.colliderect(self.boundary_rect, tile.rect):
                # check x
                self.boundary_rect.center = (self.pos.x + cam_offset.x, -self.pos.y + cam_offset.y + self.velocity.y)
                if pygame.Rect.colliderect(self.boundary_rect, tile.rect):
                    # left hand edge
                    if self.velocity.x > 0:
                        self.pos.x = tile.pos.x - self.width/2
                    # right hand side
                    elif self.velocity.x < 0:
                        self.pos.x = tile.pos.x + tile.width + self.width/2

                # check y
                self.boundary_rect.center = (self.pos.x + cam_offset.x - self.velocity.x, -self.pos.y + cam_offset.y)
                if pygame.Rect.colliderect(self.boundary_rect, tile.rect):
                    # top
                    if self.velocity.y > 0:
                        self.pos.y = tile.pos.y - tile.height - self.height/2
                    # bottom
                    elif self.velocity.y < 0:
                        self.pos.y = tile.pos.y + self.height/2
                
                # movement restricted =>
                ret_val = True
        
        return ret_val
        

    

