import pygame
from config import *
from classes.Point import Point

class ExpBar(pygame.sprite.Sprite):
    def __init__(self, player):
        super(ExpBar, self).__init__()

        # dimensions
        self.width = SCREEN_WIDTH/2
        self.height = 20
        self.pos = Point((SCREEN_WIDTH-self.width)/2, SCREEN_HEIGHT-100)

        # create image of fixed length
        #self.outer_surf = pygame.transform.scale(pygame.image.load("assets/HUD/BarOuter.png").convert_alpha(), (self.width, self.height))
        self.inner_surf = pygame.Surface((0, self.height))

        # create level varible and text feilds on either side
        self.current_level = player.level
        self.target_level = self.current_level + 1
        self.exp_to_level = player.exp_to_level
        self.exp_current = player.exp


    def draw(self, screen):
        screen.blit(self.inner_surf, (self.pos.x, self.pos.y))
        #screen.blit(self.outer_surf, (self.pos.x, self.pos.y))

    def update(self, player_level, player_exp_to_level, player_current_exp):
        changed = False

        # check if changed 
        if player_level != self.current_level or player_exp_to_level != self.exp_to_level:
            self.current_level = player_level  
            self.target_level = player_level + 1
            self.exp_to_level = player_exp_to_level
            changed = True

        # move bar
        if player_current_exp != self.exp_current or changed:
            self.exp_current = player_current_exp
            percentage = self.exp_current/self.exp_to_level
            self.inner_surf = pygame.Surface((percentage * self.width, self.height))
            self.inner_surf.fill((0,255, 0))

