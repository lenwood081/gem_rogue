from config import *
import pygame
from classes.Point import Point

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        # top left corner position
        self.pos = pos.copy()

        # image (it is assumed all tiles are 64 x 64)
        self.image = pygame.transform.rotozoom(pygame.image.load(image).convert_alpha(), 0, SCALE_FACOTOR)

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    # draw method
    def draw(self, screen, cam_offset):
        screen.blit(self.image, (cam_offset.x + self.pos.x, cam_offset.y - self.pos.y))


