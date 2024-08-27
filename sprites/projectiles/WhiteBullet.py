import pygame
from sprites.Projectile import Projectile
from classes.Direction import Direction

# sort of basic bullet, without special properties

# TODO add a offset to the initial shooting position, also adding a glow would look good 
class WhiteBullet(Projectile):
    def __init__(self, start_pos, target_unit_vector, target_dir, attributes):
        super(WhiteBullet, self).__init__(start_pos, target_unit_vector, target_dir, "assets/Projectiles/simple_bullet.png", (16, 8), attributes)

        self.dist = 500

    

