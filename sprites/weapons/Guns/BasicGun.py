import pygame
from classes.Point import Point
from config import *
from sprites.weapons.Guns.Gun import Gun
from sprites.projectiles.WhiteBullet import WhiteBullet


class BasicGun(Gun):
    def __init__(self, pos, bg_pos):
        super(BasicGun, self).__init__(pos, bg_pos, "assets/weapons/Basic_gun.png", (24, 24)) 

        # white bullets
        self.projectiles = pygame.sprite.Group()
        self.gun_damage_mod = 1
        self.bullet_speed_mod = 1.7
        self.fire_rate_mod = 1.5
        self.knockback_mod = 2

        # offset
        self.offset = max(PL_WIDTH, PL_HEIGHT) - 10

        # bulletType
        self.bullet_type = WhiteBullet

   
