from config import *
import pygame
from utility.Point import Point
from utility.Glow import Glow

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image, enemy_group):
        super(Tile, self).__init__()
        # top left corner position
        self.pos = pos.copy()
        

        # image (it is assumed all tiles are 64 x 64)
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (32*SCALE_FACOTOR, 32*SCALE_FACOTOR))
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
        self.spawning_circle = Glow.circle_surf(self.width/2, (255, 0, 0)).convert_alpha()
        self.spawning_circle.set_alpha(200)


    # update rect object and spawning
    def update(self, cam_offset, dt):
        # check if spawning
        if self.spawning:
            self.spawn_timer -= 1 * dt
            if self.spawn_timer <= 0:
                self.enemy_group.add(self.enemy)
                self.enemy = None
                self.spawning = False


        self.rect.center = (cam_offset.x + self.pos.x, cam_offset.y - self.pos.y)

    # draw method
    def draw(self, screen):
        screen.blit(self.image, self.rect)

        if self.spawning:
            screen.blit(self.spawning_circle, self.rect)


    # spawn enemy
    def spawn_enemy(self, enemy):
        self.enemy = enemy
        self.spawning = True
        self.spawn_timer = 2 * FRAMERATE