import pygame


# class that is inherited for sprites that require items, dfines basic stats

class ItemHolder(pygame.sprite.Sprite):
    def __init__(self):
        super(ItemHolder, self).__init__()

        # width and height
        self.width = self.max_width = 23
        self.height = self.max_height = 23

        # health and armour
        self.health = self.max_health = 10
        self.armour = self.max_armour = 0
        self.sheild = self.max_sheild = 0
        self.weight = self.max_weight = 1

        # hurt image time and display
        self.being_hurt = False
        self.time_refresh_currect = self.time_refresh = 7

        # hit handeling
        self.immune = False
        self.immunity_frames = 0
        self.immunity_frames_gained = 15
        self.stunned = False
        self.time_stunned = self.recover_time = 3

        # speed
        self.speed = self.max_speed = 4

        # attacking
        self.damage = self.max_damage = 1

        # level
        self.level = 0

        # drops
        self.exp = 1

        # weapons
        self.weapons = pygame.sprite.Group()

    def level_up(self):
        self.level += 1

        # reset health
        self.health = self.max_health
        # increase base stats
