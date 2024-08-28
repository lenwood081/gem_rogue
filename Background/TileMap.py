import pygame
import numpy
from Background.Tile import Tile
from config import *
from classes.Point import Point

class TileMap:
    # with collisions
    def __init__(self, index_array, tile_types, collision_group:pygame.sprite.Group):
        assert(len(tile_types) > 0)

        # height width
        temp_tile = Tile(Point(0,0), tile_types[0])
        self.width = temp_tile.width
        self.height = temp_tile.height

        # tile array
        self.tile_array = numpy.array([[Tile(Point(i * self.width, j * self.height) ,tile_types[index_array[i][j]]) if index_array[i][j] >= 0 else 0 for j in range(len(index_array[i]))] for i in range(len(index_array))])

        # add tiles to collision group
        for tile_column in self.tile_array:
            for tile in tile_column:
                # checks not
                if isinstance(tile , Tile):
                    collision_group.add(tile)


    # for purely visual
    def __init__(self, index_array, tile_types):
        assert(len(tile_types) > 0)

        # height width
        temp_tile = Tile(Point(0,0), tile_types[0])
        self.width = temp_tile.width
        self.height = temp_tile.height

        # tile array
        self.tile_array = numpy.array([[Tile(Point(i * self.width, j * -self.height) ,tile_types[index_array[i][j]]) if index_array[i][j] >= 0 else 0 for j in range(len(index_array[i]))] for i in range(len(index_array))])

    
        


    # draws tileset to screen
    def draw(self, screen, cam_offset):
        
        # blit tiles only when needed to 
        x = 0
        y = 0
        for tile_column in self.tile_array:
            # check if on screen
            if x + self.width + cam_offset.x >= 0 and x + cam_offset.x <= SCREEN_WIDTH:
                    y = 0
                    for tile in tile_column:
                        if y + self.height + cam_offset.y >= 0 and y + cam_offset.y <= SCREEN_HEIGHT:
                            # checks is a tile
                            if isinstance(tile, Tile):
                                tile.draw(screen, cam_offset)
                        y += self.height
            x += self.width