from drops.Items.Item import Item
from Actions.Dash import Dash

class DashItem(Item): 
    def __init__(self, id):
        super().__init__("Dash", "Utility", id)

    # added item to item list, add item to actions list
    def connect(self, parent):
        super().connect(parent)
        
        parent.actions.append(Dash(3, 3, parent))
        parent.determine_angles()

    # for when an item is removed
    def remove(self):
        pass