import math

import pygame
from Background.Path import Path
from Background.Stage import Stage
from utility.Point import Point
from config import SCALE_FACOTOR

class StageManager:
    def __init__(self, collisions_group, activator_group, particles_group, enemy_group:pygame.sprite.Group, experiance_group, projectile_group, player_group, cam_offset):
        # groups
        self.enemies = enemy_group
        self.experiance = experiance_group
        self.projectiles = projectile_group
        self.collisions = collisions_group
        self.activators = activator_group
        self.particles = particles_group
        self.players = player_group
        
        self.tile_dimensions = (32*SCALE_FACOTOR, 32*SCALE_FACOTOR)

        # each list of stages, first means active
        self.active_stage = Stage(self.collisions, self.particles, self.enemies, self.experiance, self.projectiles, self.players, cam_offset, Point(0, 0))
        self.active_stage.iniciate(1)
        self.adjacent_stages = []
        self.stages_to_delete = 0
        
        # a list of paths when a path is picked you add the path to the end of the list
        self.paths_to_delete = 0 # based on the stage being removed
        self.paths = []
        self.active_path:Path= None # type: ignore
        self.active_path_index = -1

        self.add_exit_paths(self.active_stage, cam_offset)

        # enemys will be despawned and a new stage will be generated at the end of the path
        self.in_path = False
        self.new_stage_entered = False
        self.generate_new_stage = False
        
        # when a player enters the new stage the old stage will be derendered as well as the old stages paths
        
        # the player will aslo no longer be able to go back through that path
        
        pass
    
    # update
    def update(self, cam_offset, dt, diff_coeff):
        # stage
        self.active_stage.update(cam_offset, dt, diff_coeff)
        
        for stage in self.adjacent_stages:
           stage.update(cam_offset, dt, diff_coeff)

        for i, path in enumerate(self.paths):
            if path.update(cam_offset, dt):
                if not self.in_path:
                    self.generate_new_stage = True
                self.in_path = True
                self.active_path = path
                self.active_path_index = i
            else:
                if i == self.active_path_index:
                    self.in_path = False
                    self.active_path_index = -1
                    self.new_stage_entered = True



        # manage stage_change
        if self.generate_new_stage:
            self.new_stage(cam_offset)
            self.generate_new_stage = False

        if self.new_stage_entered:
            # self.active_stage.iniciate(diff_coeff)
            # delete unessicary paths and stages
            # first n stages and the last one (previous stage)
            del self.adjacent_stages[:self.stages_to_delete]
            del self.adjacent_stages[-1]
            del self.paths[:self.paths_to_delete]
            self.stages_to_delete = 0
            self.paths_to_delete = 0
            self.new_stage_entered = False

        
    # new stage, 
    def new_stage(self, cam_offset):
        # generate from path
        self.active_stage.clear()
        
        # stages to delete
        self.stages_to_delete = len(self.adjacent_stages)
        # paths to delete
        self.paths_to_delete = len(self.paths)
        self.add_exit_paths(self.active_path.destination_stage, cam_offset)
        self.adjacent_stages.append(self.active_stage)
        self.paths.append(self.active_path)
        self.active_stage = self.active_path.destination_stage

    # draw
    def draw(self, screen, cam_offset):
        
        for stage in self.adjacent_stages:
           stage.draw(screen, cam_offset)
        self.active_stage.draw(screen, cam_offset)
        for path in self.paths:
            path.draw(screen, cam_offset)

    # add paths
    def add_exit_paths(self, stage:Stage, cam_offset) -> None:
        length = 40*self.tile_dimensions[0] # pixels
        paths = stage.paths
        first = True
        for path in paths:
            if first == True:
                first = False
                continue
            length_y = length * min(1+path[0][1], 1) * (1 + -2 * path[0][1])
            length_x = length * min(1+path[0][0], 1) * (1 + -2 * path[0][0])
            position = Point(path[1][0] - length_x , path[1][1] + length_y)
            # determine entry path orientation
            path_orientation = (min(1, math.fabs(length_x)), min(1, math.fabs(length_y)))
            reverse = True
            if path[0][1] == 1 or path[0][0] == 1:
                reverse = False
            
            PATHS = {"top": (-1, 0), "bottom": (-1, 1), "left": (0, -1), "right": (1, -1)}
            new_path = path[0]
            if new_path[0] == 1:
                new_path = (0, -1)
            elif new_path[0] == 0:
                new_path = (1, -1)
            elif new_path[1] == 1:
                new_path = (-1, 0)
            elif new_path[1] == 0:
                new_path = (-1, 1)
                
            path_id = list(PATHS.keys())[list(PATHS.values()).index(new_path)]
            # add new stage
            new_stage = Stage(self.collisions, self.particles, self.enemies, self.experiance, self.projectiles, self.players, cam_offset, position, path_id)
            self.adjacent_stages.append(new_stage)
            # create path
            new_path = Path(Point(path[1][0], path[1][1]), position, path_orientation, reverse, self.collisions, self.activators, self.players, new_stage)
            self.paths.append(new_path)

