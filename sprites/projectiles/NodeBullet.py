import pygame
from sprites.Projectile import Projectile
from classes.Direction import Direction

class NodeBullet(Projectile):
    def __init__(self, start_pos, target_unit_vector, target_dir, attributes):
        super(NodeBullet, self).__init__(start_pos, target_unit_vector, target_dir, "assets/Projectiles/NodeBullet.png", (16, 16), attributes)

        self.dist = 1000

    