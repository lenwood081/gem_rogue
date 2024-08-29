import pygame
from config import *
from classes.Point import Point
from classes.Direction import Direction
from classes.Glow import Glow
from sprites.weapons.Guns.BasicGun import BasicGun
from sprites.weapons.Guns.PlasmaGun import PlasmaGun
from Animations.Animation import Animation
from sprites.ItemHolder import ItemHolder
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
    K_e,
)
import math

MOUSE = 'mouse1'

# TODO link weapon and projectile damage to player damage

class Player(ItemHolder):
    def __init__(self, projectile_group):
        super(Player, self).__init__()
        # ---------------------- ITEM HOLDER ATTRIBUTES -------------------

        # health
        self.health = self.max_health = 10

        # dimensions
        self.width = self.max_width = 32*SCALE_FACOTOR
        self.height = self.max_height = 32*SCALE_FACOTOR

        # speed
        self.speed = self.max_speed = 900 / FRAMERATE

        # level
        self.level = 0

        # attacking
        self.damage = self.max_damage = 1
        self.knockback = self.max_knockback = 1
        self.attack_rate = self.max_attack_rate = 3
        self.projectile_speed = self.max_projectile_speed = 1000 / FRAMERATE

        # -----------------------------------------------------------------

        # base image
        #self.base_animate = Animation(["assets/player/Player_concept1_walk1.png", "assets/player/Player_concept1_walk2.png"], (self.width, self.height), [0.3, 0.3])
        self.base_animate = Animation(["assets/player/duck_wizard.png"], (32*SCALE_FACOTOR , 32*SCALE_FACOTOR), [0.3])
        self.image = self.base_animate.animate()
        self.base_image = self.image
        self.hitbox_rect = self.base_image.get_rect(center=(
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT/2,
        ))
        self.boundary_rect = self.hitbox_rect.copy()
        self.rect = self.hitbox_rect.copy()
        # glow
        self.radius = self.width * 0.5
        self.glow_rate = 0.5
        self.num_glows = 5
        self.max_diff = 10
        self.current = 0
        self.increasing = 30 / FRAMERATE

        # position reletive to background (centered)
        # start in the center of the playable area
        self.pos = Point(BG_WIDTH/2 + self.width/2, -BG_HEIGHT/2 - self.height/2)
        self.velocity = Point(0, 0)

        # position to the center of the screen
        self.pos_screen = Point(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

        # used to update weapons and projectiles
        self.cam_offset = Point(0, 0)

        # direction and target vextor
        self.front = Direction(0)
        self.mouse_unit_vector = Point(0, 0)

        # drops
        self.collect_range = 100
        self.exp = 0
        self.exp_to_level = 10

        # weapons
        self.weapon_assit_array = []
        self.projectile_group = projectile_group

        # added Basic gun
        self.add_weapon(PlasmaGun, MOUSE, -math.pi/3)
        self.add_weapon(PlasmaGun, MOUSE, -math.pi/8)
        self.add_weapon(PlasmaGun, MOUSE, math.pi/8)
        self.add_weapon(PlasmaGun, MOUSE, math.pi/3)
        

    # ---------------------------------------- for bliting and collision detect ------------------

    # blit player and weapon
    def draw(self, screen):
        # glow breath
        radius = self.radius * (self.num_glows*2) + self.current
        if self.current >= self.max_diff:
            self.increasing = -30 / FRAMERATE
        elif self.current <= self.max_diff * -1:
            self.increasing = 30 / FRAMERATE
        self.current += self.increasing * self.glow_rate

        # draw glow
        screen.blit(Glow.circle_image_add(radius), (self.pos_screen.x - radius, self.pos_screen.y - radius), special_flags=pygame.BLEND_RGBA_ADD)

        # draw player
        screen.blit(self.image, self.rect)

        # draw weapon
        self.draw_weapons(screen)

        # debugging
        #pygame.draw.rect(screen, "red", self.hitbox_rect, width=2)
        #pygame.draw.rect(screen, "blue", self.rect, width=2)

    def boundary_collision(self, collision_group):
        # call on self
        for tile in collision_group:
            # could be optimised by checking first if there is a collision then checking left and right
            self.boundary_rect.center = (SCREEN_WIDTH/2 + self.velocity.x, SCREEN_HEIGHT/2 - self.velocity.y)
            if pygame.Rect.colliderect(self.boundary_rect, tile.rect):
                # check x
                self.boundary_rect.center = (SCREEN_WIDTH/2 + self.velocity.x, SCREEN_HEIGHT/2)
                if pygame.Rect.colliderect(self.boundary_rect, tile.rect):
                    # left hand edge
                    if self.velocity.x > 0:
                        self.pos.x = tile.pos.x - self.width/2
                    # right hand side
                    elif self.velocity.x < 0:
                        self.pos.x = tile.pos.x + tile.width + self.width/2
    
                # check y
                self.boundary_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - self.velocity.y)
                if pygame.Rect.colliderect(self.boundary_rect, tile.rect):
                    # top
                    if self.velocity.y > 0:
                        self.pos.y = tile.pos.y - tile.height - self.height/2
                    # bottom
                    elif self.velocity.y < 0:
                        self.pos.y = tile.pos.y + self.height/2


    # ------------------------------------------ facing mouse --------------------------------

    # rotating player
    def face_mouse(self):
        # find mouse pos
        mx, my = pygame.mouse.get_pos()
        mouse_pos = Point(mx, -my)

        # y must be reversed 
        temp_pos =  Point(self.pos_screen.x, -self.pos_screen.y)
        mouse_dir = Point.direction_to_point(mouse_pos, temp_pos)

        # make unit vector for point to travel to
        self.mouse_unit_vector = Point.unit_vector(mouse_pos, temp_pos)

        # rotate image
        self.image = Direction.rotate_with_flip(mouse_dir.dir, self.base_image)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)
        self.front = mouse_dir

    # rotating player method #2
    def flip_mouse(self):
        # find mouse pos
        mx, my = pygame.mouse.get_pos()
        mouse_pos = Point(mx, -my)

        # y must be reversed 
        temp_pos =  Point(self.pos_screen.x, -self.pos_screen.y)
        mouse_dir = Point.direction_to_point(mouse_pos, temp_pos)

        # make unit vector for point to travel to
        self.mouse_unit_vector = Point.unit_vector(mouse_pos, temp_pos)

        # flip image if needed
        if mouse_dir.dir < -math.pi/2 or mouse_dir.dir > math.pi/2:
            self.image = self.base_image
        else:
            self.image = pygame.transform.flip(self.base_image, True, False)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)
        self.front = mouse_dir

    # ---------------------------------------- updates --------------------------------------------
        
    # update loop
    def update(self, keys_pressed, boundary):
        x = 0
        y = 0

        # player movement
        if keys_pressed[K_s]:
            y = -self.speed
        if keys_pressed[K_w]:
            y = self.speed
        if keys_pressed[K_d]:
            x = self.speed
        if keys_pressed[K_a]:
            x = -self.speed

        # check for diagonal speed irregularity
        if x != 0 and y != 0:
            x /= math.sqrt(2)
            y /= math.sqrt(2)

        
        self.velocity = Point(x, y)
        self.pos.move(x, y)
        self.boundary_collision(boundary)

        # animation
        self.base_image = self.base_animate.animate()

        #self.face_mouse()
        self.flip_mouse()

    # secound update for things that require background pos to be updated
    def update_after_camera(self, keys_pressed, mouse_pressed, cam_offset, enemy_group, boundary):
        if self.immune:
            self.immunity_frames -= 1
            if self.immunity_frames == 0:
                self.immune = False

        # updates store of cam_offset
        self.cam_offset = cam_offset

         # weapon update
        self.update_weapons(enemy_group, keys_pressed, mouse_pressed)


# ------------------------ Leveling up -------------------------------

    # death method
    def death(self):
        # reset to game screen
        self.kill()

    # for adding exp
    def add_exp(self, exp):
        self.exp += exp

        if self.exp >= self.exp_to_level:
            self.exp -= self.exp_to_level
            self.level_up_player()

    # leveling up
    def level_up_player(self):
        self.level_up()
        # eponentual
        self.exp_to_level *= 2 

# ------------------------ For Weapon Code ---------------------------

    # add_weapon
    def add_weapon(self, type, fire_key, angle):
        # add key to correct position
        self.weapon_assit_array.append((fire_key, angle))
        weapon = type(self.pos, self.cam_offset, self.projectile_group)
        weapon.angle_on_player = angle
        self.weapons.add(weapon)

    # using mouse_pressed and key_pressed as faster and allows for holddown input
    def update_weapons(self, enemy_group, keys_pressed, mouse_pressed):
        for  i, weapon in enumerate(self.weapons):
            fire = False
            if self.weapon_assit_array[i][0] == MOUSE:
                if mouse_pressed[0]:
                    fire = True
            elif keys_pressed[self.weapon_assit_array[i][0]]:
                fire = True
            weapon.update(self.front, self.mouse_unit_vector, self.pos, enemy_group, fire, (self.projectile_speed, self.damage, self.attack_rate, self.knockback), self.cam_offset)

    # draw weapons
    def draw_weapons(self, screen):
        for weapon in self.weapons:
            weapon.draw(screen)

