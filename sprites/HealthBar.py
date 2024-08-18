import pygame

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, health):
        super(HealthBar, self).__init__()
        
        self.width = 150
        self.height = 50
        self.outer_surf = pygame.Surface((self.width, self.height))
        self.inner_surf = pygame.Surface((self.width-4, self.height-4))
        

        self.health = health

