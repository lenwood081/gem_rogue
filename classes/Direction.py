

class Direction():
    def __inti__(self, dir):
        """
        up is 0 degrees
        right 90
        down 180
        left 270
        """
        self.dir = dir

    def normal(self):
        while self.dir < 0:
            self.dir += 360
        while self.dir > 0:
            self.dir -= 360