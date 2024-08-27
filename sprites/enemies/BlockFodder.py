import pygame
import random
from sprites.Enemy import Enemy
from classes.Direction import Direction

"""
this is the main basic enemy in the game, should just move towards the player,
"""

class BlockFodder(Enemy):
    def __init__(self, pos, experiance_group):
        super(BlockFodder, self).__init__(pos, "assets/enemies/blockfodder/base.png", (40, 40), experiance_group)
        # ---------------------- ITEM HOLDER ATTRIBUTES -------------------

        # slightly random speed
        self.speed = self.max_speed = random.uniform(self.speed, self.speed+3)  

        # attack
        self.damage = self.max_damage = 1

        # health and armour
        self.health = self.max_health = 4
        self.armour = self.max_armour = 2

        # -----------------------------------------------------------------

        # being hurt
        self.image_hurt_base = pygame.transform.scale(pygame.image.load("assets/enemies/blockfodder/hurt.png").convert_alpha(), (self.width, self.height))
        self.image_hurt = self.image_hurt_base


    # TODO REMOVE blit calls from game entry to streamline for loop through different enemies
    def draw(self, screen, bg_pos):
        self.hitbox_rect.center = (self.pos.x + bg_pos.x, -self.pos.y + bg_pos.y)
        self.rect.center = self.hitbox_rect.center

        if self.being_hurt:
            #rotate hurt image
            self.image_hurt = Direction.rotate(self.front.dir, self.image_hurt_base)
            screen.blit(self.image_hurt, self.rect)
            return

        screen.blit(self.image, self.rect) 

        #pygame.draw.rect(screen, "red", self.hitbox_rect, width=2)
        #pygame.draw.rect(screen, "blue", self.rect, width=2)