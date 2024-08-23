import pygame
from sprites.Projectile import Projectile
from classes.Direction import Direction

# sort of basic bullet, without special properties

# TODO add a offset to the initial shooting position, also adding a glow would look good 
class WhiteBullet(Projectile):
    def __init__(self, start_pos, target_unit_vector, target_dir, damage, speed):
        super(WhiteBullet, self).__init__(start_pos, target_unit_vector, target_dir, "assets/Projectiles/simple_bullet.png", 16, 8)

        self.dist = 500
        self.speed = speed
        self.damage = damage

    # blit to screen
    def draw(self, screen, bg_pos):
        self.rect = self.image.get_rect(center=(
            self.pos.x + bg_pos.x, 
            -self.pos.y + bg_pos.y))
        screen.blit(self.image, self.rect)

    def update(self, enemie_group):
        # move bullet
        self.move()

        # check for collisions
        self.collisions(enemie_group)

        # check remaining health
        self.check_health()
