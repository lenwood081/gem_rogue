import pygame
from classes.Point import Point

class Button(pygame.sprite.Sprite):
    def __init__(self, image_url, x, y, width, height):
        super(Button, self).__init__()
        self.width = width
        self.height = height
        self.pos = Point(x, y)
        self.image = pygame.image.load(image_url).convert_alpha()
        self.rect = self.image.get_rect(center=(
            self.pos.x,
            self.pos.y,
        ))

        self.pressed = False
        self.hover = False

    # false means no click, true means click
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # kill button
    def die(self):
        self.kill()

    def update(self):
        # if mouse is over object
        mx, my = pygame.mouse.get_pos()
        if self.rect.collidepoint(mx, my) == False:
            if self.hover:
                # return to noraml size
                self.hover = False
                pass
            return False
        
        # if over slightly enlarge or change button
        if self.hover == False:
            self.hover = True
            # enlarge button

        # if mouse is pressed over object
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
            
        return False
        