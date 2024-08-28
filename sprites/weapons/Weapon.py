import pygame
from classes.Point import Point
from classes.Direction import Direction
from config import FRAMERATE

class Weapon(pygame.sprite.Sprite):
    def __init__(self, pos, image_url, size, bg_pos):
        super(Weapon, self).__init__()

        # center
        self.pos = pos.copy()
        self.front = Direction(0)
        self.offset = 0

        self.image = pygame.transform.scale(pygame.image.load(image_url).convert_alpha(), (size[0], size[1]))
        self.base_image = self.image
        self.hitbox_rect = self.base_image.get_rect(center=(
            self.pos.x + bg_pos.x, 
            -self.pos.y + bg_pos.y
        ))
        self.rect = self.hitbox_rect.copy()

        # general
        self.width = size[0]
        self.height = size[1]
        self.angle_on_player = 0

        self.fire_rate = 1
        self.frame_till_fire = 0

        # autofire
        self.autofire = False
        self.fire = False

        # projectiles if any
        self.projectiles = pygame.sprite.Group()

    # face target
    def face_target(self, target_dir):
        # copy target direction
        self.front.dir = target_dir.dir

        # move image
        self.image = Direction.rotate_with_flip(self.front.dir, self.base_image)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)

    # check if can attack
    def can_attack(self):
        if self.frame_till_fire <= 0:
            return True
        
        self.frame_till_fire -= 1
        return False
    
    # check if need to attack
    def do_attack(self, fire):
        if fire or self.autofire:
            fire_rate = FRAMERATE * 1/self.fire_rate
            self.frame_till_fire = fire_rate
            return True
        return False
    
    # boundary collision detect on projectiles
    def boundary_collision(self, boundary):
        for bullet in self.projectiles:
            for tile in boundary:
                if pygame.Rect.colliderect(bullet.hitbox_rect, tile.rect):
                    if tile.shoot_through == False:
                        bullet.collision(tile.rect)
                        break

        





