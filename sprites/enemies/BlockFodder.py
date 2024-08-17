import pygame
from sprites.Enemy import Enemy

"""
this is the main basic enemy in the game, should just move towards the player,
only thing special is that it will have a radius turn
"""

class BlockFodder(Enemy):
    def __init__(self, x, y):
        super(BlockFodder, self).__init__(x, y, 30, 30)

    def update(self):
        pass