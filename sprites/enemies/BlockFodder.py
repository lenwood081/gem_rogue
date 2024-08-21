import pygame
from sprites.Enemy import Enemy

"""
this is the main basic enemy in the game, should just move towards the player,
only thing special is that it will have a radius turn
"""

class BlockFodder(Enemy):
    def __init__(self, x, y):
        self.width = 40
        self.height = 40
        super(BlockFodder, self).__init__(x, y, "assets/enemies/blockfodder/base.png", self.height, self.width)

        # personal stats to blockfodder
        self.attack_damage = 1
        self.hit_damage = self.attack_damage

    def update(self, player_pos):
        dir = self.move_towards_player(player_pos)
        self.pos.x += self.speed * dir.x
        self.pos.y += self.speed * dir.y

    # TODO REMOVE blit calls from game entry to streamline for loop through different enemies
    def draw(self, screen, bg_pos):
        self.hitbox_rect = self.surf.get_rect(center=(
            self.pos.x + bg_pos.x, 
            -self.pos.y + bg_pos.y))
        screen.blit(self.surf, self.hitbox_rect) 