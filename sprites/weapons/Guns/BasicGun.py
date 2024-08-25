import pygame
from config import *
from sprites.weapons.Guns.Gun import Gun
from sprites.projectiles.WhiteBullet import WhiteBullet


class BasicGun(Gun):
    def __init__(self, pos, bg_pos):
        super(BasicGun, self).__init__(pos, bg_pos, "assets/weapons/Basic_gun.png", (32, 32)) 

        # white bullets
        self.projectiles = pygame.sprite.Group()
        self.gun_damage_mod = 1
        self.bullet_speed = 20
        self.fire_rate = 5

        # offset
        self.offset = max(PL_WIDTH, PL_HEIGHT)

    # shoots a bullet
    def shoot(self, player_dir, target_unit_vector, fire):
        if self.can_attack(): 
            if self.do_attack(fire):
                new_projectile = WhiteBullet(self.pos, target_unit_vector, player_dir, self.bullet_speed)
                self.projectiles.add(new_projectile)
                
