import pygame
from config import SCALE_FACOTOR

class ItemDisplay:
    def __init__(self, item, x, y):

        # item values
        self.image = None
        if item:
            self.image = item.icon
        
        self.description = item.description

        # create box
        self.width, self.height = 400, 600
        self.base_surf = pygame.Surface((self.width, self.height)).convert_alpha()
        self.base_surf.fill((0, 0, 0))
        self.base_surf.set_alpha(200)
        self.rect = self.base_surf.get_rect(center = (x, y))

        self.image_rect = self.image.get_rect(center=(self.width/2, 100))
        self.base_surf.blit(self.image, self.image_rect)

        # create text
        font = pygame.font.Font(None, 28)
        max_width = self.width - 20
        space = font.size(' ')[0]
        current_width = 0
        current_height = 300
        bagOfWords = self.description.split(" ")
        for word in bagOfWords:
            word_surf = font.render(word, 1, (255, 255, 255))
            word_width, word_height = word_surf.get_size()
            
            if current_width + word_width >= max_width:
                current_width = 0
                current_height += word_height + 5
            
            self.base_surf.blit(word_surf, (current_width+10, current_height))
            current_width += word_width + space

    # draw
    def draw(self, screen):
        screen.blit(self.base_surf, self.rect)

