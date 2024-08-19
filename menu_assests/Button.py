import pygame
from classes.Point import Point

class Button:
    def __init__(self, image_url, x, y):
        self.pos = Point(x, y)
        self.image = pygame.image.load(image_url).convert_alpha()
        self.rect = self.image.get_rect(center=(
            self.pos.x,
            self.pos.y,
        ))

        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        # if mouse is pressed over object
        pass