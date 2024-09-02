import pygame
import random
from utility.Point import Point
from config import SCALE_FACOTOR
from utility.Glow import Glow

class Experiance(pygame.sprite.Sprite):
    def __init__(self, pos, amount):
        super(Experiance, self).__init__()

        # center position
        self.pos = pos.copy()
        self.width = 16*SCALE_FACOTOR
        self.height = 16*SCALE_FACOTOR

        # decide on exp image
        images = ["assets/Drops/Ex.png"]
        url = images[random.randint(0, len(images)-1)]
        self.image = pygame.transform.scale(pygame.image.load(url).convert_alpha(), (self.width, self.height))
        
        # create glow
        self.glow = Glow.circle_image_add(self.width)
        self.green = Glow.circle_surf(self.width, (0, 10, 0)) 

        # amount of Exp
        self.expValue = amount

    # draw experiance
    def draw(self, screen, cam_offset):
        screen.blit(self.green, (self.pos.x + cam_offset.x, -self.pos.y + cam_offset.y - self.height), special_flags=pygame.BLEND_RGBA_ADD)
        screen.blit(self.glow, (self.pos.x + cam_offset.x, -self.pos.y + cam_offset.y - self.height), special_flags=pygame.BLEND_RGBA_ADD)
        
        screen.blit(self.image, (self.pos.x + cam_offset.x + self.width/2, -self.pos.y + cam_offset.y - self.height/2))

    # kill might add animation
    def expire(self):
        self.kill()

    # collect when near player
    def collect(self, player):
        if Point.euclidian_dist(player.pos, self.pos) < player.collect_range:
            self.expire()
            return self.expValue
        return 0







