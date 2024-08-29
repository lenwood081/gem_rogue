from config import FRAMERATE

class Action:
    def __init__(self, cooldown, charges):
        assert(charges > 0)
        assert(cooldown >= 0)

        # cooldown amount
        self.cooldown_time = cooldown * FRAMERATE
        self.cooldown = 0

        # charges
        self.max_charges = charges
        self.charges = 1
    
    # change by percentage (up or down)
    def change_cooldown(self, percentage):
        self.cooldown_time *= 1 + percentage

    # specify charges
    def set_charges(self, charges):
        self.max_charges = max(charges, self.max_charges)

    # use a charge
    def use_charge(self):
        self.charges -= 1

    # check active
    def check_active(self):
        if self.charges > 0:
            return True
        return False
        
    # update cooldwons and charges
    def update(self):
        if self.charges == self.max_charges:
            self.cooldown = self.cooldown_time
            return
        
        # check cooldowns
        self.cooldown -= 1
        if self.cooldown <= 0:
            self.charges += 1
            self.cooldown = self.cooldown_time
        

        
