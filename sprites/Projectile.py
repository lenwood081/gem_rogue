import pygame
import math
from classes.Direction import Direction
from classes.Point import Point 
 
class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_unit_vector, target_dir, image_url, size, attributes):
        super(Projectile, self).__init__()
        self.pos = start_pos.copy()
        self.image = pygame.transform.scale(pygame.image.load(image_url).convert_alpha(), (size[0], size[1]))
        self.base_image = self.image
        self.hitbox_rect = self.base_image.get_rect()
        self.rect = self.hitbox_rect.copy()
        self.width = size[0]
        self.height = size[1]

        # target point      
        self.target_unit_vector = target_unit_vector
        self.dir = target_dir
        self.dist = 300

        # health
        self.start_health = 1
        self.current_health = 1
        self.area_hit = False

        # damage
        self.damage = attributes[1]
        self.knockback = attributes[2]

        # speed
        self.speed = attributes[0]
        self.falloff = 0
        self.time_alive = 0

        # rotate
        self.rotate()

    # check bullet health
    def check_health(self):
        if self.current_health <= 0:
            self.expire()

    # collisions
    def collisions(self, sprite_group):
        for sprite in sprite_group:
            if pygame.Rect.colliderect(self.hitbox_rect, sprite.hitbox_rect):
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

    # basic update loop can be overriden
    def update(self, enemie_group):
        # move bullet
        self.move()

        # check for collisions
        self.collisions(enemie_group)

        # check remaining health
        self.check_health()

    # blit to screen
    def draw(self, screen, cam_offset):
        self.hitbox_rect.center = (self.pos.x + cam_offset.x, -self.pos.y + cam_offset.y)
        self.rect.center = self.hitbox_rect.center
        screen.blit(self.image, self.rect)

        #pygame.draw.rect(screen, "red", self.hitbox_rect, width=2)
        #pygame.draw.rect(screen, "blue", self.rect, width=2)

        



        