import pygame
from sprites.Projectile import Projectile
from classes.Glow import Glow
from classes.Direction import Direction

# sort of basic bullet, without special properties

# TODO add a offset to the initial shooting position, also adding a glow would look good 
class WhiteBullet(Projectile):
    def __init__(self, start_pos, target_unit_vector, target_dir, damage, speed):
        super(WhiteBullet, self).__init__(start_pos, target_unit_vector, target_dir, "assets/Projectiles/White_bullet.png", 6, 12)
        
        # glow effect
        

        self.dist = 300
        self.speed = speed
        self.damage = damage

    # blit to screen
    def draw(self, screen, bg_pos):
        self.rect = self.image.get_rect(center=(
            self.pos.x + bg_pos.x, 
            -self.pos.y + bg_pos.y))
        screen.blit(self.image, self.rect)   

        # glow effect
        surf = Direction.rotate(self.dir.dir, Glow.oval_surf(self.width * 2, self.height * 2, (30, 30, 30)))
        surf2 = Direction.rotate(self.dir.dir, Glow.oval_surf(self.width, self.height, (40, 40, 40)))
        rect = surf.get_rect(center = (self.pos.x + bg_pos.x, -self.pos.y + bg_pos.y))
        rect2 = surf2.get_rect(center = (self.pos.x + bg_pos.x, -self.pos.y + bg_pos.y))

        screen.blit(surf, rect, special_flags=pygame.BLEND_RGB_ADD)
        screen.blit(surf2, rect2, special_flags=pygame.BLEND_RGB_ADD)

    def collisions(self, sprite_group):
        for sprite in sprite_group:
            if pygame.Rect.colliderect(self.rect, sprite.rect):
                self.deal_damage(sprite)
                self.take_damage(1)

    # take damage from hitting objects
    def take_damage(self, damage):
        self.current_health -= damage
          
    # deal damage to objects
    def deal_damage(self, sprite):
        sprite.take_damage(self.damage)

    def update(self, enemie_group):
        # move bullet
        self.move()

        # check for collisions
        self.collisions(enemie_group)

        # check remaining health
        self.check_health()

    # -------------------- Method for interacting and changing WhiteBullet values ----------------
    
    def increase_damage(self, damage):
        self.damage += damage

    def increase_speed(self, speed):
        self.speed += speed

    def increase_distance(self, dist):
        self.dist += dist

    def increase_health(self, health):
        self.start_health += health
        self.current_health = self.start_health
