import math
import pygame

class Direction():
    def __init__(self, dir):
        """
        up is -90
        right is 0
        left is -180 or 180
        down is 90
        """
        self.dir = dir

    @staticmethod
    def rotate(start, target, object):
        angle = target - start

        object = pygame.transform.rotate(object, math.degrees(angle))
        return object

    def normal(self):
        while self.dir < 0:
            self.dir += math.pi*2
        while self.dir > 0:
            self.dir -= math.pi*2

    # find if it is better to increase or decrease to get to desired angle
    # -1 or 1
    def leftOrRight(self, angle):
        temp = self.dir
        if math.fabs(temp - angle) > math.pi:
            # case where it will be easyier to cross over
            if angle > temp:
                return -1
            else:
                return 1

        if angle > temp:
            return 1
        else:
            return -1

