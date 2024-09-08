import pygame
from Background.TileMap import TileMap
from Background.Stage import Stage
from config import SCALE_FACOTOR
from utility.Point import Point

class Path:
    def __init__(self, start, end, orientation):
        self.start_point = start.copy()
        self.end_point = end.copy()
        self.none_group = pygame.sprite.Group()
        
        # same as in stage (-1 for not that axis, 0 for left or top 1 for right or bottom) reletive to starting stage
        self.start_orientation = orientation
                
        # visual 
        self.tile_dimensions = (32*SCALE_FACOTOR, 32*SCALE_FACOTOR)
        
        self.create_path(30, 3, 1920, 1080)
        self.base_tiles = TileMap(self.path_grid, ["assets/background/simple_tile_1.png"], self.start_point, self.none_group)

        
    # tunnel in direction
    def create_path(self, length, width, x, y):
        self.path_grid = [[0 if 0 < j < width and 0 < i < length else -1 for j in range(width+1)] for i in range(length+1)]
        
    def draw(self, screen, cam_offset):
        # blit stage_tiles 
        self.base_tiles.draw(screen, cam_offset)
        
    
    def update(self, cam_offset, dt):
        self.base_tiles.update(cam_offset, dt)
        
       
    
    
        

    
