import pygame
from classes.Point import Point
from sprites.Weapon import Weapon
from sprites.Projectile import Projectile

class BasicGun(Weapon):
    def __init__(self, x, y):
        self.pos_screen = Point(x, y)
        self.pos = Point(0,0)
        super(BasicGun, self).__init__(x, y, "assets/player/Basic_gun.png", 70, 100) 
        self.projectiles = pygame.sprite.Group()


    # blit weapon to screen
    def draw(self, screen, bg_pos):
        # change center to top left
        screen.blit(self.image, self.rect)

        # blit all projectiles
        for projectile in self.projectiles:
            print("drawing")
            projectile.draw(screen, bg_pos)

    def shoot(self, player_dir, target_unit_vector):
        if len(self.projectiles) > 1: 
            return
        new_projectile = Projectile(1000, -1000, 300, target_unit_vector, player_dir, "assets/Projectiles/White_bullet.png", 6, 12)
        self.projectiles.add(new_projectile)

    # update gun
    def update(self, player_dir, target_unit_vector):
        # point in correct direction
        self.face_target(player_dir)

        self.shoot(player_dir, target_unit_vector)

        # update projectiles
        for projectile in self.projectiles:
            projectile.update()
