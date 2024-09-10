import math
from Background.Path import Path
from Background.Stage import Stage
from utility.Point import Point

class StageManager:
    def __init__(self, collisions_group, particles_group, enemy_group, experiance_group, projectile_group, player_group, cam_offset):
        # groups
        self.enemies = enemy_group
        self.experiance = experiance_group
        self.projectiles = projectile_group
        self.collisions = collisions_group
        self.particles = particles_group
        self.players = player_group

        # each list of stages, first means active
        self.active_stage = Stage(self.collisions, self.particles, self.enemies, self.experiance, self.projectiles, self.players, cam_offset, Point(0, 0))
        self.adjacent_stages = []
        
        # a list of paths when a path is picked you add the path to the end of the list
        self.paths_to_remove = 0 # based on the stage being removed
        self.paths = []

        self.add_exit_paths(self.active_stage, cam_offset)
        
        # a stage must be gnerated with a enter path and at least one exit path

        # each path must connect to a stage but only the main stage has exit path 
        
        # when a exit path is taken the player can no longer choose a different path 
        
        # enemys will be despawned and a new stage will be generated at the end of the path
        
        # when a player enters the new stage the old stage will be derendered as well as the old stages paths
        
        # the player will aslo no longer be able to go back through that path
        
        pass
    
    # update
    def update(self, cam_offset, dt, diff_coeff):
        # stage
        self.active_stage.update(cam_offset, dt, diff_coeff)
        for stage in self.adjacent_stages:
           stage.update(cam_offset, dt, diff_coeff)

        for path in self.paths:
            path.update(cam_offset, dt)


    # draw
    def draw(self, screen, cam_offset):
        
        for stage in self.adjacent_stages:
           stage.draw(screen, cam_offset)
        self.active_stage.draw(screen, cam_offset)
        for path in self.paths:
            path.draw(screen, cam_offset)

    # add paths
    def add_exit_paths(self, stage:Stage, cam_offset) -> None:
        length = 2000 # pixels
        paths = stage.exit_paths
        for path in paths:
            length_y = 4000 * min(1+path[1], 1) * (1 + -2 * path[1])
            length_x = 4000 * min(1+path[0], 1) * (1 + -2 * path[0])
            position = Point(stage.player_start_pos.x - length_x, stage.player_start_pos.y - length_y)
            # add new stage
            new_stage = Stage(self.collisions, self.particles, self.enemies, self.experiance, self.projectiles, self.players, cam_offset, position)
            self.adjacent_stages.append(new_stage)
            # create path
            path_orientation = (min(1, math.fabs(length_x)), min(1, math.fabs(length_y)))
            print(path_orientation)
            new_path = Path(stage.player_start_pos, new_stage.player_start_pos, path_orientation, new_stage)
            self.paths.append(new_path)

