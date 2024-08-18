import pygame
import random
from sprites.Enemy import Enemy

"""
this is the main basic enemy in the game, should just move towards the player,
only thing special is that it will have a radius turn
"""

class BlockFodder(Enemy):
    def __init__(self, x, y):
        super(BlockFodder, self).__init__(x, y, "assets/enemies/blockfodder/base.png")

        # personal stats to blockfodder
        self.attack_damage = 1
        self.hit_damage = self.attack_damage

    # occurs when colliding with a player
    # if in an attck then does more damage
    def attack(self):
        return self.attack_damage

    def update(self, player_pos):
        dir = self.move_towards_player(player_pos)
        self.pos.x += self.speed * dir.x
        self.pos.y += self.speed * dir.y