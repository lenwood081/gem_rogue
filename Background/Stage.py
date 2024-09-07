import pygame
import random
from config import *
from utility.Point import Point
from Background.TileMap import TileMap
from Directors.Enemy_Director_Continous import Enemy_Director_Continous
from Directors.Enemy_Director_Instant import Enemy_Director_Instant 
import numpy


class Stage:
    def __init__(self, collisions_group, particles_group, enemy_group, experiance_group, projectile_group, player_group, cam_offset, diff_coeff):
        # if true will remove from group, and be collected as garbage
        self.to_remove = False
         
        # groups
        self.enemies = enemy_group
        self.experiance = experiance_group
        self.projectiles = projectile_group
        self.collisions = collisions_group
        self.particles = particles_group
        self.players = player_group
        
        # death tile group
        self.death_group = pygame.sprite.Group()

        # w, h
        self.width = 0
        self.height = 0

        # tile_arrays
        self.boundary_array = []
        self.final_array = []
        self.death_array = []

        # player start position
        self.center_point = Point(0, 0)
        self.player_start_pos = Point(0, 0)
        self.iniciated = False

        # ------------------------------- tiles for background (visual and trodden on) -------------------------------
        self.tile_dimensions = (32*SCALE_FACOTOR, 32*SCALE_FACOTOR)

        # tilemap
        self.generate_stage(2000, 2000, 0.6)
        self.base_tiles = TileMap(self.final_array, ["assets/background/simple_tile_1.png"], Point(0, 0), enemy_group)

        # ------------------------------ tiles for collisions --------------------------------------


        self.boundary_tiles = TileMap(self.boundary_array, ["assets/background/boundary_box.png"], Point(0, 0), enemy_group)
        self.boundary_tiles.add_collisions(collisions_group)

        #self.death_tiles = TileMap(self.death_array, ["assets/background/background_tile1.png"], Point(0, 0), enemy_group)
        #self.death_tiles.add_collisions(collisions_group)

        # ------------------------------------ enemey directors -----------------------------------------

        # spawn only on tilemap tiles where spawnable = True

        self.instant_director = Enemy_Director_Instant(300, self.enemies, self.experiance, self.projectiles, self.particles, self.players, self.base_tiles, cam_offset)
        self.fast_director = Enemy_Director_Continous(self.enemies, 2, self.experiance, self.projectiles, self.particles, self.players, self.base_tiles, cam_offset)
        self.intermetdiate_director = Enemy_Director_Continous(self.enemies, 9, self.experiance, self.projectiles, self.particles, self.players, self.base_tiles, cam_offset)
        self.slow_director = Enemy_Director_Continous(self.enemies, 20, self.experiance, self.projectiles, self.particles, self.players, self.base_tiles, cam_offset)


        # for effects
        self.surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surf.fill((50, 50, 50))
        self.surf2 = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surf2.fill(BG_OVERLAY_SHADE)

    # start enemy spawning
    def iniciate(self, diff_coeff):
        self.iniciated = True
        self.instant_director.activate(diff_coeff)
    
    # kill all enemys 
    def clear(self):
        self.iniciated = False
        for enemy in self.enemies:
            enemy.kill()

    # delete stage
    def deactivate(self):
        self.to_remove = True
 

    # update
    def update(self, cam_offset, dt, diff_coeff):
        if self.iniciated:
            # update enemy spawners
            self.fast_director.update(diff_coeff, cam_offset, dt)
            self.intermetdiate_director.update(diff_coeff, cam_offset, dt)
            self.slow_director.update(diff_coeff, cam_offset, dt)

        # update boundary tiles
        self.boundary_tiles.update(cam_offset, dt)
        
        # update enemy spawners 
        self.base_tiles.update(cam_offset, dt)
        
        # update death tiles
        #self.death_tiles.update(cam_offset, dt)

        # check if anything is out of bounds and remove them
        """
        for tile in self.death_group:
            for enemy in self.enemies:
                if pygame.Rect.colliderect(tile.rect, enemy.hitbox_rect):
                    enemy.death()
        """

    def draw(self, screen, cam_offset):
        # blit stage_tiles 
        self.base_tiles.draw(screen, cam_offset)
        self.boundary_tiles.draw(screen, cam_offset)
        #self.death_tiles.draw(screen, cam_offset)

        # makes it dark
        screen.blit(self.surf, (0,0), special_flags=pygame.BLEND_RGBA_SUB)

    def draw_after(self, screen):
        screen.blit(self.surf, (0,0), special_flags=pygame.BLEND_RGBA_SUB)
    

    # ----------------------------------------- Tilemap stage generation -------------------------

    # paths is a tuple ((x, y), (x, y), (x, y)...) indicating the direction of entry
    def generate_stage(self, width, height, percantage_fill, paths):
        # percentage_tollerance TODO

        # decide on a random weight and width
        self.width = random.randint(width-width//2, width+width//2)
        self.height = random.randint(height-height//2, height+height//2)

        # calculate number of tiles in each axis
        x_dim = (int)(self.width // self.tile_dimensions[0] + 1)
        y_dim = (int)(self.height // self.tile_dimensions[1] + 1)

        # calculate number of tiles to generate
        number_of_tiles_intitial = (int)(x_dim*y_dim*percantage_fill)
        number_of_tiles = number_of_tiles_intitial
        
        # generate initial grid
        initial_grid = numpy.array([[-1 for i in range(y_dim+4)] for j in range(x_dim+4)])

        
        # ------------------------------------ generation idea one ----------------------------------

        # pick points to start generation
        num_of_points = random.randint(2, 4)
        first = True
        for point in range(num_of_points):
            while True:
                x = random.randint(x_dim//6, (x_dim)//2)
                y = random.randint(x_dim//6, (y_dim)//2)
                if initial_grid[x][y] == -1:
                    if first:
                        # get center and spawn pos for player
                        # also the section where flood filling occurs
                        self.player_start_pos.move(x*self.tile_dimensions[0]+self.tile_dimensions[0]/2, -(y*self.tile_dimensions[1] + self.tile_dimensions[1]/2))
                        self.center_point = Point(x, y)
                        initial_grid[x][y] = 2 
                        initial_grid[x][y-1] = 2 
                        initial_grid[x][y+1] = 2 
                        initial_grid[x-1][y] = 2 
                        initial_grid[x-1][y-1] = 2 
                        initial_grid[x-1][y+1] = 2 
                        initial_grid[x+1][y] = 2 
                        initial_grid[x+1][y-1] = 2 
                        initial_grid[x+1][y+1] = 2 
                        number_of_tiles -= 1
                        first = False
                    else:
                        initial_grid[x][y] = 0 
                        initial_grid[x][y-1] = 0 
                        initial_grid[x][y+1] = 0 
                        initial_grid[x-1][y] = 0 
                        initial_grid[x-1][y-1] = 0 
                        initial_grid[x-1][y+1] = 0 
                        initial_grid[x+1][y] = 0 
                        initial_grid[x+1][y-1] = 0 
                        initial_grid[x+1][y+1] = 0
                    break;

        # generate from those points
        while number_of_tiles > 0:
            # very costly 
            for i in range(2, x_dim):
                for j in range(2, y_dim):
                    if initial_grid[i][j] >= 1:
                        # check right 
                        if i+1 <= x_dim-1 and initial_grid[i+1][j] == -1:
                            initial_grid[i+1][j] = 0
                        # check left 
                        if i-1 >= 0 and initial_grid[i-1][j] == -1:
                            initial_grid[i-1][j] = 0
                        # check right 
                        if j+1 <= y_dim-1 and initial_grid[i][j+1] == -1:
                            initial_grid[i][j+1] = 0
                        # check right 
                        if j-1 >= 0 and initial_grid[i][j-1] == -1:
                            initial_grid[i][j-1] = 0
                    
                    if initial_grid[i][j] == 0:
                        if number_of_tiles > 0:
                            initial_grid[i][j] = 1
                            number_of_tiles -= 1

        # connected platforms
        num_of_points_found = 0
        incomplete = True

        # pick a point and flood fill anything not connected is discarded
        while incomplete:
            incomplete = False
            for i in range(2, x_dim):
                for j in range(2, y_dim):
                    if initial_grid[i][j] == 2:
                        
                        # ------------------------------------------ noraml --------------------------------------

                        # check right 
                        if i+1 <= x_dim-1 and initial_grid[i+1][j] == 1:
                            initial_grid[i+1][j] = 2
                            num_of_points_found += 1
                            incomplete = True
                        # check left 
                        if i-1 >= 0 and initial_grid[i-1][j] == 1:
                            initial_grid[i-1][j] = 2
                            num_of_points_found += 1
                            incomplete = True
                        # check down
                        if j+1 <= y_dim-1 and initial_grid[i][j+1] == 1:
                            initial_grid[i][j+1] = 2
                            num_of_points_found += 1
                            incomplete = True
                        # check up
                        if j-1 >= 0 and initial_grid[i][j-1] == 1:
                            initial_grid[i][j-1] = 2
                            num_of_points_found += 1
                            incomplete = True

        # -------------------------------------------- method 2 cell automata with flood fill -----------------------------------------


        # -------------------------------------------- method 3 super tiles, with bridgeing -----------------------------------------

        
        # ----------------------------------------------------------------------------------------------------------------------------
        """
        for generating pathways they will connect directly to the center 4 squares and span from them, they will only start generating once 
        there is no more 2's to connect to
        """
        
        # middle point of the path must align with the center 2
        for path in paths:
            x = self.center_point.x
            y = self.center_point.y
            while True:
                # x axis
                if path[1] == 0:
                    x += path[0]
                    # check 
                
        
        
        # ------------------------------------- boundarys --------------------------------------------
        
        for i in range(x_dim+4):
            for j in range(y_dim+4):
                if initial_grid[i][j] == 2:
                    # boundrys will be recorded as -2 in the initial_array


                    # check right 
                    if i+1 <= x_dim+2 and initial_grid[i+1][j] != 2:
                        initial_grid[i+1][j] = -2
                    # check left 
                    if i-1 >= 0 and initial_grid[i-1][j] != 2:
                        initial_grid[i-1][j] = -2
                    # check down
                    if j+1 <= y_dim+2 and initial_grid[i][j+1] != 2:
                        initial_grid[i][j+1] = -2
                    # check up 
                    if j-1 >= 0 and initial_grid[i][j-1] != 2:
                        initial_grid[i][j-1] = -2

                    # check diagonal lower right
                    if i+1 <= x_dim+2 and j+1 <= y_dim+2 and initial_grid[i+1][j+1] != 2:
                        initial_grid[i+1][j+1] = -2
                    # check diagonal lower left
                    if i-1 >= 0 and j+1 <= y_dim+2 and initial_grid[i-1][j+1] != 2:
                        initial_grid[i-1][j+1] = -2
                    # check diagonal upper right
                    if i+1 <= x_dim+2 and j-1 >= 0 and initial_grid[i+1][j-1] != 2:
                        initial_grid[i+1][j-1] = -2
                    # check diagonal upper left
                    if i-1 >= 0 and j-1 >= 0 and initial_grid[i-1][j-1] != 2:
                        initial_grid[i-1][j-1] = -2
                    

                        

        
        

        # ----------------------------------------------------------------------------------------------------------------------------

        # recast to 0's and -1
        self.final_array = [[0 if initial_grid[i][j] == 2 else -1 for j in range(y_dim+4)] for i in range(x_dim+4)]
        self.boundary_array = [[0 if initial_grid[i][j] == -2 else -1 for j in range(y_dim+4)] for i in range(x_dim+4)]
        #self.death_array = [[0 if self.final_array[i][j] == -1 and self.boundary_array[i][j] == -1 else -1 for j in range(y_dim+4)] for i in range(x_dim+4)]

