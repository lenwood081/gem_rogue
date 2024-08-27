import pygame
from sprites.Projectile import Projectile
from classes.Direction import Direction

class NodeBullet(Projectile):
    def __init__(self, start_pos, target_unit_vector, target_dir, attributes):
        super(NodeBullet, self).__init__(start_pos, target_unit_vector, target_dir, "assets/Projectiles/NodeBullet.png", (16, 16), attributes)

        self.dist = 1000

    # blit to screen
    def draw(self, screen, bg_pos):
        self.rect = self.image.get_rect(center=(
            self.pos.x + bg_pos.x, 
            -self.pos.y + bg_pos.y))
        screen.blit(self.image, self.rect)

    