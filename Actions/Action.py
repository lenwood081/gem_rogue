from config import FRAMERATE

class Action:
    def __init__(self, cooldown, charges, parent, name, duration=0):
        assert(charges > 0)
        assert(cooldown >= 0)

        self.class_name = "None"

        # action name
        self.name = name
        self.parent = parent
        self.angle = 0

        # cooldown amount
        self.cooldown_time = cooldown * FRAMERATE
        self.cooldown = 0

        # time between activations
        self.time_between = 0
        self.time = self.time_between

        # charges
        self.max_charges = charges
        self.charges = self.max_charges
    
        # duration
        self.duration = duration * FRAMERATE
        self.max_duration = duration * FRAMERATE

        # activaed
        self.activated = False

        # move_normal
        self.move_normal = True

        # fire_normal
        self.fire_normal = True

    # change by percentage (up or down)
    def change_cooldown(self, percentage):
        self.cooldown_time *= 1 + percentage

    # specify charges
    def set_charges(self, charges):
        self.max_charges = max(charges, self.max_charges)

    # use a charge
    def use_charge(self, dt):
        self.duration -= 1 * dt
        if self.duration <= 0:
            self.duration = self.max_duration
            self.charges -= 1
            self.activated = False

    # check active
    def check_active(self):
        if self.charges > 0:
            return True
        return False
        
    # update cooldwons and charges
    def update(self, dt):
        # check if action is ongoing
        if self.activated:
            self.use(dt)

        if self.charges == self.max_charges:
            self.cooldown = self.cooldown_time
            return
        
        # check cooldowns
        self.cooldown -= 1 * dt
        if self.cooldown <= 0:
            self.charges += 1
            self.cooldown = self.cooldown_time

    # method to be overriden
    def use(self, dt):
        # override this method in specific action class
        return
    
    # method to be overriden
    def draw(self, screen):
        # override this method in specific action class
        return
    
    # retruns whether the action is active
    def already_active(self):
        return self.activated
    
    # change angle
    def change_angle(self, angle):
        self.angle = angle
        

        
