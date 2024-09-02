import pygame
import random
from sprites.projectiles.Projectile import Projectile
from effects.Particle import HitCircle

# for plasma guns
class GlowBullet(Projectile):
    def __init__(self, start_pos, target_unit_vector, target_dir, attributes):
        super(GlowBullet, self).__init__(start_pos, target_unit_vector, target_dir, "assets/Projectiles/bullet_glow_1.png", (60, 30), attributes)

        self.dist = 1500
        self.area_hit = True

    # blit to screen override for special flag
    def draw(self, screen):
        screen.blit(self.image, self.rect, special_flags=pygame.BLEND_RGBA_ADD)


     # deal damage to objects
    def deal_damage(self, sprite):
        super().deal_damage(sprite)
        sprite.particle_group.add(HitCircle(random.randint(20, 80), self.pos.x + (random.randint(0, 20) / 10 - 1) * 20, self.pos.y + (random.randint(0, 20) / 10 - 1) * 20, duration=random.randint(1,10)/80, alpha=random.randint(150, 255), color=(160, 32, 240)))
        sprite.particle_group.add(HitCircle(random.randint(20, 80), self.pos.x + (random.randint(0, 20) / 10 - 1) * 20, self.pos.y + (random.randint(0, 20) / 10 - 1) * 20, duration=random.randint(1,10)/80, alpha=random.randint(150, 255), color=(170, 36, 250)))
        sprite.particle_group.add(HitCircle(random.randint(20, 80), self.pos.x + (random.randint(0, 20) / 10 - 1) * 20, self.pos.y + (random.randint(0, 20) / 10 - 1) * 20, duration=random.randint(1,10)/80, alpha=random.randint(150, 255), color=(150, 30, 230)))


