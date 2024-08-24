import pygame
from sprites.Weapon import Weapon
from sprites.projectiles.GlowBullet import GlowBullet

# TODO make plasma bullets hit bigger (normal need to be made to only hit once)
class PlasmaGun(Weapon):
    def __init__(self, pos, bg_pos):
        super(PlasmaGun, self).__init__(pos, "assets/weapons/PlasmaGun.png", 32, 28, bg_pos) 

        # white bullets
        self.projectiles = pygame.sprite.Group()
        self.damage = 2
        self.bullet_speed = 20
        self.fire_rate = 4

        # offeset from player (for basic gun this is zero due to the way it is drawn)
        self.offset = 30

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
                new_projectile = GlowBullet(self.pos, target_unit_vector, player_dir, self.damage, self.bullet_speed)
                self.projectiles.add(new_projectile)
                

    # update gun
    def update(self, player_dir, target_unit_vector, player_pos, enemie_group, fire):
        self.pos.x = player_pos.x + self.offset * target_unit_vector.x
        self.pos.y = player_pos.y + self.offset * target_unit_vector.y

        # point in correct direction
        self.face_target(player_dir)
        
        # run shooting script
        self.shoot(player_dir, target_unit_vector, fire)

        # update projectiles
        for projectile in self.projectiles:
            projectile.update(enemie_group)
