

class Item:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        
        # how it looks and other values should be stored


    # method to attach that item to a player or enemy, must be implimented in child classs
    def connect(self):
        pass

    # for when an item is removed
    def remove(self):
        pass