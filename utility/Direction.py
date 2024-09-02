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
    def rotate(target, object):
        new_object = pygame.transform.rotate(object, math.degrees(target))
        return new_object
    
    @staticmethod
    def rotate_with_flip(target, object):
        # flip in x direction
        if target < -math.pi/2 or target > math.pi/2:
            new_object = pygame.transform.flip(object, False, True)
            return pygame.transform.rotate(new_object, math.degrees(target))
        new_object = pygame.transform.rotate(object, math.degrees(target))
        return new_object

    def normal(self):
        while self.dir < -180:
            self.dir += math.pi*2
        while self.dir > 180:
            self.dir -= math.pi*2


