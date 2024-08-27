import pygame
from classes.Point import Point
from sprites.weapons.Weapon import Weapon

class Gun(Weapon):
    def __init__(self, pos, bg_pos, image_url, size):
        super(Gun, self).__init__(pos, image_url, size, bg_pos)

        # projectiles
        self.projectiles = pygame.sprite.Group()
        self.gun_damage_mod = 1
        self.bullet_speed_mod = 1
        self.fire_rate_mod = 1
        self.knockback_mod = 1

        # attributes combined from parent
        self.bullet_speed = 0
        self.gun_damage = 0
        self.fire_rate = 0
        self.knockback = 0


    # blit weapon to screen
    def draw(self, screen, bg_pos):
        self.rect = self.image.get_rect(center=(
            self.pos.x + bg_pos.x, 
            -self.pos.y + bg_pos.y))
        # change center to top left
        screen.blit(self.image, self.rect)

        # blit all projectiles
        for projectile in self.projectiles:
            projectile.draw(screen, bg_pos)

    # update gun (parent attributes = (bullet_speed, bullet_damage, fire_rate, knockback))
    def update(self, player_dir, target_unit_vector, player_pos, enemie_group, fire, parent_attributes):
        unit_vector = Point.rotate_unit_vector_flip(target_unit_vector, self.angle_on_player, self.front.dir)
        self.pos.x = player_pos.x + self.offset * unit_vector.x
        self.pos.y = player_pos.y + self.offset * unit_vector.y

        # point in correct direction
        self.face_target(player_dir)
        
        # update attributes return (self.bullet_speed, self.gun_damage, self.knockback)
        attributes = self.update_stats(parent_attributes)

        # run shooting script
        self.shoot(player_dir, target_unit_vector, fire, attributes)

        # update projectiles
        for projectile in self.projectiles:
            projectile.update(enemie_group)

    # update values
    def update_stats(self, parent_attributes):
        self.bullet_speed = parent_attributes[0] * self.bullet_speed_mod
        self.gun_damage = parent_attributes[1] * self.gun_damage_mod
        self.fire_rate = parent_attributes[2] * self.fire_rate_mod
        self.knockback = parent_attributes[3] * self.knockback_mod
        return (self.bullet_speed, self.gun_damage, self.knockback)
    
    # shoots a bullet
    def shoot(self, player_dir, target_unit_vector, fire, attributes):
        if self.can_attack(): 
            if self.do_attack(fire):
                pos = Point(self.pos.x + target_unit_vector.x * self.width/2, self.pos.y + target_unit_vector.y * self.height/2)
                new_projectile = self.bullet_type(pos, target_unit_vector, player_dir, attributes)
                self.projectiles.add(new_projectile)
                