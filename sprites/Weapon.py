import pygame
import math
from classes.Point import Point
from classes.Direction import Direction
from config import FRAMERATE

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

        # general
        self.width = width
        self.height = height
        self.angle_on_player = 0

        # damage
        self.damage = 5
        self.fire_rate = 1
        self.frame_till_fire = 0

        # autofire
        self.autofire = False
        self.fire = False

    # face target
    def face_target(self, target_dir):
        # copy target direction
        self.front.dir = target_dir.dir

        # move image
        self.image = Direction.rotate_with_flip(self.front.dir, self.base_image)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)

    # check if can attack
    def can_attack(self):
        if self.frame_till_fire <= 0:
            return True
        
        self.frame_till_fire -= 1
        return False
    
    # check if need to attack
    def do_attack(self, fire):
        if fire or self.autofire:
            fire_rate = FRAMERATE * 1/self.fire_rate
            self.frame_till_fire = fire_rate
            return True
        return False
        





