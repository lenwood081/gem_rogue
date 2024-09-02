from Actions.Action import Action
from config import (FRAMERATE, SCALE_FACOTOR)
from classes.Point import Point
from classes.Direction import Direction
from classes.Glow import Glow
import pygame

# TODO add animations

class Dash(Action):
    def __init__(self, cooldown, charges, own_object, angle):
        super().__init__(cooldown, charges, "dash", 0.1)

        # briefly significantly increase player speed
        self.own_object = own_object

        # time between activations
        self.time_between = 0.05 * FRAMERATE
        self.time = 0

        # move normal
        self.move_normal = True

        # target vector
        self.target = self.own_object.target_unit_vector.copy()

        # for dash animation (image should be rotated already)
        self.total_vec = Point(0, 0)
        self.start_pos = self.own_object.pos.copy()
        self.base_image = self.own_object.image

        # image, pos_division, alpha tuple
        self.image_list = []

        # icon
        self.angle = angle
        self.pos = self.own_object.pos.copy()
        self.offset = 25 * SCALE_FACOTOR

        # image
        self.base_image_active = pygame.transform.scale(pygame.image.load("assets/Equipment/Dash_ready.png").convert_alpha(), (16*SCALE_FACOTOR, 16*SCALE_FACOTOR))
        self.base_image_deactive = pygame.transform.scale(pygame.image.load("assets/Equipment/Dash_not_ready.png").convert_alpha(), (16*SCALE_FACOTOR, 16*SCALE_FACOTOR))
        self.image = self.base_image_active
        self.hitbox_rect = self.base_image_active.get_rect(center=(
            self.pos.x + own_object.cam_offset.x, 
            -self.pos.y + own_object.cam_offset.y
        ))
        self.rect = self.hitbox_rect.copy()

    # setup images
    def setup_images(self):
        self.image_list.clear()
        for i in range(10):
            pos = self.start_pos.copy()
            pos.move(self.total_vec.x/(1+0.3*i), self.total_vec.y/(1+0.3*i))
            self.image_list.append((self.base_image, pos, 255/(2 + 0.2*i)))

    # dash
    def use(self, dt):
        # check condition
        if self.check_active() == False or self.time > 0:
            self.time -= 1 * dt
            if self.time < 0:
                self.time = 0
            return
        
        # check if first time activated
        if self.activated == False:
            # target vector
            self.target = self.own_object.target_unit_vector.copy()
            self.own_object.immune = True
            self.own_object.immunity_frames = self.max_duration 
            self.start_pos = self.own_object.pos.copy()
            
        
        self.activated = True
        self.use_charge(dt)

        # for duration
        if self.activated:
            self.move_normal = False
            self.own_object.set_speed(4)

            # for dash animation
            self.total_vec.move(self.own_object.velocity.x, self.own_object.velocity.y)
            self.setup_images()

            self.own_object.velocity.x = self.own_object.speed * self.target.x * dt
            self.own_object.velocity.y = self.own_object.speed * self.target.y * dt            
        else:
            self.own_object.set_speed(0)
            self.time = self.time_between
            self.move_normal = True
            self.image_list.clear()
            self.total_vec = Point(0, 0)
            

    # dashing effect
    def draw(self, screen):
        super().draw(screen)

        # rotate image
        self.base_image_use = self.base_image_deactive
        
        if self.check_active():
            self.base_image_use = self.base_image_active

        unit_vector = Point.rotate_unit_vector_flip(self.own_object.target_unit_vector, self.angle, self.own_object.front.dir)
        self.pos.x = self.own_object.pos.x + self.offset * unit_vector.x
        self.pos.y = self.own_object.pos.y + self.offset * unit_vector.y

        # face target
        self.image = Direction.rotate_with_flip(self.own_object.front.dir, self.base_image_use)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)
        self.hitbox_rect.center = (self.pos.x + self.own_object.cam_offset.x, -self.pos.y + self.own_object.cam_offset.y)
        self.rect.center = self.hitbox_rect.center

        if self.check_active():
            # give it a small glow
            screen.blit(Glow.circle_image_add(12*SCALE_FACOTOR), (
                self.rect.centerx - 12*SCALE_FACOTOR,
                self.rect.centery - 12*SCALE_FACOTOR,
            ), special_flags=pygame.BLEND_RGBA_ADD)

        screen.blit(self.image, self.rect)

        # silohette images
        cam_offset = self.own_object.cam_offset
        for image in self.image_list:
            rect = image[0].get_rect(center = (
                image[1].x + cam_offset.x,
                -image[1].y + cam_offset.y,
            ))
            image[0].set_alpha(image[2])
            screen.blit(image[0], rect)









