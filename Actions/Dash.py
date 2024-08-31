from Actions.Action import Action
from config import FRAMERATE

# TODO add animations

class Dash(Action):
    def __init__(self, cooldown, charges, own_object):
        super().__init__(cooldown, charges, "dash", 0.1)

        # briefly significantly increase player speed
        self.own_object = own_object

        # time between activations
        self.time_between = 0.05 * FRAMERATE
        self.time = self.time_between

        # move normal
        self.move_normal = True

        # target vector
        self.target = self.own_object.target_unit_vector.copy()

    # dash
    def use(self):
        # check condition
        if self.check_active() == False or self.time > 0:
            self.time -= 1
            if self.time < 0:
                self.time = 0
            return
        
        # check if first time activated
        if self.activated == False:
            # target vector
            self.target = self.own_object.target_unit_vector.copy()
            self.own_object.immune = True
            self.own_object.immunity_frames = self.max_duration 
        
        self.activated = True
        self.use_charge()

        # for duration
        if self.activated:
            self.move_normal = False
            self.own_object.set_speed(4)
            self.own_object.velocity.x = self.own_object.speed * self.target.x
            self.own_object.velocity.y = self.own_object.speed * self.target.y
        else:
            self.own_object.set_speed(0)
            self.time = self.time_between
            self.move_normal = True






