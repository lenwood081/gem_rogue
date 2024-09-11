from turtle import width
import pygame
from Background.TileMap import TileMap
from config import SCALE_FACOTOR
from utility.Point import Point
import math

# TODO impliment doors

class Path:
    def __init__(self, start, end, orientation, reverse,end_stage):
        # stage to end at
        destination_stage = end_stage

        # same as in stage (0 for not axis or 1) reletive to starting stage
        self.start_orientation = orientation
                
        self.start_point = start.copy()
        self.end_point = end.copy()
        self.none_group = pygame.sprite.Group()
        
        self.width = 0
        self.height = 0
        self.path_width = 4
        
        # visual 
        self.tile_dimensions = (32*SCALE_FACOTOR, 32*SCALE_FACOTOR)
        
        self.create_path(self.path_width, start, end)

        # base tiles
        # TODO start pos needs to be changed
        pos = Point(start.x + self.start_orientation[0]*self.tile_dimensions[0]/2
                    - self.start_orientation[1]*self.tile_dimensions[0]*(self.path_width)//2,
                    start.y - self.start_orientation[1]*self.tile_dimensions[1]/2
                    + self.start_orientation[0]*self.tile_dimensions[1]*(self.path_width)//2)
        if reverse:
            pos = Point(start.x - self.width*self.start_orientation[0]*self.tile_dimensions[0] 
                        - self.start_orientation[0]*(self.tile_dimensions[0] + self.tile_dimensions[0]/2)
                         - self.start_orientation[1]*self.tile_dimensions[0]*(self.path_width)//2, 
                        start.y + self.height*self.start_orientation[1]*self.tile_dimensions[1] 
                        + self.start_orientation[1]*(self.tile_dimensions[1]+ self.tile_dimensions[1]/2)
                         + self.start_orientation[0]*self.tile_dimensions[1]*(self.path_width)//2)
        self.base_tiles = TileMap(self.path_grid, ["assets/background/background_cobble_tile1.png"], pos, self.none_group)
        
    # tunnel in direction
    def create_path(self,  path_width, start, end):
        # create base grid
        self.height = (int)(self.start_orientation[1] * (math.fabs(end.y - start.y)//self.tile_dimensions[1]) + self.start_orientation[0] * path_width)
        self.width = (int)(self.start_orientation[0] * (math.fabs(end.x - start.x)//self.tile_dimensions[0]) + self.start_orientation[1] * path_width)

        self.path_grid = [[0 if 0 < j < self.height and 0 < i < self.width else -1 for j in range(self.height+1)] for i in range(self.width+1)]
        
    def draw(self, screen, cam_offset):
        # blit stage_tiles 
        self.base_tiles.draw(screen, cam_offset)
        
    
    def update(self, cam_offset, dt):
        self.base_tiles.update(cam_offset, dt)
        
       
    
    
        

    
