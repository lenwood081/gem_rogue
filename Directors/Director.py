

# simplilar to how directors work in risk of rain 2

class Director:
    def __init__(self, credits, group):
        # directors current credits
        self.credits = credits

        # entity group to add to
        self.group = group

        # spawm count
        self.spawn_count = group.__len__()