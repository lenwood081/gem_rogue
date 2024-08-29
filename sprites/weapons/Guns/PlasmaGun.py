import pygame
from config import *
from sprites.weapons.Guns.Gun import Gun
from sprites.projectiles.GlowBullet import GlowBullet
from Animations.Animation import Animation

# TODO make plasma bullets hit bigger (normal need to be made to only hit once)
class PlasmaGun(Gun):
    def __init__(self, pos, cam_offset):
        fire_animation = Animation(["assets/weapons/PlasmaGun3.png", "assets/weapons/PlasmaGun2.png"], (28*SCALE_FACOTOR, 16*SCALE_FACOTOR), [0.05, 0.1])
        idle_animation = Animation(["assets/weapons/PlasmaGun1.png"], (28*SCALE_FACOTOR, 16*SCALE_FACOTOR), [1])
        muzzle_flash = Animation(["assets/weapons/PlasmaFlash.png"], (16*SCALE_FACOTOR, 16*SCALE_FACOTOR), [1])

        super(PlasmaGun, self).__init__(pos, cam_offset, idle_animation, fire_animation, muzzle_flash, (28*SCALE_FACOTOR, 16*SCALE_FACOTOR)) 

        # white bullets
        self.projectiles = pygame.sprite.Group()
        self.gun_damage_mod = 2
        self.bullet_speed_mod = 2
        self.fire_rate_mod = 1.2
        self.knockback_mod = 0

        # offeset from player (for basic gun this is zero due to the way it is drawn)
        self.offset =64

        self.bullet_type = GlowBullet
                
