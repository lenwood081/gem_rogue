import pygame
from Background.Tile import Door, Tile
from Background.TileMap import TileMap, DoorMap
from config import SCALE_FACOTOR, INTERACT_KEY
from utility.Point import Point
from Background.Activator import DistActivator, KeyActivator
import math

class Path:
    def __init__(self, start, end, orientation, reverse, collisions:pygame.sprite.Group, activators:pygame.sprite.Group, players:pygame.sprite.Group):
        # same as in stage (0 for not axis or reletive to starting stage
        self.start_orientation = orientation

        # boundry group
        self.players = players
        self.boundry = collisions
        self.path_grid = []
        self.border_grid = []

        # doors
        self.entry_door =  pygame.sprite.Group()
        self.exit_door = pygame.sprite.Group()

        self.start_point = start.copy()
        self.end_point = end.copy()
        self.none_group = pygame.sprite.Group()
        
        self.width = 0
        self.height = 0
        self.path_width = 6
        
        # visual 
        self.tile_dimensions = (32*SCALE_FACOTOR, 32*SCALE_FACOTOR)
        
        self.create_path(self.path_width, start, end)

        # base tiles
        pos = Point(start.x - self.start_orientation[1]*self.tile_dimensions[0]*(self.path_width)//2,
                    start.y + self.start_orientation[0]*self.tile_dimensions[1]*(self.path_width)//2)

        # create doors
        entry_door = [[0 for j in range((int)(1+self.start_orientation[0]*self.path_width))] for i in range((int)(1+self.start_orientation[1]*self.path_width))]

        # remove edges
        if self.start_orientation[0]:
            entry_door[0][0] = -1
            entry_door[0][(int)(self.path_width)] = -1
        elif self.start_orientation[1]:
            entry_door[0][0] = -1
            entry_door[(int)(self.path_width)][0] = -1

        self.entry_door_tiles = DoorMap(entry_door, ["assets/background/boundary_box_blue.png"], pos, self.none_group, Door)
        self.entry_door_tiles.add_collisions(self.boundry)
        self.entry_door_tiles.add_pass_group(self.players)

        # ----------------------------------------------------------------- door activors (entry) ---------------------------------------------
        # center activator
        self.entry_open = KeyActivator(1, 1, start, INTERACT_KEY, 0)
        activators.add(self.entry_open)

        close_pos = Point(start.x + self.start_orientation[0]*self.tile_dimensions[0] + self.start_orientation[0]*50*SCALE_FACOTOR, start.y - self.start_orientation[1]*self.tile_dimensions[1] - self.start_orientation[1]*50*SCALE_FACOTOR)
        if reverse:
            close_pos = Point(start.x - self.start_orientation[0]*self.tile_dimensions[0] - self.start_orientation[0]*50*SCALE_FACOTOR, start.y + self.start_orientation[1]*self.tile_dimensions[1] + self.start_orientation[1]*50*SCALE_FACOTOR)
        self.entry_close = DistActivator(1, 1, close_pos, 30, 0)
        activators.add(self.entry_close)
        for player in players:
            self.entry_close.add_sprites(player)
            self.entry_open.add_sprites(player)

        # checks whether to render in reverse essentually
        if reverse:
            pos = Point(start.x - self.width*self.start_orientation[0]*self.tile_dimensions[0] - self.start_orientation[1]*self.tile_dimensions[0]*(self.path_width)//2, 
                        start.y + self.height*self.start_orientation[1]*self.tile_dimensions[1] + self.start_orientation[0]*self.tile_dimensions[1]*(self.path_width)//2)
        self.base_tiles = TileMap(self.path_grid, ["assets/background/background_cobble_tile1.png"], pos, self.none_group, Tile)

        # add border tiles
        self.border_tiles =  TileMap(self.border_grid, ["assets/background/boundary_box.png"], pos, self.none_group, Tile)
        self.border_tiles.add_collisions(self.boundry)

    # tunnel in direction
    def create_path(self,  path_width, start, end):
        # create base grid
        self.height = (int)(self.start_orientation[1] * (math.fabs(end.y - start.y)//self.tile_dimensions[1]) + self.start_orientation[0] * path_width)
        self.width = (int)(self.start_orientation[0] * (math.fabs(end.x - start.x)//self.tile_dimensions[0]) + self.start_orientation[1] * path_width) 

        # create grid
        self.path_grid = [[0 if 0 < j < self.height and 0 < i < self.width else -1 for j in range(self.height)] for i in range(self.width)]

        # create border_grid
        # y direction
        if self.start_orientation[0]:
            self.border_grid = [[0 if j == 0 or j == self.height else -1 for j in range(self.height+1)] for i in range(self.width+1)]
        # x direction
        if self.start_orientation[1]:
            self.border_grid = [[0 if i == 0 or i == self.width else -1 for j in range(self.height+1)] for i in range(self.width+1)]

    def draw(self, screen, cam_offset):
        # blit stage_tiles 
        self.base_tiles.draw(screen, cam_offset)
        self.border_tiles.draw(screen, cam_offset)
        self.entry_door_tiles.draw(screen, cam_offset)        
    
    def update(self, cam_offset, dt):
        self.base_tiles.update(cam_offset, dt)
        self.border_tiles.update(cam_offset, dt)

        # check if activator is open (if front is active open door, if back is active close door)
        if self.entry_open.active and not self.entry_close.active:
            self.entry_door_tiles.open_doors()
        else:
            self.entry_door_tiles.close_doors()
        self.entry_door_tiles.update(cam_offset, dt)
       
    
    
        

    
