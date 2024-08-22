import pygame
import math
from classes.Point import Point
from classes.Direction import Direction


class Weapon(pygame.sprite.Sprite):
    def __init__(self, pos, image_url, width, height, bg_pos):
        super(Weapon, self).__init__()

        # center
        self.pos = Point(pos.x, pos.y)
        self.front = Direction(0)

        self.base_image = pygame.transform.scale(pygame.image.load(image_url).convert_alpha(), (width, height))
        self.image = self.base_image
        self.hitbox_rect = self.base_image.get_rect(center=(
            self.pos.x + bg_pos.x, 
            -self.pos.y + bg_pos.y
        ))
        self.rect = self.hitbox_rect.copy()
        
        self.width = width
        self.height = height

        # damage
        self.damage = 5

        

    # face target
    def face_target(self, target_dir):
        # copy target direction
        self.front.dir = target_dir.dir

        # move image
        self.image = Direction.rotate(self.front.dir, self.base_image)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)





