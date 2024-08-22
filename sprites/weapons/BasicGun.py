import pygame
from classes.Point import Point
from sprites.Weapon import Weapon
from sprites.projectiles.WhiteBullet import WhiteBullet


class BasicGun(Weapon):
    def __init__(self, pos, bg_pos):
        super(BasicGun, self).__init__(pos, "assets/player/Basic_gun.png", 70, 100, bg_pos) 

        # white bullets
        self.projectiles = pygame.sprite.Group()
        self.damage = 1
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

    # shoots a bullet
    def shoot(self, player_dir, target_unit_vector):
        if self.can_attack():
            new_projectile = WhiteBullet(self.pos, target_unit_vector, player_dir, 1, self.bullet_speed)
            self.projectiles.add(new_projectile)

    # update gun
    def update(self, player_dir, target_unit_vector, player_pos, enemie_group):
        self.pos.x = player_pos.x
        self.pos.y = player_pos.y

        # point in correct direction
        self.face_target(player_dir)

        self.shoot(player_dir, target_unit_vector)

        # update projectiles
        for projectile in self.projectiles:
            projectile.update(enemie_group)
