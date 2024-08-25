import pygame
import random
from classes.Point import Point

class Experiance(pygame.sprite.Sprite):
    def __init__(self, pos, amount):
        super(Experiance, self).__init__()

        # center position
        self.pos = pos.copy()
        self.width = 12
        self.height = 12

        # decide on exp image
        images = ["assets/Drops/Ex.png"]
        url = images[random.randint(0, len(images)-1)]
        self.image = pygame.transform.scale(pygame.image.load(url).convert_alpha(), (self.width, self.height))

        # amount of Exp
        self.expValue = amount

    # draw experiance
    def draw(self, screen, bg_pos):
        screen.blit(self.image, (self.pos.x + bg_pos.x + self.width/2, -self.pos.y + bg_pos.y - self.height/2))

    # kill might add animation
    def expire(self):
        self.kill()

    # collect when near player
    def collect(self, player):
        if Point.euclidian_dist(player.pos, self.pos) < player.collect_range:
            self.expire()
            return self.expValue
        return 0







