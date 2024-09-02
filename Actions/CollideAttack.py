from Actions.Action import Action
import pygame

# basic collision attack (ie if a enemy runs into you can it hit you)

class CollideAttack(Action):
    def __init__(self, cooldown, charges, parent, enemy_object):
        super().__init__(cooldown, charges, parent, "Collide Attack")

        # two ItemHolder subclass objects
        self.enemy_object = enemy_object
        
    
    # set enemy
    def set_new_enemy(self, enemy_object):
        self.enemy_object = enemy_object

    # attack
    def use(self, dt):
        if pygame.Rect.colliderect(self.parent.hitbox_rect, self.enemy_object.hitbox_rect) and self.check_active():
            self.enemy_object.take_damage(self.parent.attack(), self.parent.target_unit_vector, self.parent.knockback)
            self.use_charge(dt)