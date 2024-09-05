import pygame
from config import *
from utility.Point import Point
from utility.Direction import Direction
import math

# when using values from here remember for time realted ones to divide by framrate!!!
# class that is inherited for sprites that require items, dfines basic stats

class ItemHolder(pygame.sprite.Sprite):
    def __init__(self):
        super(ItemHolder, self).__init__()

        self.dt = 1

        # items!
        self.items = []
        self.current_id = 0
        self.particle_group = None

        # width and height
        self.width = self.max_width = 23
        self.height = self.max_height = 23

        # health and armour
        self.health = self.max_health = 10
        self.level_health_bonus = 1.3
        self.armour = self.max_armour = 0
        self.sheild = self.max_sheild = 0
        self.weight = self.max_weight = 1

        # hurt image time and display
        self.being_hurt = False
        self.time_refresh_currect = self.time_refresh = 0.2 * FRAMERATE
        self.time_refresh_currect = 0

        # hit handeling
        self.immune = False
        self.immunity_frames = 0
        self.immunity_frames_gained = 0.5 * FRAMERATE
        self.stunned = False
        self.time_stunned = self.recover_time = 0.3 * FRAMERATE

        # speed
        self.speed = self.max_speed = 180 / FRAMERATE
        self.velocity = Point(0, 0)
        self.target_unit_vector = Point(0, 0)
        self.front = Direction(0)
        self.move_normal = True
        self.projectile_group = None

        # attacking
        self.damage = self.max_damage = 1
        self.level_damage_bonus = 1.2
        self.knockback = self.max_knockback = 0
        self.attack_rate = self.max_attack_rate = 3
        self.projectile_speed = self.max_projectile_speed = 800 / FRAMERATE
        self.can_attack = False

        # -----------------------------------------------------------------------------------------------
        # different enemies and players have different attacks,
        # weapon attacking is handled by fire rate
        # other attacks need cooldowns
        # an exmaple is basic enemy touching damage

        self.actions = []

        # -----------------------------------------------------------------------------------------------

        # level
        self.level = 0

        # drops
        self.exp = 1

        # for the ablitlity to ignore walls
        self.trans = False

    def level_up(self):
        self.level += 1
        # increase max/base stats

        # health
        self.max_health *= self.level_health_bonus

        # damage
        self.max_damage *= self.level_damage_bonus

        # exp drops

        # reset health
        self.health = self.max_health
        self.damage = self.max_damage
    
    # for setting level, if used more than once on a player/enemy it will end up being much higher then expected
    def set_level(self, level):
        self.level = level
        # increase max/base stats

        # health
        self.max_health *= self.level_health_bonus**self.level

        # damage
        self.max_damage *= self.level_damage_bonus**self.level

        # exp drops
        
        # reset health and damage
        self.health = self.max_health
        self.damage = self.max_damage
        

    # ------------------------------ General functions ----------------------------

    # for taking damage
    def take_damage(self, damage, unit_vector, knockback):
        if self.immune:
            return

        # calculate knockback, and if stunned
        knockback_dist = 0
        if knockback >= self.weight:
            self.stunned = True
            knockback_dist = knockback * 10 / self.weight 

        # preform knockback
        if knockback_dist > 0:
            self.pos.x += unit_vector.x * knockback_dist * self.dt
            self.pos.y += unit_vector.y * knockback_dist * self.dt

        # armour at 10 = %50, at 20 = %66.66 at 30 = %75 damage deflected (tenno armour calculation)
        self.health -= damage - damage*(self.armour/(self.armour + 10))

        # for being_hurt
        self.being_hurt = True
        self.time_refresh_currect = self.time_refresh

        if self.health <= 0:
            self.death()
            return
        
        # damage immunity frame?
        if self.immunity_frames_gained == 0:
            return
        
        self.immune = True
        self.immunity_frames = self.immunity_frames_gained

    # increase speed 
    def set_speed(self, percentage):
        self.speed = self.max_speed * (1 + percentage)

    # for Items
    def pickup_item(self, itemType):
        item = itemType(self.current_id)
        item.connect(self)
        self.current_id += 1
        self.items.append(item)

    # lose Item
    def lose_item(self, id):
        item_index = self.items.index(id)
        self.items[item_index].remove(self)
        self.items.pop(item_index)

    
    # for delta time
    def update_with_dt(self, dt):
        self.dt = dt

    # collision detection

    def boundary_collision(self, collision_group, x_bound_point, y_bound_point):
        if self.trans:
            self.pos.move(self.velocity.x, self.velocity.y)
            return False

        # maximum change in velocity (if greater than this then use increments)
        dist = 32*SCALE_FACOTOR
        x_safe = y_safe = True

        # call on self TODO update other collision detection on projectiles and enemys
        for tile in collision_group:
            x = (int)(math.fabs(self.velocity.x // dist) + 1)
            y = (int)(math.fabs(self.velocity.y // dist) + 1)

            # check y
            for y_i in range(y):
                vel_y = dist * math.copysign(1, self.velocity.y) * (y_i)

                # for last one
                if y_i == y-1:
                    vel_y = self.velocity.y

                self.boundary_rect.center = (x_bound_point, y_bound_point - vel_y)
                if pygame.Rect.colliderect(self.boundary_rect, tile.rect):
                    # top
                    if vel_y > 0:
                        self.velocity.y = self.pos.y - (tile.pos.y - tile.height - self.height/2)
                        self.pos.y = tile.pos.y - tile.height - self.height/2
                    # bottom
                    elif vel_y < 0:
                        self.velocity.y = self.pos.y - (tile.pos.y + self.height/2)
                        self.pos.y = tile.pos.y + self.height/2

                    y_safe = False
                    break

            # check x
            for x_i in range(x):
                vel_x = dist * math.copysign(1, self.velocity.x) * (x_i)

                # for last one
                if x_i == x-1:
                    vel_x = self.velocity.x

                self.boundary_rect.center = (x_bound_point + vel_x, y_bound_point)
                if pygame.Rect.colliderect(self.boundary_rect, tile.rect):
                    # left hand edge
                    if vel_x > 0:
                        self.velocity.x = self.pos.x - (tile.pos.x - self.width/2)
                        self.pos.x = tile.pos.x - self.width/2
                    # right hand side
                    elif vel_x < 0:
                        self.velocity.x = self.pos.x - (tile.pos.x + tile.width + self.width/2 )
                        self.pos.x = tile.pos.x + tile.width + self.width/2 
                    x_safe = False
                    break

        if x_safe:
            self.pos.move(self.velocity.x, 0)
        
        if y_safe:
            self.pos.move(0, self.velocity.y)

        return ((y_safe and x_safe) == False)



        




