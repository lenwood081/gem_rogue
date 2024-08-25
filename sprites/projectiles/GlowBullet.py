import pygame
from sprites.Projectile import Projectile

# for plasma guns
class GlowBullet(Projectile):
    def __init__(self, start_pos, target_unit_vector, target_dir, speed):
        super(GlowBullet, self).__init__(start_pos, target_unit_vector, target_dir, "assets/Projectiles/bullet_glow_1.png", 50, 20)

        self.dist = 500
        self.speed = speed
        self.knockback = 0

        self.area_hit = True

    # blit to screen
    def draw(self, screen, bg_pos):
        self.rect = self.image.get_rect(center=(
            self.pos.x + bg_pos.x, 
            -self.pos.y + bg_pos.y))
        screen.blit(self.image, self.rect, special_flags=pygame.BLEND_RGBA_ADD)

