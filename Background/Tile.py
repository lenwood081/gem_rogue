from config import *
import pygame
from utility.Point import Point
from utility.Glow import Glow

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, images, enemy_group):
        super(Tile, self).__init__()
        # top left corner position
        self.pos = pos.copy()
        

        # image (it is assumed all tiles are 64 x 64)
        self.image = pygame.transform.scale(pygame.image.load(images[0]).convert_alpha(), (32*SCALE_FACOTOR, 32*SCALE_FACOTOR))
        self.rect = self.image.get_rect()

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.is_shoot_through = False
        self.spawn_tile = False

        self.center_pos = Point(self.pos.x + self.width/2, self.pos.y - self.height/2)

        # spawning enemy
        self.spawning = False
        self.enemy = None
        self.enemy_group = enemy_group
        self.spawn_timer = 0
        self.spawning_circle = Glow.circle_surf(self.width/2, (255, 0, 0)).convert_alpha()
        self.spawning_circle.set_alpha(200)

    # needs to be added to collision group to work
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

class Door(Tile):
    def __init__(self, pos, images,enemy_group):
        super().__init__(pos, images, enemy_group)

        self.open = False
        self.pass_group = pygame.sprite.Group()
        self.open_image = pygame.transform.scale(pygame.image.load(images[1]).convert_alpha(), (32*SCALE_FACOTOR, 32*SCALE_FACOTOR))
        self.closed_image = pygame.transform.scale(pygame.image.load(images[0]).convert_alpha(), (32*SCALE_FACOTOR, 32*SCALE_FACOTOR))

    # opens door
    def open_door(self):
        self.image = self.open_image
        self.open = True
    
    # close door
    def close_door(self):
        self.image = self.closed_image
        self.open = False

    # add to pass_group
    def add_member(self, sprite):
        self.pass_group.add(sprite)

    # remove from group
    def remove_member(self, sprite):
        pass

    # update function override to include changing image (TODO)
    def update(self, cam_offset, dt):
        return super().update(cam_offset, dt)

    # check whether to allow a sprite to pass though
    def enter_door(self, sprite):
        if self.open == False:
            return False
        
        # check if in pass_group
        if self.pass_group.__contains__(sprite):
            return True
        
        return False
    
class ACtivateTile(Tile):
    def __init__(self, pos, image, enemy_group):
        super().__init__(pos, image, enemy_group)