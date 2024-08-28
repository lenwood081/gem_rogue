import pygame
from sprites.Projectile import Projectile

# for plasma guns
class GlowBullet(Projectile):
    def __init__(self, start_pos, target_unit_vector, target_dir, attributes):
        super(GlowBullet, self).__init__(start_pos, target_unit_vector, target_dir, "assets/Projectiles/bullet_glow_1.png", (50, 20), attributes)

        self.dist = 500

        self.area_hit = True

    # blit to screen override for special flag
    def draw(self, screen):
        screen.blit(self.image, self.rect, special_flags=pygame.BLEND_RGBA_ADD)

