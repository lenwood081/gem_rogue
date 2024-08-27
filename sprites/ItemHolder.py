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
        self.level_health_bonus = 1.3
        self.armour = self.max_armour = 0
        self.sheild = self.max_sheild = 0
        self.weight = self.max_weight = 1

        # hurt image time and display
        self.being_hurt = False
        self.time_refresh_currect = self.time_refresh = 10

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
        self.level_damage_bonus = 1.2
        self.knockback = self.max_knockback = 0
        self.attack_rate = self.max_attack_rate = 1
        self.projectile_speed = self.max_projectile_speed = 20

        # level
        self.level = 0

        # drops
        self.exp = 1

        # weapons
        self.weapons = pygame.sprite.Group()

    def level_up(self):
        self.level += 1
        # increase max/base stats

        # health
        self.max_health *= self.level_health_bonus

        # damage
        self.max_damage *= self.level_damage_bonus

        # exp drops

        # reset health
        self.health = self.max_health
        self.damage = self.max_damage
    
    # for setting level, if used more than once on a player/enemy it will end up being much higher then expected
    def set_level(self, level):
        self.level = level
        # increase max/base stats

        # health
        self.max_health *= self.level_health_bonus**self.level

        # damage
        self.max_damage *= self.level_damage_bonus**self.level

        # exp drops
        
        # reset health and damage
        self.health = self.max_health
        self.damage = self.max_damage
        

    # ------------------------------ General functions ----------------------------

    # for taking damage
    def take_damage(self, damage, unit_vector, knockback):
        if self.immune:
            return

        # calculate knockback, and if stunned
        knockback_dist = 0
        if knockback >= self.weight:
            self.stunned = True
            knockback_dist = knockback * 10 / self.weight 

        # preform knockback
        if knockback_dist > 0:
            self.pos.x += unit_vector.x * knockback_dist
            self.pos.y += unit_vector.y * knockback_dist

        # armour at 10 = %50, at 20 = %66.66 at 30 = %75 damage deflected (tenno armour calculation)
        self.health -= damage - damage*(self.armour/(self.armour + 10))

        # for being_hurt
        self.being_hurt = True
        self.time_refresh_currect = self.time_refresh

        if self.health <= 0:
            self.death()
            return
        
        # damage immunity frame?
        self.immune = True
        self.immunity_frames = self.immunity_frames_gained


