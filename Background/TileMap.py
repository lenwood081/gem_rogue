import pygame
import numpy
from Background.Tile import Tile
from config import *
from utility.Point import Point

class TileMap:
    # for purely visual
    def __init__(self, index_array, tile_types, pos):
        assert(len(tile_types) > 0)
        # topleft
        self.pos = pos.copy()

        # height width
        temp_tile = Tile(Point(0,0), tile_types[0])
        self.width = temp_tile.width
        self.height = temp_tile.height

        # tile array
        self.tile_array = numpy.array([[Tile(Point(i * self.width + self.pos.x, j * -self.height + self.pos.y), tile_types[index_array[i][j]]) if index_array[i][j] >= 0 else 0 for j in range(len(index_array[i]))] for i in range(len(index_array))])

    # make shoot though
    def shoot_through(self, x, y, bool):
        if isinstance(self.tile_array[x][y], Tile):
            self.tile_array[x][y].shoot_through = bool
    
    # add to collisions
    def add_collisions(self, collision_group):
        # add tiles to collision group
        for tile_column in self.tile_array:
            for tile in tile_column:
                # checks not
                if isinstance(tile , Tile):
                    collision_group.add(tile)

    # draws tileset to screen
    def draw(self, screen, cam_offset):
        # blit tiles only when needed to 
        x = self.pos.x
        y = -self.pos.y
        for tile_column in self.tile_array:
            # check if on screen
            if x + self.width + cam_offset.x >= 0 and x + cam_offset.x <= SCREEN_WIDTH:
                    y = -self.pos.y
                    for tile in tile_column:
                        if y + self.height + cam_offset.y >= 0 and y + cam_offset.y <= SCREEN_HEIGHT:
                            # checks is a tile
                            if isinstance(tile, Tile):
                                tile.draw(screen, cam_offset)
                        y += self.height
            x += self.width

    # for boundary boes so that the rect is always updated
    def update(self, cam_offset):
        for tile_column in self.tile_array:
            for tile in tile_column:
                # checks not
                if isinstance(tile , Tile):
                    tile.update(cam_offset)

