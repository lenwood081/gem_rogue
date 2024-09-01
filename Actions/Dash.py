from Actions.Action import Action
from config import FRAMERATE
from classes.Point import Point

# TODO add animations

class Dash(Action):
    def __init__(self, cooldown, charges, own_object):
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

    # setup images
    def setup_images(self):
        self.image_list.clear()
        for i in range(10):
            pos = self.start_pos.copy()
            pos.move(self.total_vec.x/(1.2+0.2*i), self.total_vec.y/(1.2+0.2*i))
            self.image_list.append((self.base_image, pos, 255/(2 + 0.2*i)))

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
            self.start_pos = self.own_object.pos.copy()
            
        
        self.activated = True
        self.use_charge()

        # for duration
        if self.activated:
            self.move_normal = False
            self.own_object.set_speed(4)
            self.own_object.velocity.x = self.own_object.speed * self.target.x
            self.own_object.velocity.y = self.own_object.speed * self.target.y

            # for dash animation
            self.total_vec.move(self.own_object.velocity.x, self.own_object.velocity.y)
            self.setup_images()
        else:
            self.own_object.set_speed(0)
            self.time = self.time_between
            self.move_normal = True
            self.image_list.clear()
            self.total_vec = Point(0, 0)
            

    # dashing effect
    def draw(self, screen):
        super().draw(screen)

        cam_offset = self.own_object.cam_offset
        for image in self.image_list:
            rect = image[0].get_rect(center = (
                image[1].x + cam_offset.x,
                -image[1].y + cam_offset.y,
            ))
            image[0].set_alpha(image[2])
            screen.blit(image[0], rect)









