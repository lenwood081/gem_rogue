import pygame
from config import *
from classes.Point import Point
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
)
import math

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((PL_WIDTH, PL_HEIGHT))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT/2,
        ))

        # position reletive to background (centered)
        self.pos = Point(BG_WIDTH/2 + PL_WIDTH/2, -BG_HEIGHT/2 - PL_HEIGHT/2)

        # health and armour
        self.health = 10
        self.armour = 0
        self.immune = False
        self.immunity_frames = 0
        self.immunity_frames_gained = 30
        self.sheild = 0

    # death method
    def death(self):
        # reset to game screen
        self.kill()

    # for taking damage
    def take_damage(self, damage):
        if self.immune:
            self.immunity_frames -= 1
            if self.immunity_frames == 0:
                self.immune = False   
            return

        self.health -= damage - damage*(self.armour * 0.01)
        if self.health <= 0:
            self.death()
            return
        
        # damage immunity frame?
        self.immune = True
        self.immunity_frames = self.immunity_frames_gained
        

    def update(self, keys_pressed):
        x = 0
        y = 0

        # player movement
        if keys_pressed[K_s]:
            y = -PL_SPEED
        if keys_pressed[K_w]:
            y = PL_SPEED
        if keys_pressed[K_d]:
            x = PL_SPEED
        if keys_pressed[K_a]:
            x = -PL_SPEED

        # check for diagonal speed irregularity
        if x != 0 and y != 0:
            x /= math.sqrt(2)
            y /= math.sqrt(2)

        self.pos.move(x, y)

        # movement restriction (BG_WIDTH and BG_HEIGHT)
        if self.pos.x > BG_WIDTH - PL_WIDTH/2:
            self.pos.x = BG_WIDTH - PL_WIDTH/2
        if self.pos.x < PL_WIDTH/2:
            self.pos.x = PL_WIDTH/2
        if self.pos.y < -BG_HEIGHT + PL_HEIGHT/2:
            self.pos.y = -BG_HEIGHT + PL_HEIGHT/2
        if self.pos.y > -PL_HEIGHT/2:
            self.pos.y = -PL_HEIGHT/2