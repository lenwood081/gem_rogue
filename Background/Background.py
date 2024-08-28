import pygame
from config import *
from classes.Point import Point
from Background.TileMap import TileMap

# change this to tiles (scaled by 2.5)

class Background():
    def __init__(self):
        # tiles
        self.tile_dimensions = (64*SCALE_FACOTOR, 64*SCALE_FACOTOR)
        self.tile_dimensions_overlay = (256*SCALE_FACOTOR, 256*SCALE_FACOTOR)
        self.tile_image = pygame.transform.scale(pygame.image.load("assets/background/background_tile1.png").convert_alpha(), self.tile_dimensions)
        self.overlay = pygame.transform.scale(pygame.image.load("assets/background/ash_overlay.png").convert_alpha(), self.tile_dimensions_overlay)
        self.ovelay_count = self.ovelay_max_count = self.tile_dimensions_overlay[0]

        

        x_dim = (int)(BG_WIDTH // self.tile_dimensions[0] + 1)
        y_dim = (int)(BG_HEIGHT // self.tile_dimensions[1] + 1)
        x_dim_o = (int)(BG_WIDTH // self.tile_dimensions_overlay[0] + 1)
        y_dim_o = (int)(BG_HEIGHT // self.tile_dimensions_overlay[1] + 1)

        # create a 2d array of tiles
        self.tiles = [[0 for i in range(y_dim)] for i in range(x_dim)]
        self.tiles_ash = [[self.overlay for i in range(y_dim_o)] for i in range(x_dim_o)]

        # tilemap
        self.base_tiles = TileMap(self.tiles, ["assets/background/background_tile1.png"])

        self.image = pygame.transform.scale(pygame.image.load("assets/background/pebble-rock-ground.png").convert_alpha(), (BG_WIDTH, BG_HEIGHT))
        self.rect = self.image.get_rect()

        # for effects
        self.surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surf.fill(BG_HORROR_SHADE)
        self.surf2 = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surf2.fill(BG_OVERLAY_SHADE)

        # for determining position of background 
        self.location = Point(BG_WIDTH, -BG_HEIGHT)

    def draw(self, screen, cam_offset):
        # blit tiles 
        self.base_tiles.draw(screen, cam_offset)

        #screen.blit(self.image, (cam_offset.x, cam_offset.y))
        #screen.blit(self.surf, (0,0), special_flags=pygame.BLEND_RGBA_SUB)


    def draw_after(self, screen, cam_offset):
        screen.blit(self.surf, (0,0), special_flags=pygame.BLEND_RGBA_SUB)
        # blit ovelay
        """x = self.ovelay_count
        y = self.ovelay_count
        for tile_column in self.tiles_ash:
            # check if on screen
            if x + self.tile_dimensions_overlay[0] + cam_offset.x >= -self.ovelay_count and x + cam_offset.x <= SCREEN_WIDTH:
                y = self.ovelay_count
                for tile in tile_column:
                    if y + self.tile_dimensions_overlay[1] + cam_offset.y >= -self.ovelay_count and y + cam_offset.y <= SCREEN_HEIGHT:
                        print("bliting")
                        screen.blit(tile, (cam_offset.x + x, cam_offset.y + y))
                    y += self.tile_dimensions_overlay[1]
            x += self.tile_dimensions_overlay[0]

        self.ovelay_count += 0.5
        if self.ovelay_count >= self.ovelay_max_count:
            self.ovelay_count = 0"""
        