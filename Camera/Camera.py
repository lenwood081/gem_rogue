from classes.Point import Point
from config import *

# Camera position is the offset of the player and the screen

class Camera:
    def __init__(self, player_pos):
        
        # offeset
        self.offset = Point(0, 0)
        self.update(player_pos)

    # update camera
    def update(self, player_pos):
        # offset reletive to middle of character
        self.offset.x = SCREEN_WIDTH // 2 - player_pos.x
        self.offset.y = SCREEN_HEIGHT // 2 + player_pos.y
        #print(self.offset.x, self.offset.y)

    def get_offset(self):
        new_offset = self.offset.copy()
        return new_offset

