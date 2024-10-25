import pygame
import time
import random
from Background.Tile import Tile
from config import *
from utility.Point import Point
from Background.TileMap import TileMap
from Directors.Enemy_Director_Continous import Enemy_Director_Continous
from Directors.Enemy_Director_Instant import Enemy_Director_Instant 
import numpy
import sys
numpy.set_printoptions(threshold=sys.maxsize)


class Stage:
    def __init__(self, collisions_group, particles_group, enemy_group:pygame.sprite.Group, experiance_group, projectile_group, player_group, cam_offset, position, entry_path="right"):
        # if true will remove from group, and be collected as garbage
        self.to_remove = False
        self.draw_pos = position.copy()

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
        self.width = 2000
        self.height = 2000

        # tile_arrays
        self.boundary_array = []
        self.final_array = []

        # player start position
        self.player_start_pos = Point(0, 0)
        self.iniciated = False

        # ------------------------------- tiles for background (visual and trodden on) -------------------------------
        self.tile_dimensions = (32*SCALE_FACOTOR, 32*SCALE_FACOTOR)
        self.num_paths = random.randint(4, 4)
        self.paths = []

        # tilemap
        self.generate_stage(0.7, entry_path)
        self.base_tiles = TileMap(self.final_array, [["assets/background/simple_tile_1.png"]], self.draw_pos, enemy_group, Tile)

        # ------------------------------ tiles for collisions --------------------------------------

        self.boundary_tiles = TileMap(self.boundary_array, [["assets/background/blank_tile.png"]], self.draw_pos, enemy_group, Tile)
        self.boundary_tiles.add_collisions(collisions_group)


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

    # clear enemies
    def clear_sprites(self):
        for enemy in self.enemies:
            enemy.kill()
    
    # kill all enemys 
    def clear(self):
        self.iniciated = False
        self.clear_sprites()

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
        

    def draw(self, screen, cam_offset):
        # blit stage_tiles 
        self.base_tiles.draw(screen, cam_offset)
        self.boundary_tiles.draw(screen, cam_offset)

        # makes it dark
        # screen.blit(self.surf, (0,0), special_flags=pygame.BLEND_RGBA_SUB)

    def draw_after(self, screen):
        screen.blit(self.surf, (0,0), special_flags=pygame.BLEND_RGBA_SUB)
    

    # ----------------------------------------- Tilemap stage generation -------------------------

    def generate_stage(self, percantage_fill, entry_path):
        # percentage_tollerance TODO
        time_check = time.time()
        print("start time", time_check-time.time())

        # calculate number of tiles in each axis
        x_dim = (int)(self.width // self.tile_dimensions[0] + 1)
        y_dim = (int)(self.height // self.tile_dimensions[1] + 1)

        # calculate number of tiles to generate
        number_of_tiles_intitial = (int)(x_dim*y_dim*percantage_fill)
        number_of_tiles = number_of_tiles_intitial
        
        # generate initial grid
        initial_grid = numpy.array([[-1 for i in range(y_dim+4)] for j in range(x_dim+4)])

        
        # ------------------------------------ generation idea one ----------------------------------
    
        # debuging the time sink
        print("after inital grid", time_check-time.time())

        # pick points to start generation
        num_of_points = random.randint(1, 2)
        first = True
        for point in range(num_of_points):
            while True:
                x = random.randint(x_dim//7+1, (x_dim)//2)
                y = random.randint(y_dim//7+1, (y_dim)//2)
                if initial_grid[x][y] == -1:
                    if first:
                        # get center and spawn pos for player
                        # also the section where flood filling occurs
                        self.player_start_pos.move(x*self.tile_dimensions[0]+self.tile_dimensions[0]/2, -(y*self.tile_dimensions[1] + self.tile_dimensions[1]/2))
                        self.center_point = Point(x, y)
                        initial_grid[x][y] = 2 
                        number_of_tiles -= 1
                        first = False
                    else:
                        initial_grid[x][y] = 0 
                    break;

        
        print("after first point generation", time_check-time.time())

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

        print("after first generation", time_check-time.time())

        # pick a point and flood fill anything not connected is discarded
        while incomplete:
            incomplete = False
            for i in range(x_dim+4):
                for j in range(y_dim+4):
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
        
        print("after flood fill", time_check-time.time())
        # -------------------------------------------- method 2 cell automata with flood fill -----------------------------------------
            

        # -------------------------------------------- method 3 faster than method one using consecutive squares -----------------------------------------
        
        # attempt method one, but without needing to flood fill and having a shorter generation time (as these are proved to take the most computation)
        """
        # debuging the time sink
        print("after inital grid", time_check-time.time())

        # pick point to start generation
        x = random.randint(3, x_dim-2)
        y = random.randint(3, y_dim-2)
        first = True
        while number_of_tiles > 0:
            if first:
                # get center and spawn pos for player
                self.player_start_pos.move(x*self.tile_dimensions[0]+self.tile_dimensions[0]/2, -(y*self.tile_dimensions[1] + self.tile_dimensions[1]/2))
                self.center_point = Point(x, y)
                first = False

            number_of_tiles -= 1
            self.threeByThree(initial_grid, x, y, 2)
            x_add = random.randint(-1, 1)
            y_add = random.randint(-1, 1)
            if 1 < x + x_add < x_dim:
                x += x_add
            if 1 < y + y_add < y_dim:
                y += y_add

        # debuging the time sink
        print("after generation", time_check-time.time())
        
        x_start = x = random.randint(3, x_dim-2)
        y_start = y = random.randint(3, y_dim-2)
        x_add = 1
        y_add = 0
        first = True
        while number_of_tiles > 0:
            if first:
                # get center and spawn pos for player
                self.player_start_pos.move(x*self.tile_dimensions[0]+self.tile_dimensions[0]/2, -(y*self.tile_dimensions[1] + self.tile_dimensions[1]/2))
                self.center_point = Point(x, y)
                first = False

            

            initial_grid[x][y] = 2
            number_of_tiles -= 1
            if x_add == 0:
                x = x_start
            if 1 < x + x_add < x_dim:
                x += x_add
            else:
                y_add = 1
                x_add = 0

            if 1 < y + y_add < y_dim:
                y += y_add
                y_add = 0
                
        
        # ----------------------------------------------------------------------------------------------------------------------------
        
        for generating pathways they will connect directly to the center 4 squares and span from them, they will only start generating once 
        there is no more 2's to connect to
        """
        
        # paths is a tuple ((x, y), (x, y), (x, y)...) indicating the direction of entry
        # -1 means not that axis, 0 means left or top, 1 means right or bottom
        
        # print(initial_grid
        PATHS = {"top": (-1, 0), "bottom": (-1, 1), "left": (0, -1), "right": (1, -1)}

            
        # calculate position should be relevtive to the path connection
        path = PATHS[entry_path]


        # entry path will always be to the first
        self.paths.append((PATHS.pop(entry_path), []))
        for i in range(1, self.num_paths):
            temp = PATHS.pop(random.choice(list(PATHS.keys())))
            self.paths.append((temp, []))
            # exit paths need the position as well

        # middle point of the path must align with the center 2
        first = True
        for path in self.paths:
            x = 0
            y = 0
            
            if path[0][0] == -1:
                x = self.center_point.x
                y = path[0][1] * y_dim
            if path[0][1] == -1:
                y = self.center_point.y
                x = path[0][0] * x_dim
                
            # start from outwards and build in
            while True:
                # x axis
                if path[0][1] == -1:
                    increment = 1 - 2 * path[0][0]
                    x += increment
                    # check 
                    if initial_grid[x][y] == 2 or initial_grid[x][y-1] == 2 or initial_grid[x][y+1] == 2:
                        # create doors
                        initial_grid[x-2*increment][y] = -3
                        initial_grid[x-2*increment][y+1] = -3
                        initial_grid[x-2*increment][y-1] = -3
                        initial_grid[x-2*increment][y+2] = -3
                        initial_grid[x-2*increment][y-2] = -3
                        path[1].append(self.draw_pos.x + (x-2*increment)*self.tile_dimensions[0])
                        path[1].append(self.draw_pos.y - (y*self.tile_dimensions[1]))
                        self.threeByThree(initial_grid, x, y, 2)
                        break
                    
                if path[0][0] == -1:
                    increment = 1 - 2 * path[0][1]
                    y += increment
                    # check 
                    if initial_grid[x][y] == 2 or initial_grid[x-1][y] == 2 or initial_grid[x+1][y] == 2:
                        # create doors
                        initial_grid[x][y-2*increment] = -3
                        initial_grid[x-1][y-2*increment] = -3
                        initial_grid[x+1][y-2*increment] = -3
                        initial_grid[x+2][y-2*increment] = -3
                        initial_grid[x-2][y-2*increment] = -3
                        path[1].append(self.draw_pos.x + x*self.tile_dimensions[0])
                        path[1].append(self.draw_pos.y -((y-2*increment)*self.tile_dimensions[1]))
                        self.threeByThree(initial_grid, x, y, 2)
                        break
                    
            if first:
                first = False
                # assigning the position to draw the top left point of the grid, reletive to the entry path
                self.draw_pos = Point(self.draw_pos.x + self.draw_pos.x - self.paths[0][1][0]
                                    ,self.draw_pos.y + self.draw_pos.y - self.paths[0][1][1])
                self.player_start_pos.move(self.draw_pos.x,self.draw_pos.y)
                
        print("after paths", time_check-time.time())
        # ------------------------------------- boundarys --------------------------------------------
        
        for i in range(x_dim+4):
            for j in range(y_dim+4):
                if initial_grid[i][j] == 2:
                    # boundrys will be recorded as -2 in the initial_array


                    # check right 
                    if i+1 <= x_dim+2 and initial_grid[i+1][j] != 2 and initial_grid[i+1][j] != -3:
                        initial_grid[i+1][j] = -2
                    # check left 
                    if i-1 >= 0 and initial_grid[i-1][j] != 2 and initial_grid[i-1][j] != -3:
                        initial_grid[i-1][j] = -2
                    # check down
                    if j+1 <= y_dim+2 and initial_grid[i][j+1] != 2 and initial_grid[i][j+1] != -3:
                        initial_grid[i][j+1] = -2
                    # check up 
                    if j-1 >= 0 and initial_grid[i][j-1] != 2 and initial_grid[i][j-1] != -3:
                        initial_grid[i][j-1] = -2

                    # check diagonal lower right
                    if i+1 <= x_dim+2 and j+1 <= y_dim+2 and initial_grid[i+1][j+1] != 2 and initial_grid[i+1][j+1] != -3:
                        initial_grid[i+1][j+1] = -2
                    # check diagonal lower left
                    if i-1 >= 0 and j+1 <= y_dim+2 and initial_grid[i-1][j+1] != 2 and initial_grid[i-1][j+1] != -3:
                        initial_grid[i-1][j+1] = -2
                    # check diagonal upper right
                    if i+1 <= x_dim+2 and j-1 >= 0 and initial_grid[i+1][j-1] != 2 and initial_grid[i+1][j-1] != -3:
                        initial_grid[i+1][j-1] = -2
                    # check diagonal upper left
                    if i-1 >= 0 and j-1 >= 0 and initial_grid[i-1][j-1] != 2 and initial_grid[i-1][j-1] != -3:
                        initial_grid[i-1][j-1] = -2
                    
        # ----------------------------------------------------------------------------------------------------------------------------

        print("after border", time_check-time.time())

        # recast to 0's and -1
        self.final_array = [[0 if initial_grid[i][j] == 2 else -1 for j in range(y_dim+4)] for i in range(x_dim+4)]
        self.boundary_array = [[0 if initial_grid[i][j] == -2 else -1 for j in range(y_dim+4)] for i in range(x_dim+4)]

        print("complete", time_check-time.time())

    # utility function
    def threeByThree(self, grid, x, y, value) -> int:
        values = 0

        values += grid[x][y] < value
        grid[x][y] = value
        values += grid[x][y-1] < value 
        grid[x][y-1] = value 
        values += grid[x][y+1] < value 
        grid[x][y+1] = value 
        values += grid[x-1][y] < value 
        grid[x-1][y] = value 
        values += grid[x-1][y-1] < value 
        grid[x-1][y-1] = value
        values += grid[x-1][y+1] < value 
        grid[x-1][y+1] = value
        values += grid[x+1][y] < value 
        grid[x+1][y] = value
        values += grid[x+1][y-1] < value 
        grid[x+1][y-1] = value
        values += grid[x+1][y+1] < value 
        grid[x+1][y+1] = value

        return values