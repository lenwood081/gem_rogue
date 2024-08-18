import math
import pygame

class Direction():
    def __init__(self, dir):
        """
        up is 90
        right is 0
        left is -180 or 180
        down is -90
        angle is in radians
        """
        self.dir = dir

    @staticmethod
    def rotate(start, target, object):
        angle = target - start

        object = pygame.transform.rotate(object, math.degrees(angle))
        return object

    def normal(self):
        while self.dir < -180:
            self.dir += math.pi*2
        while self.dir > 180:
            self.dir -= math.pi*2


