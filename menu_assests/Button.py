import pygame
from classes.Point import Point

class Button(pygame.sprite.Sprite):
    def __init__(self, text, x, y, font_size=32, padding=(20, 20, 20, 20)):
        super(Button, self).__init__()
        self.pos = Point(x, y)

        # text
        self.font = pygame.font.Font(None, 64)
        self.button_text = pygame.font.Font.render(self.font, text, 1, (20, 20, 20))

        # up down top left for padding
        self.width = self.button_text.get_rect().width + padding[1] + padding[3]
        self.height = self.button_text.get_rect().height + padding[0] + padding[2]
        self.base_surf = pygame.Surface((self.width, self.height))
        self.base_surf.fill((255, 255, 255))
        self.surf = self.base_surf
        self.rect = self.base_surf.get_rect(center=(
            self.pos.x,
            self.pos.y,
        ))

        self.pressed = False
        self.hover = False

        self.base_surf.blit(self.button_text, (
            self.rect.width/2 - self.button_text.get_rect().width/2,
            self.rect.height/2 - self.button_text.get_rect().height/2
        ))


    # false means no click, true means click
    def draw(self, screen):
        screen.blit(self.surf, self.rect)

    # kill button
    def die(self):
        self.kill()

    # checking if button is pressed
    def update(self, events):
        # if mouse is over object
        mx, my = pygame.mouse.get_pos()
        if self.rect.collidepoint(mx, my) == False:
            if self.hover:
                # return to noraml size
                self.hover = False
                self.surf = self.base_surf
                pass
            return False

        # if over slightly enlarge or change button
        if self.hover == False:
            self.hover = True
            self.surf = pygame.transform.scale_by(self.base_surf, 1.05)
            # enlarge button

        # if mouse is pressed over object
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
            
        return False
        