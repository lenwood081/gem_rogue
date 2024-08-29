from Actions.Action import Action
import pygame

# basic collision attack (ie if a enemy runs into you can it hit you)

class CollideAttack(Action):
    def __init__(self, cooldown, charges, own_object, enemy_object):
        super().__init__(cooldown, charges)

        # two ItemHolder subclass objects
        self.own_object = own_object
        self.enemy_object = enemy_object
    
    # set enemy
    def set_new_enemy(self, enemy_object):
        self.enemy_object = enemy_object

    # attack
    def use(self):
        if pygame.Rect.colliderect(self.own_object.hitbox_rect, self.enemy_object.hitbox_rect) and self.check_active():
            self.enemy_object.take_damage(self.own_object.attack(), self.own_object.target_unit_vector, self.own_object.knockback)
            self.use_charge()