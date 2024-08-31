from Actions.Action import Action
from config import *

# checks if a weapon can fire
class WeaponFire(Action):
    def __init__(self, charges, name, parent, type, angle):
        # weapon 
        self.weapon = type(parent.pos, parent.cam_offset, parent.projectile_group)

        # determine cooldown based on attack_rate
        cooldown = 1/(parent.attack_rate * self.weapon.fire_rate_mod)

        # Action constructer
        super().__init__(cooldown, charges, name)

        # reference to parent
        self.parent = parent
        self.weapon.angle_on_player = angle
        self.fire = False

    # use method
    def use(self):
        if self.check_active():
            self.fire = True
            self.use_charge()

    # update method
    def update(self):
        self.weapon.update(self.parent.front, self.parent.target_unit_vector, self.parent.pos, self.parent.enemy_group, self.fire,
                           (self.parent.projectile_speed, self.parent.damage, self.parent.knockback), self.parent.cam_offset)
        if self.fire:
            self.fire = False
        super().update()
        
    # draw method
    def draw(self, screen):
        self.weapon.draw(screen)

