import math
from classes.Direction import Direction

# makes easier to control position
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, x_increase, y_increase):
        self.x += x_increase
        self.y += y_increase

    @staticmethod
    def unit_vector(pos1, pos2):
        move_dir = Point(0,0)

        # vector between two points
        x = pos1.x - pos2.x
        y = pos1.y - pos2.y

        # make unit vector
        magnitude = math.sqrt(x*x+y*y)
        move_dir.x = x/magnitude
        move_dir.y = y/magnitude
        
        return move_dir
    
    @staticmethod
    def direction_to_point(pos1, pos2):
        direction = Direction(0.0)
        x=pos1.x-pos2.x
        y=pos1.y-pos2.y
        angle = math.atan2(y, x)
        direction.dir = angle
        return direction