import pygame
import random
from sprites.Enemy import Enemy

"""
will create a distance and shoot, should puase when shooting
"""

class BlockRange(Enemy):
    def __init__(self, pos, experiance_group):
        super(BlockRange, self).__init__(pos, "", (40, 40), experiance_group)
        # ---------------------- ITEM HOLDER ATTRIBUTES -------------------

        # slightly random speed
        self.speed = self.max_speed = 4  

        # attack
        self.damage = self.max_damage = 2

        # -----------------------------------------------------------------

    # draw method
    def draw(self, sceen, bg_pos):
        pass

    # update method override
    def update(self, player_pos):
        self.being_hit()

        unit_vector = self.move_towards_player(player_pos)

        # when a certain distance is reached try to maintain it by circling and shooting

        # shooting should puase the character
        