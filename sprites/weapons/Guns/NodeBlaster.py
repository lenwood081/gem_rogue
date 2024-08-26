import pygame
from sprites.weapons.Guns.Gun import Gun
from sprites.projectiles.NodeBullet import NodeBullet
from classes.Direction import Direction
from config import *

class NodeBlaster(Gun):
    def __init__(self, pos, bg_pos):
        super().__init__(pos, bg_pos, "assets/weapons/NodeBlaster.png", (40, 40))

        # bullets
        self.projectiles = pygame.sprite.Group()
        self.gun_damage_mod = 2
        self.bullet_speed_mod = 0.8
        self.fire_rate_mod = 0.2
        self.knockback_mod = 0

        self.offset = 20

    # shoots a bullet
    def shoot(self, player_dir, target_unit_vector, fire, attributes):
        if self.can_attack(): 
            if self.do_attack(fire):
                new_projectile = NodeBullet(self.pos, target_unit_vector, player_dir, attributes)
                self.projectiles.add(new_projectile)

    # face target overide
    def face_target(self, target_dir):
        # copy target direction
        self.front.dir = target_dir.dir

        # move image
        self.image = Direction.rotate(self.front.dir, self.base_image)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)