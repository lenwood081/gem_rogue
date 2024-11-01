import math
from utility.Direction import Direction

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
        if magnitude == 0:
            move_dir.x = 0
            move_dir.y = 0
            return move_dir
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
    
    # rotate a unit vector by radians 
    @staticmethod
    def rotate_unit_vector(unit_vector, angle):
        x = (unit_vector.x*math.cos(angle) - unit_vector.y*math.sin(angle))
        y = (unit_vector.x*math.sin(angle) + unit_vector.y*math.cos(angle))
        return Point(x, y)
    
    # rotate a unit vector by radians with flip
    @staticmethod
    def rotate_unit_vector_flip(unit_vector, angle, dir):
        if dir < -math.pi/2 or dir > math.pi/2:
            angle = -angle
        return Point.rotate_unit_vector(unit_vector, angle)
    
    # calculate ecuclidian distance
    @staticmethod
    def euclidian_dist(pos1, pos2):
        return math.sqrt((pos1.x - pos2.x)**2 + (pos1.y - pos2.y)**2)
    
    # duplicates with new reference
    def copy(self):
        new_point = Point(self.x, self.y)
        return new_point