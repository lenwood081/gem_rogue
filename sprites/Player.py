import pygame
from config import *
from classes.Point import Point
from classes.Direction import Direction
from classes.Glow import Glow
from sprites.weapons.BasicGun import BasicGun
from sprites.weapons.PlasmaGun import PlasmaGun
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
    K_e,
)
import math

MOUSE = 'mouse1'

class Player(pygame.sprite.Sprite):
    def __init__(self, bg_pos):
        super(Player, self).__init__()
        # base image
        self.base_image = pygame.transform.scale(pygame.image.load("assets/player/Player_concept1.png").convert_alpha(), (PL_WIDTH, PL_HEIGHT))
        self.image = self.base_image
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
        self.pos = Point(BG_WIDTH/2 + PL_WIDTH/2, -BG_HEIGHT/2 - PL_HEIGHT/2)
        self.pos_screen = Point(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.bg_pos = bg_pos.copy()
        self.front = Direction(0)
        self.mouse_unit_vector = Point(0, 0)

        # health and armour
        self.max_health = 10
        self.current_health = self.max_health
        self.armour = 0
        self.immune = False
        self.immunity_frames = 0
        self.immunity_frames_gained = 15
        self.sheild = 0

        # drops
        self.collect_range = 60

        # weapons
        self.weapons = pygame.sprite.Group()
        self.weapon_assit_array = []

        # added Basic gun
        self.add_BasicGun(MOUSE, 0)
        self.add_PlasmaGun(K_e, math.pi/5)



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

    # death method
    def death(self):
        # reset to game screen
        self.kill()

    # for taking damage
    def take_damage(self, damage):
        if self.immune:  
            return

        self.current_health -= damage - damage*(self.armour * 0.01)
        if self.current_health <= 0:
            self.death()
            return
        
        # damage immunity frame?
        self.immune = True
        self.immunity_frames = self.immunity_frames_gained

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
        self.image = Direction.rotate_with_flip(mouse_dir.dir, self.base_image)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)
        self.front = mouse_dir
        
    # update loop
    def update(self, keys_pressed):
        if self.immune:
            self.immunity_frames -= 1
            if self.immunity_frames == 0:
                self.immune = False

        x = 0
        y = 0

        # player movement
        if keys_pressed[K_s]:
            y = -PL_SPEED
        if keys_pressed[K_w]:
            y = PL_SPEED
        if keys_pressed[K_d]:
            x = PL_SPEED
        if keys_pressed[K_a]:
            x = -PL_SPEED

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

        self.face_mouse()

    # secound update for things that require background pos to be updated
    def update_after_background(self, keys_pressed, mouse_pressed, bg_pos, enemy_group):
        # updates store of bg.location
        self.bg_pos = bg_pos.copy()

        # weapon update
        self.update_weapons(enemy_group, keys_pressed, mouse_pressed)


        
# ------------------------ For Weapon Code ---------------------------
    # add basic gun
    def add_BasicGun(self, fire_key, angle):
        # add key to correct position
        self.weapon_assit_array.append((fire_key, angle))
        gun = BasicGun(self.pos, self.bg_pos)
        gun.angle_on_player = angle
        self.weapons.add(gun)

    # add plasma gun
    def add_PlasmaGun(self, fire_key, angle):
        # add key to correct position
        self.weapon_assit_array.append((fire_key, angle))
        gun = PlasmaGun(self.pos, self.bg_pos)
        gun.angle_on_player = angle
        self.weapons.add(gun)

    # using mouse_pressed and key_pressed as faster and allows for holddown input
    def update_weapons(self, enemy_group, keys_pressed, mouse_pressed):
        for  i, weapon in enumerate(self.weapons):
            fire = False
            if self.weapon_assit_array[i][0] == MOUSE:
                if mouse_pressed[0]:
                    fire = True
            elif keys_pressed[self.weapon_assit_array[i][0]]:
                fire = True
            weapon.update(self.front, self.mouse_unit_vector, self.pos, enemy_group, fire)

    def draw_weapons(self, screen):
        for weapon in self.weapons:
            weapon.draw(screen, self.bg_pos)

