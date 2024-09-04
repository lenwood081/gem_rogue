import pygame
from config import *
from utility.Point import Point
from Background.TileMap import TileMap

# changed this to tiles (scaled by 2.5)

# achived code

"""
class Background:
    def __init__(self, collisions_group):
        # ------------------------------- tiles for background (visual and trodden on) -------------------------------
        tile_dimensions = (64*SCALE_FACOTOR, 64*SCALE_FACOTOR)
        
        # main area tile map
        x_dim = (int)(BG_WIDTH // tile_dimensions[0] + 1)
        y_dim = (int)(BG_HEIGHT //tile_dimensions[1] + 1)

        # tilemap
        self.base_tiles = TileMap([[0 for i in range(y_dim)] for i in range(x_dim)], ["assets/background/background_cobble_tile1.png"], Point(0, 0))

        # ------------------------------ tiles for collisions --------------------------------------

        # construct array of boundary tiles
        boundary = [[0 if j == 0 or i == 0 or j == y_dim+1 or i == x_dim+1 else -1 for j in range(y_dim + 2)] for i in range(x_dim + 2)]
        #boundary[5][5] = 0
        self.boundary_tiles = TileMap(boundary, ["assets/background/boundary_box.png"], Point(-tile_dimensions[0], tile_dimensions[1]))
        self.boundary_tiles.add_collisions(collisions_group)

        # for effects
        self.surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surf.fill((50, 50, 50))
        self.surf2 = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surf2.fill(BG_OVERLAY_SHADE)

    def update(self, cam_offset):
        self.boundary_tiles.update(cam_offset)

    def draw(self, screen, cam_offset):
        # blit tiles 
        self.base_tiles.draw(screen, cam_offset)
        self.boundary_tiles.draw(screen, cam_offset)

        # makes it dark
        screen.blit(self.surf, (0,0), special_flags=pygame.BLEND_RGBA_SUB)


    def draw_after(self, screen, cam_offset):
        screen.blit(self.surf, (0,0), special_flags=pygame.BLEND_RGBA_SUB)
        pass
"""