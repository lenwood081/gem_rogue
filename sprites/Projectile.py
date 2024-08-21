import pygame
from classes.Direction import Direction
from classes.Point import Point 

class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, dist, target_unit_vector, target_dir, image_url, width, height):
        super(Projectile, self).__init__()
        self.pos = (start_x, start_y)
        self.base_image = pygame.transform.scale(pygame.image.load(image_url).convert_alpha(), (width, height))
        self.image = self.base_image
        self.hitbox_rect = self.base_image.get_rect()
        self.rect = self.hitbox_rect.copy()

        # target point      
        self.target_unit_vector = target_unit_vector
        self.dir = target_dir

        # health
        self.start_health = 1
        self.current_health = 1

        # damage
        self.damage = 1

        # speed
        self.speed = 5
        self.falloff = 0
        self.time_alive = 0
    
    # blit to screen
    def draw(self, screen, bg_pos):
        self.hitbox_rect = self.image.get_rect(center=(
            self.pos.x + bg_pos.x, 
            -self.pos.y + bg_pos.y))
        screen.blit(self.image, self.hitbox_rect) 

    # when health is zero or is too much distance
    def expire(self):
        self.kill()

    # rotate to target direction
    def rotate(self):
        pass

    # move towards target
    def move(self):
        # check dist
        if self.dist <= 0:
            self.expire()
            return
        
        # move based on speed and unit vector
        self.pos.x += self.speed * self.target_unit_vector.x
        self.pos.y += self.speed * self.target_unit_vector.y

    def update(self):
        self.move(self)

        # check for collisions
        



        