import pygame
from config import *
from classes.Point import Point

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super(Background, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/background/pebble-rock-ground.png").convert_alpha(), (BG_WIDTH, BG_HEIGHT))
        self.rect = self.image.get_rect()
        self.surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surf.fill(BG_HORROR_SHADE)

        # for determining position of background
        self.location = Point(SCREEN_WIDTH/2 - BG_WIDTH/2, SCREEN_HEIGHT/2 - BG_HEIGHT/2)

    def draw(self, screen):
        screen.blit(self.image, (self.location.x, self.location.y))

    def draw_after(self, screen):
        screen.blit(self.surf, (0,0), special_flags=pygame.BLEND_RGB_SUB)

    def update(self, player_pos):
        # the player x and y represent where the center of the screen should be
        self.location.x = SCREEN_WIDTH/2 - player_pos.x
        self.location.y = SCREEN_HEIGHT/2 + player_pos.y