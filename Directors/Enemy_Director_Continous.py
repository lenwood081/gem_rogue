from Directors.Director import Director
from Directors.Enemy_cards.EnemyCards import ENEMYCARDS
from config import *
import random

# basic Enemy director, for continuous spawns (can be fast or slow)

class Enemy_Director_Continous(Director):
    def __init__(self, group, wave_freq, experiance_group):
        # continous directors start with zero credits
        super(Enemy_Director_Continous, self).__init__(0, group, experiance_group)

        # spawn intervals
        self.time_till_next_spawn = 0
        self.time_till_next_wave = 0
        self.spawn_diff_time = random.uniform(0.1*FRAMERATE, FRAMERATE)
        self.wave_diff_time = random.uniform(wave_freq*FRAMERATE, (wave_freq + wave_freq/2)*FRAMERATE)
        self.wave_freq = wave_freq

        
    # update loop
    def update(self, coeff, player_pos):
        self.spawn_diff_time = random.uniform(0.1*FRAMERATE, FRAMERATE)
        self.wave_diff_time = random.uniform(self.wave_freq*FRAMERATE, (self.wave_freq + self.wave_freq/2)*FRAMERATE)

        self.player_pos = player_pos.copy()

        # credit increase per framerate
        self.credits += (self.credit_multiplier * (1+coeff))/FRAMERATE

        # attempt spawn
        self.attempt_spawn()

    # attampt to spawn
    def attempt_spawn(self):
        # wave check first
        self.time_till_next_wave -= 1

        if self.time_till_next_wave > 0:
            return

        # then spawn check
        self.time_till_next_spawn -= 1
        
        if self.time_till_next_spawn <= 0:
            # if zero then will attampt to spawn (so reset timer)
            self.time_till_next_spawn = self.spawn_diff_time
        else:
            return
        
        # if index != -1 skip next two steps
        if self.index != -1:
            if ENEMYCARDS[self.index].cost > self.credits:
                # fail
                self.time_till_next_wave = self.wave_diff_time
                self.index = -1
                return
            else:
                # spawn this moster
                self.spawn_monster(ENEMYCARDS)
                return
            
        # ---------------------------- selecting monster ----------------------------

        # spawn monster (with random positions, and enemy_group)
        if self.choose_monster_index(ENEMYCARDS):
            self.spawn_monster(ENEMYCARDS)
        else:
            self.time_till_next_wave = self.wave_diff_time





        






