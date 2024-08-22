import pygame
from classes.Point import Point
from sprites.Weapon import Weapon
from sprites.Projectile import Projectile

class BasicGun(Weapon):
    def __init__(self, pos_screen, pos):
        self.pos_screen = Point(pos_screen.x, pos_screen.y)
        self.pos = Point(pos.x, pos.y)
        super(BasicGun, self).__init__(pos_screen, pos, "assets/player/Basic_gun.png", 70, 100) 
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
        new_projectile = Projectile(self.pos.x, self.pos.y, 300, target_unit_vector, player_dir, "assets/Projectiles/White_bullet.png", 6, 12)
        self.projectiles.add(new_projectile)

    # update gun
    def update(self, player_dir, target_unit_vector, player_pos):
        self.pos.x = player_pos.x
        self.pos.y = player_pos.y

        # point in correct direction
        self.face_target(player_dir)

        self.shoot(player_dir, target_unit_vector)

        # update projectiles
        for projectile in self.projectiles:
            projectile.update()
