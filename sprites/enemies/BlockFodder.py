from config import *
import random
from sprites.enemies.Enemy import Enemy
from Animations.Animation import Animation
from sprites.weapons.Guns.PlasmaGun import PlasmaGun
from Actions.WeaponFire import WeaponFire

"""
this is the main basic enemy in the game, should just move towards the player,
"""

class BlockFodder(Enemy):
    def __init__(self, pos, experiance_group, projectile_group, enemy_group, particle_group, cam_offset):
        animation_move = Animation(["assets/enemies/blockfodder/base.png"], (32*SCALE_FACOTOR, 32*SCALE_FACOTOR), [1])
        animation_hurt = Animation(["assets/enemies/blockfodder/hurt.png"], (32*SCALE_FACOTOR, 32*SCALE_FACOTOR), [1])

        super(BlockFodder, self).__init__(pos, (animation_move, animation_hurt), (32*SCALE_FACOTOR, 32*SCALE_FACOTOR), experiance_group, projectile_group, enemy_group, particle_group, cam_offset)
        # ---------------------- ITEM HOLDER ATTRIBUTES -------------------

        # slightly random speed
        self.speed = self.max_speed = random.randint(400, 600) / FRAMERATE  

        # attack
        self.damage = self.max_damage = 1
        self.can_attack = True

        # health and armou
        self.health = self.max_health = 6
        self.armour = self.max_armour = 2

        # -----------------------------------------------------------------

        