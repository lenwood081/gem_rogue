import pygame


class Glow:

    @staticmethod
    def circle_surf(radius, color):
        surf = pygame.Surface((radius*2, radius*2)).convert_alpha()
        pygame.draw.circle(surf, color, (radius, radius), radius)
        surf.set_colorkey((0, 0, 0))
        return surf
    
    @staticmethod
    def bullet_surf(height, width):
        image = pygame.transform.scale(pygame.image.load("assets/player/bullet_glow_1.png").convert_alpha(), (width*2, height*2))
        return image
    
    @staticmethod
    def circle_image_add(radius):
        image = pygame.transform.scale(pygame.image.load("assets/effects/glow_add_circle.png").convert_alpha(), (radius*2, radius*2))
        return image
