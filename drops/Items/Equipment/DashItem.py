from drops.Items.Item import Item
from Actions.Dash import Dash
import pygame

class DashItem(Item): 
    def __init__(self, id):
        super().__init__("Dash", "Active", id)
        self.icon = pygame.transform.scale(pygame.image.load("assets/Equipment/Dash_ready.png").convert_alpha(), (16*8, 16*8))
        self.description = "Inrease movement speed, when troubles face you... run away"

    # added item to item list, add item to actions list
    def connect(self, parent):
        super().connect(parent)
        
        parent.actions.append(Dash(4, 3, parent))
        parent.determine_angles()

    # for when an item is removed
    def remove(self):
        pass