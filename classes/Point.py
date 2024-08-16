# makes easier to control position
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, x_increase, y_increase):
        self.x += x_increase
        self.y += y_increase
        