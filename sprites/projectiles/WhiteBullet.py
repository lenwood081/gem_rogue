import pygame
from sprites.Projectile import Projectile

# sort of basic bullet, without special properties
class WhiteBullet(Projectile):
    def __init__(self, start_pos, target_unit_vector, target_dir, damage):
        super(WhiteBullet, self).__init__(start_pos, target_unit_vector, target_dir, "assets/Projectiles/White_bullet.png", 6, 12)
        self.dist = 300
        self.speed = 10

        self.damage = damage

    # blit to screen
    def draw(self, screen, bg_pos):
        self.rect = self.image.get_rect(center=(
            self.pos.x + bg_pos.x, 
            -self.pos.y + bg_pos.y))
        screen.blit(self.image, self.rect)   

    def collisions(self, sprite_group):
        for sprite in sprite_group:
            if pygame.Rect.colliderect(self.rect, sprite.rect):
                self.deal_damage(sprite)
                self.take_damage(1)

    def take_damage(self, damage):
        self.current_health -= damage
          

    def deal_damage(self, sprite):
        sprite.take_damage(self.damage)

    def update(self, enemie_group):
        self.move()

        # check for collisions
        self.collisions(enemie_group)

        # check remaining health
        self.check_health()
