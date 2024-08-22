import pygame


class Glow:

    @staticmethod
    def circle_surf(radius, color):
        surf = pygame.Surface((radius*2, radius*2))
        pygame.draw.circle(surf, color, (radius, radius), radius)
        surf.set_colorkey((0, 0, 0))
        return surf
    
    @staticmethod
    def oval_surf(height, width, color):
        surf = pygame.Surface((width*2, height*2))
        rect = surf.get_rect()
        pygame.draw.ellipse(surf, color, rect, width)
        surf.set_colorkey((0, 0, 0))
        return surf
