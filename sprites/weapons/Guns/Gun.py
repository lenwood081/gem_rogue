import pygame
from utility.Point import Point
from sprites.weapons.Weapon import Weapon
from utility.Direction import Direction

class Gun(Weapon):
    def __init__(self, pos, cam_offset, idle_animaiton, fire_animation, muzzle_flash, size, projectile_group):
        super(Gun, self).__init__(pos, idle_animaiton, size, cam_offset, projectile_group)

        # fire animation
        self.fire_animaiton = fire_animation
        self.muzzle_flash_animaiton = muzzle_flash

        self.muzzle_image_base = self.muzzle_flash_animaiton.animate(1)
        self.muzzle_image = self.muzzle_image_base
        self.muzzle_image_rect = self.muzzle_image_base.get_rect()

        # projectiles
        self.gun_damage_mod = 1
        self.bullet_speed_mod = 1
        self.fire_rate_mod = 1
        self.knockback_mod = 1

        # attributes combined from parent
        self.bullet_speed = 0
        self.gun_damage = 0
        self.knockback = 0

        self.dt = 1


    # blit weapon to screen
    def draw(self, screen):
        # main gun
        screen.blit(self.image, self.rect)

        # blit muzzle flash if exists
        if self.muzzle_image:
            screen.blit(self.muzzle_image,self.muzzle_image_rect, special_flags=pygame.BLEND_RGBA_ADD)


    # update gun (parent attributes = (bullet_speed, bullet_damage, knockback))
    def update(self, player_dir, target_unit_vector, player_pos, enemy_group, fire, parent_attributes, cam_offset, dt):
        self.dt = dt

        unit_vector = Point.rotate_unit_vector_flip(target_unit_vector, self.angle_on_player, self.front.dir)
        self.pos.x = player_pos.x + self.offset * unit_vector.x
        self.pos.y = player_pos.y + self.offset * unit_vector.y

        # point in correct direction
        self.face_target(player_dir)

        # update attributes return (self.bullet_speed, self.gun_damage, self.knockback)
        attributes = self.update_stats(parent_attributes)

        # run shooting script
        self.shoot(player_dir, target_unit_vector, enemy_group, fire, attributes)

        self.hitbox_rect.center = (self.pos.x + cam_offset.x, -self.pos.y + cam_offset.y)
        self.rect.center = self.hitbox_rect.center
        self.muzzle_image_rect.center = (self.hitbox_rect.centerx + (self.flash_offset)* target_unit_vector.x, self.hitbox_rect.centery - (self.flash_offset) * target_unit_vector.y)

    # update values
    def update_stats(self, parent_attributes):
        self.bullet_speed = parent_attributes[0] * self.bullet_speed_mod
        self.gun_damage = parent_attributes[1] * self.gun_damage_mod
        self.knockback = parent_attributes[2] * self.knockback_mod
        return (self.bullet_speed, self.gun_damage, self.knockback)
    
    # shoots a bullet
    def shoot(self, player_dir, target_unit_vector, enemy_group, fire, attributes):
        if self.do_attack(fire):
            pos = Point(self.pos.x + target_unit_vector.x * self.width/2, self.pos.y + target_unit_vector.y * self.height/2)
            new_projectile = self.bullet_type(pos, target_unit_vector, player_dir, attributes)
            new_projectile.set_enemy_group(enemy_group)
            self.projectiles.add(new_projectile)

    # animation control
    def animation_control(self):
        # fire animation
        if self.continous_fire:
            # assign to last frame
            self.fire_animaiton.set_frame(self.fire_animaiton.length-1)
        self.continous_fire = False

        if self.start_fire and self.fire_animaiton.get_completed() == False:
            # display muzzle_flash
            
            self.muzzle_image_base = self.muzzle_flash_animaiton.animate(self.dt)
            self.muzzle_image = Direction.rotate_with_flip(self.front.dir, self.muzzle_image_base)
            self.muzzle_image_rect = self.muzzle_image.get_rect(center = self.hitbox_rect.center)
            return self.fire_animaiton.animate(self.dt)
        
        self.start_fire = False
        self.muzzle_image = None

        # defualt is idle
        return self.idle_animaiton.animate(self.dt)

                