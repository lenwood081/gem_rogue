import numpy
import random
from utility.Point import Point
from config import *
from Background.TileMap import TileMap
from Background.Tile import Tile

# simplilar to how directors work in risk of rain 2

# for both spawners make sure to take into account player pos

class Director:
    def __init__(self, credits, group, experiance_group, projectile_group, particle_group, players, spawn_map:TileMap, cam_offset):
        # directors current credits
        self.credits = credits
        self.credit_multiplier = 1

        # entity group to add to
        self.group = group
        self.experiance_group = experiance_group
        self.projectile_group = projectile_group
        self.particle_group = particle_group
        self.players = players
        self.spawn_map = spawn_map

        # spawm count
        self.spawn_count = group.__len__()

        # current spawn card index (-1 means new card must be selected)
        self.index = -1

        # player aura
        self.player = None
        # select a player
        for player in players:
            self.player = player
        self.player_aura = 300

        self.player_pos = player.pos
        self.cam_offset = cam_offset

    # for spawning
    def spawn_monster(self, cards):
        self.credits -= cards[self.index].cost

        # decide on a random spawnable tile
        tileP = None;

        while True:
            attempt_index = random.randint(0, self.spawn_map.length)
            i = 0
            breaking = False
            for tile_row in self.spawn_map.tile_array:
                for tile in tile_row:
                    if i == attempt_index:
                        tileP = tile
                        breaking = True
                        break
                    i += 1
                if breaking:
                    break;

            # check spawing is false
            if isinstance(tileP, Tile) == False:
                continue;
            
            if tileP.spawning:
                continue;

            # else spawn
            break;


        # spawn there, indicate first (spawning circle)

        tileP.spawning = True
        tileP.enemy = cards[self.index].type(tileP.center_pos, self.experiance_group, self.projectile_group, self.players, self.particle_group, self.cam_offset)

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