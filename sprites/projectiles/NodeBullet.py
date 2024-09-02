import pygame
from sprites.projectiles.Projectile import Projectile
from utility.Direction import Direction
from config import SCALE_FACOTOR

class NodeBullet(Projectile):
    def __init__(self, start_pos, target_unit_vector, target_dir, attributes):
        super(NodeBullet, self).__init__(start_pos, target_unit_vector, target_dir, "assets/Projectiles/NodeBullet.png", (16*SCALE_FACOTOR, 16*SCALE_FACOTOR), attributes)

        self.dist = 1000

    