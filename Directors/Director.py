import numpy
import random
from classes.Point import Point
from config import *

# simplilar to how directors work in risk of rain 2

# for both spawners make sure to take into account player pos

class Director:
    def __init__(self, credits, group, experiance_group, projectile_group):
        # directors current credits
        self.credits = credits
        self.credit_multiplier = 1

        # entity group to add to
        self.group = group
        self.experiance_group = experiance_group
        self.projectile_group = projectile_group

        # spawm count
        self.spawn_count = group.__len__()

        # current spawn card index (-1 means new card must be selected)
        self.index = -1

        # player aura
        self.player_aura = 300
        self.player_pos = Point(0,0)

    # for spawning
    def spawn_monster(self, cards):
        #print("before", self.credits)
        self.credits -= cards[self.index].cost
        # create a buffer for monsters so they dont glitch out of bounds
        monster_pos = Point(random.randint(64, BG_WIDTH - 64), random.randint(-BG_HEIGHT+ 64, -64))
        # make sure point is not too close to player
        while True:
            if monster_pos.x < self.player_pos.x - self.player_aura or monster_pos.x > self.player_pos.x + self.player_aura:
                if monster_pos.y < self.player_pos.y - 300 or monster_pos.y > self.player_pos.y + 300:
                    break;
            monster_pos = Point(random.randint(64, BG_WIDTH - 64), random.randint(-BG_HEIGHT+ 64, -64))
        self.group.add(cards[self.index].type(monster_pos, self.experiance_group, self.projectile_group))
        #print("Spawning", cards[self.index].name)
        #print("after", self.credits)

    # choose monster
    def choose_monster_index(self, cards):
        # find all avaliable spawn picks (everything with a cos less then the credit value)
        index_array = []
        prob_array = []
        num_attributes = 0
        for i, entity in enumerate(cards):
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
            self.index = -1
            return False
        
        self.index = random.choices(index_array, prob_array)[0]
        return True