import pygame
from config import *
from classes.Point import Point
from classes.Direction import Direction
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
        self.base_image = pygame.transform.scale(pygame.image.load("assets/player/Player.png").convert_alpha(), (PL_WIDTH, PL_HEIGHT))
        self.image = self.base_image
        self.hitbox_rect = self.base_image.get_rect(center=(
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT/2,
        ))
        self.rect = self.hitbox_rect.copy()

        # position reletive to background (centered)
        self.pos = Point(BG_WIDTH/2 + PL_WIDTH/2, -BG_HEIGHT/2 - PL_HEIGHT/2)
        self.pos_screen = Point(SCREEN_WIDTH/2, -SCREEN_HEIGHT/2)
        self.front = Direction(0)

        # health and armour
        self.max_health = 10
        self.current_health = self.max_health
        self.armour = 0
        self.immune = False
        self.immunity_frames = 0
        self.immunity_frames_gained = 15
        self.sheild = 0

    # blit player
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # death method
    def death(self):
        # reset to game screen
        self.kill()

    # for taking damage
    def take_damage(self, damage):
        if self.immune:  
            return

        self.current_health -= damage - damage*(self.armour * 0.01)
        if self.current_health <= 0:
            self.death()
            return
        
        # damage immunity frame?
        self.immune = True
        self.immunity_frames = self.immunity_frames_gained

    # rotating player
    def face_mouse(self):
        # find mouse pos
        mx, my = pygame.mouse.get_pos()
        mouse_pos = Point(mx, -my)

        mouse_dir = Point.direction_to_point(mouse_pos, self.pos_screen)
        self.image = Direction.rotate(mouse_dir.dir, self.base_image)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)
        self.front = mouse_dir
        
    # update loop
    def update(self, keys_pressed):
        if self.immune:
            self.immunity_frames -= 1
            if self.immunity_frames == 0:
                self.immune = False

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

        self.face_mouse()

        