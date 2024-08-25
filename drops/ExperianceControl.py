import pygame
from drops.Experiance import Experiance

class ExperianceControl:
    def __init__(self, player_group):
        self.group = pygame.sprite.Group()
        self.player_group = player_group

    # clears all experiance
    def clear(self):
        for exp in self.group:
            exp.expire()

    # draws all experiance
    def draw(self, screen, bg_pos):
        for exp in self.group:
            exp.draw(screen, bg_pos)

    # returns refernce for experiance group
    def get_group(self):
        return self.group
    
    def update(self):
        for exp in self.group:
            for player in self.player_group:
                exp = exp.collect(player)
                if exp > 0:
                    player.add_exp(exp)
