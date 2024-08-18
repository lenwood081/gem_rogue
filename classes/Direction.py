import math

class Direction():
    def __init__(self, dir):
        """
        follows unit circle conventions
        right is 0 
        up 90
        left 180
        down 270
        """
        self.dir = dir

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

