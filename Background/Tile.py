from config import *
import pygame
from utility.Point import Point

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image, enemy_group):
        super(Tile, self).__init__()
        # top left corner position
        self.pos = pos.copy()
        

        # image (it is assumed all tiles are 64 x 64)
        self.image = pygame.transform.rotozoom(pygame.image.load(image).convert_alpha(), 0, SCALE_FACOTOR)
        self.rect = self.image.get_rect()

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.shoot_through = False
        self.spawn_tile = False

        self.center_pos = Point(self.pos.x + self.width/2, self.pos.y - self.height/2)

        # spawning enemy
        self.spawning = False
        self.enemy = None
        self.enemy_group = enemy_group
        self.spawn_timer = 0

    # update rect object and spawning
    def update(self, cam_offset, dt):
        if self.spawning:
            self.spawn_timer -= 1 * dt
            if self.spawn_tile <= 0:
                self.enemy_group.add(self.enemy)
                self.enemy = None
                self.spawning = False
                self.spawn_timer = 3 * FRAMERATE


        self.rect.topleft = (cam_offset.x + self.pos.x, cam_offset.y - self.pos.y)

    # draw method
    def draw(self, screen, cam_offset):
        screen.blit(self.image, self.rect)


