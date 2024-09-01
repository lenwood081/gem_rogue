from drops.Items.Item import Item

# improves movement speed by 5%

class Quads(Item): 
    def __init__(self, id):
        super().__init__("Quads", "Passive", id)

        self.speed_increase = 2
        

    # produce effect
    def connect(self, parent):
        super().connect(parent)

        parent.max_speed *= self.speed_increase
        parent.speed = parent.max_speed
        

    # for when an item is removed
    def remove(self, parent):
        super().remove(parent)

        parent.max_speed /= self.speed_increase
        parent.speed = parent.max_speed