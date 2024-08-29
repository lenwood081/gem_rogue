import pygame
from sprites.projectiles.Projectile import Projectile

# for plasma guns
class GlowBullet(Projectile):
    def __init__(self, start_pos, target_unit_vector, target_dir, attributes):
        super(GlowBullet, self).__init__(start_pos, target_unit_vector, target_dir, "assets/Projectiles/bullet_glow_1.png", (60, 30), attributes)

        self.dist = 1500

        self.area_hit = True

    # blit to screen override for special flag
    def draw(self, screen):
        screen.blit(self.image, self.rect, special_flags=pygame.BLEND_RGBA_ADD)

