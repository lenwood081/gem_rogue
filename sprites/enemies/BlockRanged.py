import math
from sprites.Enemy import Enemy
from classes.Point import Point
from sprites.weapons.Guns.NodeBlaster import NodeBlaster
from Animations.Animation import Animation
from config import *

"""
will create a distance and shoot, should puase when shooting
"""

class BlockRanged(Enemy):
    def __init__(self, pos, experiance_group): 
        animation_move = Animation(["assets/enemies/BlockRanged/BlockRanged.png"], (40, 40), [1])
        animation_hurt = Animation(["assets/enemies/BlockRanged/BlockRanged_hurt.png"], (40, 40), [1])

        super(BlockRanged, self).__init__(pos, (animation_move, animation_hurt), (40, 40), experiance_group)
        # ---------------------- ITEM HOLDER ATTRIBUTES -------------------

        # slightly random speed
        self.speed = self.max_speed = 4  

        # attack
        self.damage = self.max_damage = 1

        # health and armour
        self.health = self.max_health = 4

        # -----------------------------------------------------------------

        self.lock_on_dist = 500
        self.too_close = 200
        # should target the one place
        self.VARIATION = 0

        # circle direction should change every 5 secounds
        self.circle_dir_clockwise = 1
        self.circle_timer = FRAMERATE * 5
        self.circle_timer_current = 0
        self.stutter_tolerance = 20

        # add gun
        self.weapons.add(NodeBlaster(self.pos, Point(0, 0)))

    # move method override
    def move(self, unit_vector):
        # if too close move away
        if self.dist_player < self.too_close:
            self.pos.x -= self.speed * unit_vector.x
            self.pos.y -= self.speed * unit_vector.y
            self.fire = True
            return

        # if too far away move directly towards player
        if self.dist_player > self.lock_on_dist:
            self.pos.x += self.speed * unit_vector.x
            self.pos.y += self.speed * unit_vector.y
            self.fire = False
            return
        
        self.fire = True
        
        # otherwise circle
        new_unit_vector = Point.rotate_unit_vector(unit_vector, self.circle_dir_clockwise * math.pi/2)

        # if too close to either edge to prevent stuttering
        if self.dist_player < self.too_close + self.stutter_tolerance:
            self.pos.x -= self.speed * unit_vector.x
            self.pos.y -= self.speed * unit_vector.y
        elif self.dist_player > self.lock_on_dist - self.stutter_tolerance:
            self.pos.x += self.speed * unit_vector.x
            self.pos.y += self.speed * unit_vector.y

        self.pos.x += self.speed * new_unit_vector.x
        self.pos.y += self.speed * new_unit_vector.y

        # after set time flip rotation
        if self.circle_timer_current >= self.circle_timer:
            self.circle_timer_current = 0
            self.circle_dir_clockwise *= -1

        self.circle_timer_current += 1

    # override to make detcetion better for ranged units
    def check_boundarys(self):
        hit = super().check_boundarys()

        if hit:
            # flip turning direction
            self.circle_timer_current = 0
            self.circle_dir_clockwise *= -1

