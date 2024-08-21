import pygame
from sprites.Enemy import Enemy

class BlockRange(Enemy):
    def __init__(self, x, y):
        super(BlockRange, self).__init__(x, y, image, 40, 40)
        