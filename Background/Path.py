import pygame
from Background.TileMap import TileMap
from Background.Stage import Stage

class Path:
    def __init__(self, starting_stage:Stage, end_stage:Stage):
        self.start_point = starting_stage.player_start_pos.copy()
        self.end_point = end_stage.player_start_pos.copy()

        pass
        

    
