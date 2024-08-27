import pygame

# represents a entity, and its spawn parameters
class Card:
    def __init__(self, name, type, catagory, cost, weight):
        
        # parameters
        self.name = name
        self.type = type
        self.catagory = catagory
        self.cost = cost
        self.weight = weight