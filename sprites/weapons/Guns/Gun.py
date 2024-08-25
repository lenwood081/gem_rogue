import pygame
from classes.Point import Point
from sprites.weapons.Weapon import Weapon

class Gun(Weapon):
    def __init__(self, pos, bg_pos, image_url, size):
        super(Gun, self).__init__(pos, image_url, size, bg_pos)

        # projectiles
        self.projectiles = pygame.sprite.Group()
        self.gun_damage_mod = 1
        self.bullet_speed = 20
        self.fire_rate = 5

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

    # update gun
    def update(self, player_dir, target_unit_vector, player_pos, enemie_group, fire, damage):
        unit_vector = Point.rotate_unit_vector_flip(target_unit_vector, self.angle_on_player, self.front.dir)
        self.pos.x = player_pos.x + self.offset * unit_vector.x
        self.pos.y = player_pos.y + self.offset * unit_vector.y

        # point in correct direction
        self.face_target(player_dir)
        
        # run shooting script
        self.shoot(player_dir, target_unit_vector, fire)

        # update projectiles
        for projectile in self.projectiles:
            projectile.update(enemie_group, self.gun_damage_mod * damage)