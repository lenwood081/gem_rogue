from Actions.Action import Action
from config import *

# checks if a weapon can fire
class WeaponFire(Action):
    def __init__(self, charges, name, parent, type):
        # weapon 
        self.weapon = type(parent.pos, parent.cam_offset, parent.projectile_group)
        

        # determine cooldown based on attack_rate
        cooldown = 1/(parent.attack_rate * self.weapon.fire_rate_mod)

        # Action constructer
        super().__init__(cooldown, charges, parent, name)
        self.class_name = "Weapon"
        # reference to parent
        self.weapon.angle_on_player = 0
        self.fire = False

    # use method
    def use(self, dt):
        if self.check_active():
            self.fire = True
            self.use_charge(dt)

    # override check.active
    def check_active(self):
        if self.parent.can_attack == False:
            return False
        return super().check_active()

    # update method
    def update(self, dt):
        self.weapon.update(self.parent.front, self.parent.target_unit_vector, self.parent.pos, self.parent.enemy_group, self.fire,
                           (self.parent.projectile_speed, self.parent.damage, self.parent.knockback), self.parent.cam_offset, dt)
        if self.fire:
            self.fire = False
        super().update(dt)
        
    # draw method
    def draw(self, screen):
        self.weapon.draw(screen)

    # angle
    def change_angle(self, angle):
        super().change_angle(angle)
        self.weapon.angle_on_player = angle

