import pygame
import numpy
from Background.Tile import Door, Tile
from config import *
from utility.Point import Point

class TileMap:
    # for purely visual
    def __init__(self, index_array, tile_types, pos, enemy_group, tile_type=Tile):
        assert(len(tile_types) > 0)
        # topleft
        self.pos = pos.copy()

        # height width
        temp_tile = Tile(Point(0,0), tile_types[0], enemy_group)
        self.width = temp_tile.width
        self.height = temp_tile.height
        self.tile_type = tile_type

        # tile array
        self.tile_array = numpy.array([[tile_type(Point(i * self.width + self.pos.x, j * -self.height + self.pos.y), tile_types[index_array[i][j]], enemy_group) if index_array[i][j] >= 0 else 0 for j in range(len(index_array[i]))] for i in range(len(index_array))])
        self.length = len(self.tile_array) * len(self.tile_array[0])

    # make shoot though
    def shoot_through(self, x, y, bool):
        tile = self.tile_array[x][y]
        if isinstance(tile, self.tile_type):
            tile.is_shoot_through = bool

    # replace a tile
    def replace_tile(self, x, y, tile):
        # basic bounds check
        assert(0 <= x < len(self.tile_array) and 0 <= y < len(self.tile_array[0]))

        # replace tile
        # change position to match
        tile.pos = Point(x*self.width + self.pos.x, y*-self.height + self.pos.y)
        self.tile_array[x][y] = tile

    # add to collisions
    def add_collisions(self, collision_group):
        # add tiles to collision group
        for tile_column in self.tile_array:
            for tile in tile_column:
                # checks not
                if isinstance(tile , self.tile_type):
                    collision_group.add(tile)

    # draws tileset to screen
    def draw(self, screen, cam_offset):
        # blit tiles only when needed to 
        x = self.pos.x
        y = -self.pos.y
        for tile_column in self.tile_array:
            # check if on screen
            if x + self.width + cam_offset.x >= self.width/2 and x + cam_offset.x <= SCREEN_WIDTH + self.width/2:
                    y = -self.pos.y
                    for tile in tile_column:
                        if y + self.height + cam_offset.y >= self.height/2 and y + cam_offset.y <= SCREEN_HEIGHT + self.height/2:
                            # checks is a tile
                            if isinstance(tile, self.tile_type):
                                tile.draw(screen)
                        y += self.height
            x += self.width

    # for boundary boes so that the rect is always updated
    def update(self, cam_offset, dt):
        for tile_column in self.tile_array:
            for tile in tile_column:
                # checks not
                if isinstance(tile , self.tile_type):
                    tile.update(cam_offset, dt)

    # add pass group to door
    def add_pass_group(self, sprite):
        assert(self.tile_type == Door)

        for tile_row in self.tile_array:
            for tile in tile_row:
                if isinstance(tile, self.tile_type):
                    tile.add_member(sprite)
