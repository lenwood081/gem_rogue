import pygame
from classes.Point import Point
from sprites.Weapon import Weapon

class BasicGun(Weapon):
    def __init__(self, x, y):
        self.pos = Point(x, y)
        super(BasicGun, self).__init__(x, y, "assets/player/Basic_gun.png", 70, 100) 

    def update(self, player_dir):
        self.face_target(player_dir)