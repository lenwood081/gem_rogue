import pygame
from config import *
from classes.Point import Point

# change this to tiles

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super(Background, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/background/pebble-rock-ground.png").convert_alpha(), (BG_WIDTH, BG_HEIGHT))
        self.rect = self.image.get_rect()

        self.surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surf.fill(BG_HORROR_SHADE)
        self.surf2 = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surf2.fill(BG_OVERLAY_SHADE)

        # for determining position of background 
        self.location = Point(BG_WIDTH, -BG_HEIGHT)

    def draw(self, screen, cam_offset):
        screen.blit(self.image, (cam_offset.x, cam_offset.y))
        screen.blit(self.surf, (0,0), special_flags=pygame.BLEND_RGBA_SUB)


    def draw_after(self, screen):
        screen.blit(self.surf2, (0,0), special_flags=pygame.BLEND_RGBA_SUB)

    def update(self, player_pos):
        # the player x and y represent where the center of the screen should be
        self.location.x = SCREEN_WIDTH/2 - player_pos.x
        self.location.y = SCREEN_HEIGHT/2 + player_pos.y