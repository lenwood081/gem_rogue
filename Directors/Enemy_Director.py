from Directors.Director import Director
from Directors.Card import Card
import numpy
from Directors.Enemy_cards.EnemyCards import ENEMYCARDS
from classes.Point import Point
from config import *
import random

# basic Enemy director, for continuous spawns (can be fast or slow)

class Enemy_Director(Director):
    def __init__(self, group, wave_freq, experiance_group):
        # continous directors start with zero credits
        super(Enemy_Director, self).__init__(0, group, experiance_group)

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
            self.time_till_next_spawn = random.uniform(0.1*FRAMERATE, FRAMERATE)
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
                self.spawn_monster()
                return
            
        # ---------------------------- selecting monster ----------------------------
    
        # find all avaliable spawn picks (everything with a cos less then the credit value)
        index_array = []
        prob_array = []
        num_attributes = 0
        for i, entity in enumerate(ENEMYCARDS):
            if entity.cost <= self.credits:
                index_array.append(i)
                prob_array.append(entity.weight)
                num_attributes += 1

        # divide prob array by num_attributes
        prob_array = numpy.array(prob_array)
        prob_array = prob_array/num_attributes

        # take these cards and select a monster (save this to an index)
        if len(index_array) == 0:
            # fail
            self.time_till_next_wave = self.wave_diff_time
            self.index = -1
            return
        
        self.index = random.choices(index_array, prob_array)[0]

        # spawn monster (with random positions, and enemy_group)
        self.spawn_monster()

    def spawn_monster(self):
        #print("before", self.credits)
        self.credits -= ENEMYCARDS[self.index].cost
        monster_pos = Point(random.randint(0, BG_WIDTH), random.randint(-BG_HEIGHT, 0))
        self.group.add(ENEMYCARDS[self.index].type(monster_pos, self.experiance_group))
        #print("Spawning", ENEMYCARDS[self.index].name)
        #print("after", self.credits)




        






