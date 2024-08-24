import pygame
from classes.Point import Point
from sprites.Weapon import Weapon
from sprites.projectiles.WhiteBullet import WhiteBullet


class BasicGun(Weapon):
    def __init__(self, pos, bg_pos):
        super(BasicGun, self).__init__(pos, "assets/weapons/Basic_gun.png", 70, 100, bg_pos) 

        # white bullets
        self.projectiles = pygame.sprite.Group()
        self.damage = 1
        self.bullet_speed = 20
        self.fire_rate = 5

        # offeset from player (for basic gun this is zero due to the way it is drawn)
        self.offset = 0

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
    def shoot(self, player_dir, target_unit_vector, fire):
        if self.can_attack(): 
            if self.do_attack(fire):
                new_projectile = WhiteBullet(self.pos, target_unit_vector, player_dir, self.damage, self.bullet_speed)
                self.projectiles.add(new_projectile)
                

    # update gun
    def update(self, player_dir, target_unit_vector, player_pos, enemie_group, fire):
        unit_vector = Point.rotate_unit_vector_flip(target_unit_vector, self.angle_on_player, self.front.dir)
        self.pos.x = player_pos.x + self.offset * unit_vector.x
        self.pos.y = player_pos.y + self.offset * unit_vector.y

        # point in correct direction
        self.face_target(player_dir)
        
        # run shooting script
        self.shoot(player_dir, target_unit_vector, fire)

        # update projectiles
        for projectile in self.projectiles:
            projectile.update(enemie_group)
