from config import *
import pygame
from classes.Point import Point

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super(Tile, self).__init__()
        # top left corner position
        self.pos = pos.copy()

        # image (it is assumed all tiles are 64 x 64)
        self.image = pygame.transform.rotozoom(pygame.image.load(image).convert_alpha(), 0, SCALE_FACOTOR)
        self.rect = self.image.get_rect()

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.shoot_through = False

    # update rect object (only needed for boundary boxes)
    def update(self, cam_offset):
        self.rect.topleft = (cam_offset.x + self.pos.x, cam_offset.y - self.pos.y)

    # draw method
    def draw(self, screen, cam_offset):
        self.update(cam_offset)
        screen.blit(self.image, self.rect)


