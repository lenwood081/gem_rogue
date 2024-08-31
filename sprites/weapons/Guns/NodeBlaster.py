import pygame
import math
from sprites.weapons.Guns.Gun import Gun
from sprites.projectiles.NodeBullet import NodeBullet
from classes.Direction import Direction
from Animations.Animation import Animation
from config import *

class NodeBlaster(Gun):
    def __init__(self, pos, cam_offset, projectile_group):
        fire_animation = Animation(["assets/weapons/NodeBlaster2.png", "assets/weapons/NodeBlaster3.png"], (16*SCALE_FACOTOR, 32*SCALE_FACOTOR), [0.05, 0.1])
        idle_animation = Animation(["assets/weapons/NodeBlaster1.png"], (16*SCALE_FACOTOR, 32*SCALE_FACOTOR), [1])
        muzzle_flash = Animation(["assets/weapons/PlasmaFlash.png"], (10*SCALE_FACOTOR, 16*SCALE_FACOTOR), [1])

        super().__init__(pos, cam_offset, idle_animation, fire_animation, muzzle_flash, (32*SCALE_FACOTOR, 32*SCALE_FACOTOR), projectile_group)

        # bullets
        self.gun_damage_mod = 1
        self.bullet_speed_mod = 1.2
        self.fire_rate_mod = 0.6
        self.knockback_mod = 0

        self.offset = 18 * SCALE_FACOTOR
        self.flash_offset = self.height/2 - 20

        self.bullet_type = NodeBullet

    # face target overide, as this is an enemy weapon
    def face_target(self, target_dir):
        # copy target direction
        self.front.dir = target_dir.dir - math.pi/2

        # move image
        self.base_image = self.animation_control()
        self.image = Direction.rotate(self.front.dir, self.base_image)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)