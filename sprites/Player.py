import pygame
from config import *
from utility.Point import Point
from utility.Direction import Direction
from utility.Glow import Glow
from Animations.Animation import Animation
from sprites.ItemHolder import ItemHolder
from drops.Items.Passive.Quads import Quads
from drops.Items.Equipment.PlasmaGunItem import PlasmaGunItem
from drops.Items.Equipment.DashItem import DashItem
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
    K_e,
    KMOD_LSHIFT,
)
import math

MOUSE1 = 0

# TODO link weapon and projectile damage to player damage

class Player(ItemHolder):
    def __init__(self, projectile_group, particle_group):
        super(Player, self).__init__()
        # ---------------------- ITEM HOLDER ATTRIBUTES -------------------

        # health
        self.health = self.max_health = 100

        # dimensions
        self.width = self.max_width = 32*SCALE_FACOTOR
        self.height = self.max_height = 32*SCALE_FACOTOR

        # speed
        self.speed = self.max_speed = 700 / FRAMERATE

        # level
        self.level = 0

        # attacking
        self.damage = self.max_damage = 1
        self.knockback = self.max_knockback = 1
        self.attack_rate = self.max_attack_rate = 3
        self.projectile_speed = self.max_projectile_speed = 1000 / FRAMERATE

        # immunity_frames
        self.immunity_frames_gained = 0

        # -----------------------------------------------------------------

        # base image
        #self.base_animate = Animation(["assets/player/Player_concept1_walk1.png", "assets/player/Player_concept1_walk2.png"], (self.width, self.height), [0.3, 0.3])
        self.base_animate = Animation(["assets/player/duck_wizard.png"], (32*SCALE_FACOTOR , 32*SCALE_FACOTOR), [0.3])
        self.image = self.base_animate.animate(self.dt)
        self.base_image = self.image
        self.hitbox_rect = self.base_image.get_rect(center=(
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT/2,
        ))
        self.boundary_rect = self.hitbox_rect.copy()
        self.rect = self.hitbox_rect.copy()
        # glow
        self.radius = self.width * 0.5
        self.glow_rate = 30 / FRAMERATE
        self.num_glows = 5
        self.max_diff = 10
        self.current = 0
        self.increasing = 1

        # position to the center of the screen
        self.pos_screen = Point(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

        # used to update weapons and projectiles
        self.cam_offset = Point(0, 0)

        # drops
        self.collect_range = 100
        self.exp = 0
        self.exp_to_level = 10
        
        # groups
        self.projectile_group = projectile_group
        self.particle_group = particle_group
        self.enemy_group = None

        # allows wall going through
        self.trans = False 

        # actions
        self.angle = 0
        self.action_key_array = []
        
        # action keys (order is inside then outside positive to negative)
        self.action_key_array.append(MOUSE1) # pos2
        self.action_key_array.append(MOUSE1) # pos1
        self.action_key_array.append(MOUSE1) # pos3
        self.action_key_array.append(KMOD_LSHIFT) # pos4

        # add active items
        self.active_item_cap = 4
        self.pickup_item(PlasmaGunItem) 
        self.pickup_item(PlasmaGunItem) 
        self.pickup_item(PlasmaGunItem) 
        self.pickup_item(DashItem) 

        self.pickup_item(Quads)
        self.pickup_item(Quads)
        self.pickup_item(Quads)
        self.pickup_item(Quads)
        self.pickup_item(Quads)
        
        

    # ---------------------------------------- for bliting and collision detect ------------------

    # blit player and weapon
    def draw(self, screen):
        # glow breath
        radius = self.radius * (self.num_glows*2) + self.current
        if self.current >= self.max_diff:
            self.increasing = -1
        elif self.current <= -self.max_diff:
            self.increasing = 1
        self.current += self.increasing * self.glow_rate * self.dt

        # draw glow
        screen.blit(Glow.circle_image_add(radius), (self.pos_screen.x - radius, self.pos_screen.y - radius), special_flags=pygame.BLEND_RGBA_ADD)

        # draw player
        screen.blit(self.image, self.rect)

        # draw actions
        for action in self.actions:
            action.draw(screen)

        # debugging
        #pygame.draw.rect(screen, "red", self.hitbox_rect, width=2)
        #pygame.draw.rect(screen, "blue", self.rect, width=2)

    # ------------------------------------------ facing mouse --------------------------------

    # rotating player
    def face_mouse(self):
        # find mouse pos
        mx, my = pygame.mouse.get_pos()
        mouse_pos = Point(mx, -my)

        # y must be reversed 
        temp_pos =  Point(self.pos_screen.x, -self.pos_screen.y)
        mouse_dir = Point.direction_to_point(mouse_pos, temp_pos)

        # make unit vector for point to travel to
        self.target_unit_vector = Point.unit_vector(mouse_pos, temp_pos)

        # rotate image
        self.image = Direction.rotate_with_flip(mouse_dir.dir, self.base_image)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)
        self.front = mouse_dir

    # rotating player method #2
    def flip_mouse(self):
        # find mouse pos
        mx, my = pygame.mouse.get_pos()
        mouse_pos = Point(mx, -my)

        # y must be reversed 
        temp_pos =  Point(self.pos_screen.x, -self.pos_screen.y)
        mouse_dir = Point.direction_to_point(mouse_pos, temp_pos)

        # make unit vector for point to travel to
        self.target_unit_vector = Point.unit_vector(mouse_pos, temp_pos)

        # flip image if needed
        if mouse_dir.dir < -math.pi/2 or mouse_dir.dir > math.pi/2:
            self.image = self.base_image
        else:
            self.image = pygame.transform.flip(self.base_image, True, False)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)
        self.front = mouse_dir

    # ---------------------------------------- updates --------------------------------------------
        
    # update loop
    def update(self, keys_pressed, mouse_pressed, boundary, activators, dt):
        # check trans
        if keys_pressed[pygame.K_t]:
            self.trans = (self.trans == False)

        self.update_with_dt(dt)

        self.move_normal = True
        self.can_attack = True

        # check actions
        for i, action in enumerate(self.actions):
            # check for movement restrictions
            if action.move_normal == False:
                self.move_normal = False

            # check for firing restrictions
            if action.fire_normal == False:
                self.can_attack = False
        
            if (keys_pressed[self.action_key_array[i]] or (pygame.key.get_mods() & self.action_key_array[i]) or mouse_pressed[self.action_key_array[i]]) and action.already_active() == False:
                action.use(dt)
        
        if self.move_normal:
            x = 0
            y = 0

            # player movement
            if keys_pressed[K_s]:
                y = -self.speed * dt
            if keys_pressed[K_w]:
                y = self.speed * dt
            if keys_pressed[K_d]:
                x = self.speed * dt
            if keys_pressed[K_a]:
                x = -self.speed * dt

            # check for diagonal speed irregularity
            if x != 0 and y != 0:
                x /= math.sqrt(2)
                y /= math.sqrt(2)

            # add drag when stoping
            # if not x and not y:
            #     if self.velocity.x**2 > 9 or self.velocity.y**2 > 9:
            #         x = self.velocity.x*0.5*dt
            #         y = self.velocity.y*0.5*dt
            self.velocity = Point(x, y)

        self.boundary_collision(boundary, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

        # activators
        self.special_collision(activators, keys_pressed)

        # animation
        self.base_image = self.base_animate.animate(dt)

        #self.face_mouse()
        self.flip_mouse()

    # secound update for things that require background pos to be updated
    def update_after_camera(self, cam_offset, enemy_group):
        if self.immunity_frames > 0:
            self.immunity_frames -= 1 * self.dt
            if self.immunity_frames <= 0:
                self.immune = False

        # updates store of cam_offset
        self.cam_offset = cam_offset

        self.enemy_group = enemy_group

        # weapon update
        for action in self.actions:
            action.update(self.dt)
        
# ------------------------ Leveling up -------------------------------

    # death method
    def death(self):
        # reset to game screen
        self.kill()

    # for adding exp
    def add_exp(self, exp):
        self.exp += exp

        if self.exp >= self.exp_to_level:
            self.exp -= self.exp_to_level
            self.level_up_player()

    # leveling up
    def level_up_player(self):

        self.level_up()
        # eponentual
        self.exp_to_level *= 2 

# -------------------------------- Action skills -----------------------------------------------

    # for determining the angle to place the next skill (should change for weapons and utility)
    def personalise_angles(self, action_subset, rotation):
        # check not full
        if len(self.actions) == 4:
            pass
            # determine which to switch out

        # check which angles 0 -> math.pi/8, -math.pi/8 -> 0, math.pi/6, -math.pi/6 ->  math.pi/8, -math.pi/8, -math.pi/3, math.pi/3
        odd_or_even = 0
        if len(action_subset) % 2 == 0:
            # even
            odd_or_even = 1


        # change angles
        curr_angle = odd_or_even * 1/10
        past = 0

        for i in range(len(action_subset)):
            action_subset[past].change_angle(math.pi*curr_angle+rotation)
            past += 1
            if curr_angle != 0:
                curr_angle *= -1
                action_subset[past].change_angle(math.pi*curr_angle+rotation)
                past += 1
                curr_angle *= -1
            else:
                curr_angle = 1/8

            if past == len(action_subset):
                break
            curr_angle *= 2 + odd_or_even * 1

    def determine_angles(self):
        weapons = [action for action in self.actions if action.class_name == "Weapon"]
        utility = [action for action in self.actions if action.class_name == "Utility"]
        self.personalise_angles(weapons, 0)
        self.personalise_angles(utility, math.pi)

    # set position
    def set_position(self, pos):
        self.pos = pos.copy()


