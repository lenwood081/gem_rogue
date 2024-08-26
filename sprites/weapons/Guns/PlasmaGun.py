import pygame
from config import *
from sprites.weapons.Guns.Gun import Gun
from sprites.projectiles.GlowBullet import GlowBullet

# TODO make plasma bullets hit bigger (normal need to be made to only hit once)
class PlasmaGun(Gun):
    def __init__(self, pos, bg_pos):
        super(PlasmaGun, self).__init__(pos, bg_pos, "assets/weapons/PlasmaGun.png", (32, 20)) 

        # white bullets
        self.projectiles = pygame.sprite.Group()
        self.gun_damage_mod = 2
        self.bullet_speed_mod = 1
        self.fire_rate_mod = 1.2
        self.knockback_mod = 0

        # offeset from player (for basic gun this is zero due to the way it is drawn)
        self.offset = max(PL_WIDTH, PL_HEIGHT)

    # shoots a bullet
    def shoot(self, player_dir, target_unit_vector, fire, attributes):
        if self.can_attack(): 
            if self.do_attack(fire):
                new_projectile = GlowBullet(self.pos, target_unit_vector, player_dir, attributes)
                self.projectiles.add(new_projectile)
                
