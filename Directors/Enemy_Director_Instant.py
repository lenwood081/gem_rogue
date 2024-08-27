from Directors.Director import Director
from Directors.Card import Card
from Directors.Enemy_cards.EnemyCards import ENEMYCARDS
from classes.Point import Point
from config import *


class Enemy_Director_Instant(Director):
    def __init__(self, credits, group, experiance_group):
        # get credits from user
        super(Enemy_Director_Instant, self).__init__(credits, group, experiance_group)

        # counts the number of the current monster being spawned (if above 4, pick a new one)
        self.count_monster = 0
        self.base_credits = credits        


    def activate(self, coeff, player_pos):
        self.player_pos = player_pos.copy()

        # assign credits
        self.credits = self.credits * coeff

        # keep spawning until credits are lower then lowest enemy
        while True:
            # if enemy found spawn it
            if self.index != -1:
                self.spawn_monster(ENEMYCARDS)
                self.count_monster += 1

            # choose new enemy if too many
            if self.count_monster >= 4:
                self.count_monster = 0
                self.index = -1

            # choose enemy
            if self.index == -1:
                val = self.choose_monster_index(ENEMYCARDS)
                if val == False:
                    return

            
            
