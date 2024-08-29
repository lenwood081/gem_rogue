from config import *
import random
from sprites.Enemy import Enemy
from Animations.Animation import Animation

"""
this is the main basic enemy in the game, should just move towards the player,
"""

class BlockFodder(Enemy):
    def __init__(self, pos, experiance_group):
        animation_move = Animation(["assets/enemies/blockfodder/base.png"], (32*SCALE_FACOTOR, 32*SCALE_FACOTOR), [1])
        animation_hurt = Animation(["assets/enemies/blockfodder/hurt.png"], (32*SCALE_FACOTOR, 32*SCALE_FACOTOR), [1])

        super(BlockFodder, self).__init__(pos, (animation_move, animation_hurt), (32*SCALE_FACOTOR, 32*SCALE_FACOTOR), experiance_group)
        # ---------------------- ITEM HOLDER ATTRIBUTES -------------------

        # slightly random speed
        self.speed = self.max_speed = random.uniform(self.speed, self.speed+3)  

        # attack
        self.damage = self.max_damage = 1

        # health and armour
        self.health = self.max_health = 6
        self.armour = self.max_armour = 2

        # -----------------------------------------------------------------