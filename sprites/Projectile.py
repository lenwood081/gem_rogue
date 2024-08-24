import pygame
import math
from classes.Direction import Direction
from classes.Point import Point 
 
class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_unit_vector, target_dir, image_url, width, height):
        super(Projectile, self).__init__()
        self.pos = start_pos.copy()
        self.base_image = pygame.transform.scale(pygame.image.load(image_url).convert_alpha(), (width, height))
        self.image = self.base_image
        self.hitbox_rect = self.base_image.get_rect()
        self.rect = self.hitbox_rect.copy()
        self.width = width
        self.height = height

        # target point      
        self.target_unit_vector = target_unit_vector
        self.dir = target_dir
        self.dist = 300

        # health
        self.start_health = 1
        self.current_health = 1
        self.area_hit = False

        # damage
        self.damage = 1
        self.knockback = 3

        # speed
        self.speed = 10
        self.falloff = 0
        self.time_alive = 0

        # rotate
        self.rotate()

        # move away from sprite for initial fire
        self.move()
        self.move()
        self.move()

    # check bullet health
    def check_health(self):
        if self.current_health <= 0:
            self.expire()

    # collisions
    def collisions(self, sprite_group):
        for sprite in sprite_group:
            if pygame.Rect.colliderect(self.rect, sprite.rect):
                self.deal_damage(sprite)
                self.take_damage(1)
                if self.area_hit == False:
                    return

    # deal damage to objects
    def deal_damage(self, sprite):
        sprite.take_damage(self.damage, self.target_unit_vector, self.knockback)

    # take damage from hitting objects
    def take_damage(self, damage):
        self.current_health -= damage

    # when health is zero or is too much distance
    def expire(self):
        self.kill()

    # rotate to target direction
    def rotate(self):
        self.image = Direction.rotate_with_flip(self.dir.dir, self.base_image)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)

    # move towards target
    def move(self):
        # check dist
        if self.dist <= 0:
            self.expire()
            return
        
        # move based on speed and unit vector
        self.pos.x += self.speed * self.target_unit_vector.x
        self.pos.y += self.speed * self.target_unit_vector.y

        # decrement dist
        self.dist -= self.speed

    # -------------------- Method for interacting and changing projectile values ----------------
    
    def increase_damage(self, damage):
        self.damage += damage

    def increase_speed(self, speed):
        self.speed += speed

    def increase_distance(self, dist):
        self.dist += dist

    def increase_health(self, health):
        self.start_health += health
        self.current_health = self.start_health
    
        



        