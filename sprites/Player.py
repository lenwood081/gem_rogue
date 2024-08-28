import pygame
from config import *
from classes.Point import Point
from classes.Direction import Direction
from classes.Glow import Glow
from sprites.weapons.Guns.BasicGun import BasicGun
from sprites.weapons.Guns.PlasmaGun import PlasmaGun
from Animations.Animation import Animation
from sprites.ItemHolder import ItemHolder
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
    K_e,
)
import math

MOUSE = 'mouse1'

# TODO link weapon and projectile damage to player damage

class Player(ItemHolder):
    def __init__(self, cam_offset):
        super(Player, self).__init__()
        # ---------------------- ITEM HOLDER ATTRIBUTES -------------------

        # health
        self.health = self.max_health = 10

        # dimensions
        self.width = self.max_width = PL_WIDTH
        self.height = self.max_height = PL_HEIGHT

        # speed
        self.speed = self.max_speed = 10

        # level
        self.level = 0

        # attacking
        self.damage = self.max_damage = 1
        self.knockback = self.max_knockback = 1
        self.attack_rate = self.max_attack_rate = 3
        self.projectile_speed = self.max_projectile_speed = 20

        # -----------------------------------------------------------------

        # base image
        self.base_animate = Animation(["assets/player/Player_concept1_walk1.png", "assets/player/Player_concept1_walk2.png"], (self.width, self.height), [0.3, 0.3])
        self.image = self.base_animate.animate()
        self.base_image = self.image
        self.hitbox_rect = self.base_image.get_rect(center=(
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT/2,
        ))
        self.rect = self.hitbox_rect.copy()

        # glow
        self.radius = PL_WIDTH * 0.8
        self.glow_rate = 0.5
        self.num_glows = 5
        self.max_diff = 10
        self.current = 0
        self.increasing = 1

        # position reletive to background (centered)
        # start in the center of the playable area
        self.pos = Point(BG_WIDTH/2 + PL_WIDTH/2, -BG_HEIGHT/2 - PL_HEIGHT/2)

        # position to the center of the screen
        self.pos_screen = Point(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.cam_offset = cam_offset.copy()
        self.front = Direction(0)
        self.mouse_unit_vector = Point(0, 0)

        # drops
        self.collect_range = 60
        self.exp = 0
        self.exp_to_level = 10

        # weapons
        self.weapon_assit_array = []

        # added Basic gun
        self.add_weapon(BasicGun, MOUSE, 0)
        self.add_weapon(PlasmaGun, MOUSE, -math.pi/2)
        self.add_weapon(BasicGun, MOUSE, math.pi/2)
        


    # blit player and weapon
    def draw(self, screen):
        # glow breath
        radius = self.radius * (self.num_glows*2) + self.current
        if self.current >= self.max_diff:
            self.increasing = -1
        elif self.current <= self.max_diff * -1:
            self.increasing = 1
        self.current += self.increasing * self.glow_rate

        # draw glow
        screen.blit(Glow.circle_image_add(radius), (self.pos_screen.x - radius, self.pos_screen.y - radius), special_flags=pygame.BLEND_RGBA_ADD)

        # draw player
        screen.blit(self.image, self.rect)

        # draw weapon
        self.draw_weapons(screen)

        # debugging
        #pygame.draw.rect(screen, "red", self.hitbox_rect, width=2)
        #pygame.draw.rect(screen, "blue", self.rect, width=2)

    # death method
    def death(self):
        # reset to game screen
        self.kill()

    # rotating player
    def face_mouse(self):
        # find mouse pos
        mx, my = pygame.mouse.get_pos()
        mouse_pos = Point(mx, -my)

        # y must be reversed 
        temp_pos =  Point(self.pos_screen.x, -self.pos_screen.y)
        mouse_dir = Point.direction_to_point(mouse_pos, temp_pos)

        # make unit vector for point to travel to
        self.mouse_unit_vector = Point.unit_vector(mouse_pos, temp_pos)

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
        self.mouse_unit_vector = Point.unit_vector(mouse_pos, temp_pos)

        # flip image if needed
        if mouse_dir.dir < -math.pi/2 or mouse_dir.dir > math.pi/2:
            self.image = self.base_image
        else:
            self.image = pygame.transform.flip(self.base_image, True, False)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)
        self.front = mouse_dir
        
    # update loop
    def update(self, keys_pressed):
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

        self.pos.move(x, y)

        # movement restriction (BG_WIDTH and BG_HEIGHT)
        if self.pos.x > BG_WIDTH - PL_WIDTH/2:
            self.pos.x = BG_WIDTH - PL_WIDTH/2
        if self.pos.x < PL_WIDTH/2:
            self.pos.x = PL_WIDTH/2
        if self.pos.y < -BG_HEIGHT + PL_HEIGHT/2:
            self.pos.y = -BG_HEIGHT + PL_HEIGHT/2
        if self.pos.y > -PL_HEIGHT/2:
            self.pos.y = -PL_HEIGHT/2

        # animation
        self.base_image = self.base_animate.animate()

        #self.face_mouse()
        self.flip_mouse()

    # secound update for things that require background pos to be updated
    def update_after_background(self, keys_pressed, mouse_pressed, cam_offset, enemy_group):
        if self.immune:
            self.immunity_frames -= 1
            if self.immunity_frames == 0:
                self.immune = False

        # updates store of cam_offset
        self.cam_offset = cam_offset

        # weapon update
        self.update_weapons(enemy_group, keys_pressed, mouse_pressed)


# ------------------------ Leveling up -------------------------------

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
        self.exp_to_level = self.exp_to_level * (self.exp_to_level/5)

# ------------------------ For Weapon Code ---------------------------

    # add_weapon
    def add_weapon(self, type, fire_key, angle):
        # add key to correct position
        self.weapon_assit_array.append((fire_key, angle))
        weapon = type(self.pos, self.cam_offset)
        weapon.angle_on_player = angle
        self.weapons.add(weapon)

    # using mouse_pressed and key_pressed as faster and allows for holddown input
    def update_weapons(self, enemy_group, keys_pressed, mouse_pressed):
        for  i, weapon in enumerate(self.weapons):
            fire = False
            if self.weapon_assit_array[i][0] == MOUSE:
                if mouse_pressed[0]:
                    fire = True
            elif keys_pressed[self.weapon_assit_array[i][0]]:
                fire = True
            weapon.update(self.front, self.mouse_unit_vector, self.pos, enemy_group, fire, (self.projectile_speed, self.damage, self.attack_rate, self.knockback))

    # draw weapons
    def draw_weapons(self, screen):
        for weapon in self.weapons:
            weapon.draw(screen, self.cam_offset)

