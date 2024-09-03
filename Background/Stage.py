import pygame
from config import *
from utility.Point import Point
from Background.TileMap import TileMap
from Directors.Enemy_Director_Continous import Enemy_Director_Continous
from Directors.Enemy_Director_Instant import Enemy_Director_Instant 


class Stage:
    def __init__(self, collisions_group, particles_group, enemy_group, experiance_group, projectile_group, player_group, cam_offset, diff_coeff):
        # groups
        self.enemies = enemy_group
        self.experiance = experiance_group
        self.projectiles = projectile_group
        self.collisions = collisions_group
        self.particles = particles_group
        self.players = player_group

        # ------------------------------- tiles for background (visual and trodden on) -------------------------------
        tile_dimensions = (64*SCALE_FACOTOR, 64*SCALE_FACOTOR)

        # main area tile map
        x_dim = (int)(BG_WIDTH // tile_dimensions[0] + 1)
        y_dim = (int)(BG_HEIGHT //tile_dimensions[1] + 1)

        # tilemap
        self.base_tiles = TileMap([[0 for i in range(y_dim)] for i in range(x_dim)], ["assets/background/background_cobble_tile1.png"], Point(0, 0), enemy_group)

        # ------------------------------ tiles for collisions --------------------------------------

        # construct array of boundary tiles
        boundary = [[0 if j == 0 or i == 0 or j == y_dim+1 or i == x_dim+1 else -1 for j in range(y_dim + 2)] for i in range(x_dim + 2)]
        #boundary[5][5] = 0
        self.boundary_tiles = TileMap(boundary, ["assets/background/boundary_box.png"], Point(-tile_dimensions[0], tile_dimensions[1]), enemy_group)
        self.boundary_tiles.add_collisions(collisions_group)

        # ------------------------------------ enemey directors -----------------------------------------

        # spawn only on tilemap tiles where spawnable = True

        instant_director = Enemy_Director_Instant(150, self.enemies, self.experiance, self.projectiles, self.particles, self.players, self.base_tiles, cam_offset)
        fast_director = Enemy_Director_Continous(self.enemies, 5, self.experiance, self.projectiles, self.particles, self.players, self.base_tiles, cam_offset)

        instant_director.activate(diff_coeff)
 

    # update
    def update(self, cam_offset, dt):
        # update boundary tiles
        self.boundary_tiles.update(cam_offset, dt)
        
        # update enemy spawners 
        self.base_tiles.update(cam_offset, dt)

        pass

    def draw(self, screen, cam_offset):
        # blit stage_tiles 
        self.base_tiles.draw(screen, cam_offset)
        self.boundary_tiles.draw(screen, cam_offset)



    def draw_after(self, screen):
        pass