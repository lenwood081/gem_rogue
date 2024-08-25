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

        # for being_hurt
        self.being_hurt = False
        self.time_refresh_currect = self.time_refresh

        # speed
        self.speed = self.max_speed = 4

        # attacking
        self.damage = self.max_damage = 1
        self.knockback = self.max_knockback = 0
        self.attack_rate = self.max_attack_rate = 5

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

    # ------------------------------ General functions ----------------------------

    # for taking damage
    def take_damage(self, damage, unit_vector, knockback):
        if self.immune:
            return

        # calculate knockback
        knockback_dist = 0
        if knockback >= self.weight:
            self.stunned = True
            knockback_dist = knockback * 10 / self.weight 

        # preform knockback
        if knockback_dist > 0:
            self.pos.x += unit_vector.x * knockback_dist
            self.pos.y += unit_vector.y * knockback_dist

        self.health -= damage - damage*(self.armour * 0.01)

        # for being_hurt
        self.being_hurt = True
        self.time_refresh_currect = self.time_refresh

        if self.health <= 0:
            self.death()
            return
        
        # damage immunity frame?
        self.immune = True
        self.immunity_frames = self.immunity_frames_gained


