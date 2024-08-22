import pygame
import math
from classes.Point import Point
from classes.Direction import Direction
from config import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH
)

class Weapon(pygame.sprite.Sprite):
    def __init__(self, x, y, image_url, width, height):
        super(Weapon, self).__init__()
        self.base_image = pygame.transform.scale(pygame.image.load(image_url).convert_alpha(), (width, height))
        self.image = self.base_image
        self.hit_rect = self.base_image.get_rect(center=(
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT/2,
        ))
        self.rect = self.hit_rect.copy()
        self.width = width
        self.height = height

        # center
        self.pos = Point(x, y)
        self.front = Direction(0)

    # face target
    def face_target(self, target_dir):
        # copy target direction
        self.front.dir = target_dir.dir

        # move image
        self.image = Direction.rotate(self.front.dir, self.base_image)
        self.rect = self.image.get_rect(center=self.hit_rect.center)





