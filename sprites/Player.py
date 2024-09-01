import pygame
from config import *
from classes.Point import Point
from classes.Direction import Direction
from classes.Glow import Glow
from sprites.weapons.Guns.BasicGun import BasicGun
from sprites.weapons.Guns.PlasmaGun import PlasmaGun
from Animations.Animation import Animation
from sprites.ItemHolder import ItemHolder
from Actions.Dash import Dash
from Actions.WeaponFire import WeaponFire 
from drops.Items.Passive.Quads import Quads
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
    def __init__(self, projectile_group):
        super(Player, self).__init__()
        # ---------------------- ITEM HOLDER ATTRIBUTES -------------------

        # health
        self.health = self.max_health = 10

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
        self.image = self.base_animate.animate()
        self.base_image = self.image
        self.hitbox_rect = self.base_image.get_rect(center=(
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT/2,
        ))
        self.boundary_rect = self.hitbox_rect.copy()
        self.rect = self.hitbox_rect.copy()
        # glow
        self.radius = self.width * 0.5
        self.glow_rate = 0.5
        self.num_glows = 5
        self.max_diff = 10
        self.current = 0
        self.increasing = 30 / FRAMERATE

        # position reletive to background (centered)
        # start in the center of the playable area
        self.pos = Point(BG_WIDTH/2 + self.width/2, -BG_HEIGHT/2 - self.height/2)

        # position to the center of the screen
        self.pos_screen = Point(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

        # used to update weapons and projectiles
        self.cam_offset = Point(0, 0)

        # drops
        self.collect_range = 100
        self.exp = 0
        self.exp_to_level = 10

        # projectile group
        self.projectile_group = projectile_group

        # enemy_group
        self.enemy_group = None

        # actions
        self.action_key_array = []
        self.actions.append(Dash(2, 3, self))
        self.action_key_array.append(KMOD_LSHIFT)
        self.actions.append(WeaponFire(1, "Plasma Gun", self, PlasmaGun, math.pi/8))
        self.action_key_array.append(MOUSE1)
        self.actions.append(WeaponFire(1, "Plasma Gun", self, PlasmaGun, -math.pi/8))
        self.action_key_array.append(MOUSE1)
        self.actions.append(WeaponFire(1, "Plasma Gun", self, PlasmaGun, -math.pi/3))
        self.action_key_array.append(MOUSE1)
        self.actions.append(WeaponFire(1, "Plasma Gun", self, PlasmaGun, math.pi/3))
        self.action_key_array.append(MOUSE1)
        
        

    # ---------------------------------------- for bliting and collision detect ------------------

    # blit player and weapon
    def draw(self, screen):
        # glow breath
        radius = self.radius * (self.num_glows*2) + self.current
        if self.current >= self.max_diff:
            self.increasing = -30 / FRAMERATE
        elif self.current <= self.max_diff * -1:
            self.increasing = 30 / FRAMERATE
        self.current += self.increasing * self.glow_rate

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

    def boundary_collision(self, collision_group):
        # maximum change in velocity (if greater than this then use increments)
        dist = 64*SCALE_FACOTOR
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

                self.boundary_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - vel_y)
                if pygame.Rect.colliderect(self.boundary_rect, tile.rect):
                    # top
                    if vel_y > 0:
                        self.pos.y = tile.pos.y - tile.height - self.height/2
                    # bottom
                    elif vel_y < 0:
                        self.pos.y = tile.pos.y + self.height/2
                    y_safe = False
                    break

            # check x
            for x_i in range(x):
                vel_x = dist * math.copysign(1, self.velocity.x) * (x_i)

                # for last one
                if x_i == x-1:
                    vel_x = self.velocity.x

                self.boundary_rect.center = (SCREEN_WIDTH/2 + vel_x, SCREEN_HEIGHT/2)
                if pygame.Rect.colliderect(self.boundary_rect, tile.rect):
                    # left hand edge
                    if vel_x > 0:
                        self.pos.x = tile.pos.x - self.width/2
                    # right hand side
                    elif vel_x < 0:
                        self.pos.x = tile.pos.x + tile.width + self.width/2 
                    x_safe = False
                    break

        if x_safe:
            self.pos.move(self.velocity.x, 0)
        
        if y_safe:
            self.pos.move(0, self.velocity.y)


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
    def update(self, keys_pressed, mouse_pressed, boundary):
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
                action.use()
        
        if self.move_normal:
            x = 0
            y = 0

            # player movement
            if keys_pressed[K_s]:
                y = -self.speed
            if keys_pressed[K_w]:
                y = self.speed
            if keys_pressed[K_d]:
                x = self.speed
            if keys_pressed[K_a]:
                x = -self.speed

            # check for diagonal speed irregularity
            if x != 0 and y != 0:
                x /= math.sqrt(2)
                y /= math.sqrt(2)
            self.velocity = Point(x, y)

        self.boundary_collision(boundary)

        # animation
        self.base_image = self.base_animate.animate()

        #self.face_mouse()
        self.flip_mouse()

    # secound update for things that require background pos to be updated
    def update_after_camera(self, cam_offset, enemy_group):
        if self.immunity_frames > 0:
            self.immunity_frames -= 1
            if self.immunity_frames <= 0:
                print("not immune")
                self.immune = False

        # updates store of cam_offset
        self.cam_offset = cam_offset

        self.enemy_group = enemy_group

        # weapon update
        for action in self.actions:
            action.update()
        
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




