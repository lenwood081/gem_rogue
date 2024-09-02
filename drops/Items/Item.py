

class Item:
    def __init__(self, name, type, id):
        # item name and type
        self.name = name
        self.type = type

        # need to be implimented in the parent class
        self.description = "Defualt description"
        self.icon = None
        
        # this will identify the item in a item or action list as will be always unique per entity
        self.unique_id = id


    # method to attach that item to a player or enemy, must be implimented in child classs
    def connect(self, parent):
        pass

    # for when an item is removed
    def remove(self, parent):
        pass

    def __eq__(self, id):
        return self.unique_id == id