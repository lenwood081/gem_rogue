import pygame
from config import SCALE_FACOTOR
from sprites.ItemHolder import ItemHolder
from utility.Point import Point

class Activator(pygame.sprite.Sprite):
    def __init__(self, height, width, pos:Point, cam_offset) -> None:
        super().__init__()

        self.height = height*SCALE_FACOTOR
        self.width = width*SCALE_FACOTOR

        self.pos = pos.copy()

        # make traansperant surface
        self.surf = pygame.Surface((self.height, self.width))
        self.surf.fill((0, 0, 0))
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect(center=(
            self.pos.x + cam_offset,
            -self.pos.y + cam_offset,
        ))

        # determine if activated
        self.active = False
        
        # affect sprite group
        self.affect_group = pygame.sprite.Group()

    def update_rect(self, cam_offset):
        self.rect.center = (
            self.pos.x + cam_offset,
            -self.pos.y + cam_offset,
        ) 
    
    def draw(self, screen):
        screen.blit(self.surf)

    def activate(self, sprite:ItemHolder, keys=None):
        self.active = True
    
    def deactivate(self):
        self.active = False

    def add_sprites(self, sprite):
        self.affect_group.add(sprite)

# activates if a sprite is close enough
class DistActivator(Activator):
    def __init__(self, height, width, pos: Point, distance, cam_offset) -> None:
        super().__init__(height, width, pos, cam_offset)

        self.activate_distance = distance*SCALE_FACOTOR

    # check if the key is a match, input is acitve keys
    def activate(self, sprite:ItemHolder, keys=None):
        # check that it is the correct group
        if sprite not in self.affect_group:
            return

        assert(keys!=None)

        # should check the cartisian distance between the two points
        if Point.euclidian_dist(self.pos, sprite.pos) < self.activate_distance:
            super().activate(sprite)

# activates whena  sprite is close enough and presses a key
class KeyActivator(Activator):
    def __init__(self, height, width, pos: Point, activate_key, cam_offset) -> None:
        super().__init__(height, width, pos, cam_offset)
        
        self.activate_key = activate_key
        self.activate_distance = 70*SCALE_FACOTOR

    # check if the key is a match, input is acitve keys
    def activate(self, sprite:ItemHolder, keys=None):
        # check that it is the correct group
        if sprite not in self.affect_group:
            return

        assert(keys!=None)

        # should check the cartisian distance between the two points
        if Point.euclidian_dist(self.pos, sprite.pos) < self.activate_distance:
            if keys[self.activate_key]: 
                super().activate(sprite)
        