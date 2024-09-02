import pygame
from config import SCALE_FACOTOR

class ItemDisplay:
    def __init__(self, item, x, y):

        # item values
        self.image = None
        if item:
            self.image = item.icon
        
        self.description = item.description

        # create box
        self.width, self.height = 400, 600
        self.base_surf = pygame.Surface((self.width, self.height)).convert_alpha()
        self.base_surf.fill((0, 0, 0))
        self.base_surf.set_alpha(200)
        self.rect = self.base_surf.get_rect(center = (x, y))

        self.image_rect = self.image.get_rect(center=(self.width/2, 100))
        

    # draw
    def draw(self, screen):
        self.base_surf.blit(self.image, self.image_rect)
        screen.blit(self.base_surf, self.rect)

