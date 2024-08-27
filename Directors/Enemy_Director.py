from Director import Director
from Card import Card
from Enemy_cards.EnemyCards import ENEMYCARDS
from classes.Point import Point
from config import *
import random

# basic Enemy director, for continuous spawns (can be fast or slow)

class Enemy_Director(Director):
    def __init__(self, group, wave_freq):
        # continous directors start with zero credits
        super(Enemy_Director, self).__init__(credits, 0, group)

        # credits
        self.credit_multiplier = 1

        # spawn intervals
        self.time_till_next_spawn = 0
        self.time_till_next_wave = 0
        self.wave_diff_time = random.uniform(wave_freq*FRAMERATE, (wave_freq + wave_freq/2)*FRAMERATE)

        # current spawn card index (-1 means new card must be selected)
        self.index = -1

    def update(self, coeff):
        # credit increase per framerate
        self.credits += (self.credit_multiplier * (1+coeff))/FRAMERATE

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
            self.time_till_next_spawn = random.uniform(0.1*FRAMERATE, FRAMERATE)
        else:
            return
        
        # if index != -1 skip next two steps

        # find all avaliable spawn picks (everything with a cos less then the credit value)

        # take these cards and select a monster (save this to an index)

        # spawn monster (with random positions, and enemy_group)

    def spawn_monster(self):
        monster_pos = Point()




        






