import pygame
from sprites.weapons.Guns.Gun import Gun
from sprites.projectiles.NodeBullet import NodeBullet
from classes.Direction import Direction
from config import *

class NodeBlaster(Gun):
    def __init__(self, pos, cam_offset):
        super().__init__(pos, cam_offset, "assets/weapons/NodeBlaster.png", (40, 40))

        # bullets
        self.projectiles = pygame.sprite.Group()
        self.gun_damage_mod = 2
        self.bullet_speed_mod = 0.8
        self.fire_rate_mod = 0.2
        self.knockback_mod = 0

        self.offset = 20

        self.bullet_type = NodeBullet

    # face target overide, as this is an enemy weapon
    def face_target(self, target_dir):
        # copy target direction
        self.front.dir = target_dir.dir

        # move image
        self.image = Direction.rotate(self.front.dir, self.base_image)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)