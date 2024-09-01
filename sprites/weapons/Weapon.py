import pygame
from classes.Point import Point
from classes.Direction import Direction
from config import FRAMERATE

class Weapon(pygame.sprite.Sprite):
    def __init__(self, pos, idle_animation, size, cam_offset, projectile_group):
        super(Weapon, self).__init__()

        # center
        self.pos = pos.copy()
        self.front = Direction(0)
        self.offset = 0

        # animations
        self.idle_animaiton = idle_animation

        # image
        self.image = idle_animation.animate(1)
        self.base_image = self.image
        self.hitbox_rect = self.base_image.get_rect(center=(
            self.pos.x + cam_offset.x, 
            -self.pos.y + cam_offset.y
        ))
        self.rect = self.hitbox_rect.copy()

        # general
        self.width = size[0]
        self.height = size[1]
        self.angle_on_player = 0

        # used to determine if firing
        self.start_fire = False
        self.continous_fire = False

        # projectiles if any
        self.projectiles = projectile_group

    # face target
    def face_target(self, target_dir):
        # copy target direction
        self.front.dir = target_dir.dir

        # move image
        self.base_image = self.animation_control()
        self.image = Direction.rotate_with_flip(self.front.dir, self.base_image)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)
    
    # check if need to attack
    def do_attack(self, fire):
        if fire:
            # for animations
            if self.start_fire:
                self.continous_fire = True
            else:
                self.start_fire = True
            return True
        return False
    
    

        





