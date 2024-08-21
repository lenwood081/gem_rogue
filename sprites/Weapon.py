import pygame
from classes.Point import Point
from classes.Direction import Direction

class Weapon(pygame.sprite.Sprite):
    def __init__(self, parent_pos, image_url, width, height):
        super(Weapon, self).__init__()
        self.base_image = pygame.transform.scale(pygame.image.load(image_url).convert_alpha(), (width, height))
        self.image = self.base_image
        self.width = width
        self.height = height

        # center
        self.pos = Point(parent_pos.x, parent_pos.y)
        self.front = Direction(0)

    def draw(self, screen):
        # change center to top left
        screen.blit(self.image, (self.pos.x - self.width/2, self.pos.y - self.height/2))


    def face_target(self, target_dir):
        # copy target direction
        self.front.x = target_dir.x
        self.front.y = target_dir.y



