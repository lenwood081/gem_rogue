import pygame
from utility.Point import Point
from config import FRAMERATE

class Particle(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y, duration):
        super().__init__()

        # base blit 
        self.width, self.height = w, h
        self.blit_surf = pygame.Surface((w, h)).convert_alpha()
        self.blit_rect = self.blit_surf.get_rect(center=(x, y))
        
        self.pos = Point(x, y)
        self.duration = duration
        self.time_alive = 0

    # draw method
    def draw(self, screen, cam_offset):
        self.blit_rect.center = (self.pos.x + cam_offset.x, -self.pos.y + cam_offset.y)
        screen.blit(self.blit_surf, self.blit_rect)

    # update method (override)
    def update(self, dt):
        if self.time_alive >= self.duration:
            self.kill() 
        self.time_alive += 1 / FRAMERATE * dt


# ------------------------------------------------------------------------------------------

class HollowParticle(Particle):
    def __init__(self, w, x, y, color=(0, 255, 0), duration=3, width=5, alpha=255, follow=False):
        super().__init__(w, w, x, y, duration=duration) 

        # two cicles, one is the transperant color  
        self.radius_outside = 0
        self.radius_inside = 0
        self.radius_grow_rate = (w/2 / self.duration) / FRAMERATE
        self.blit_surf.set_colorkey((0, 0, 0))
        self.blit_surf.set_alpha(alpha)
        self.color = color
        self.rad_width = width
        self.follow = follow
        

    # update
    def update(self, dt):
        if self.follow:
            return
        super().update(dt)

        # circle drawing
        pygame.draw.circle(self.blit_surf, self.color, (self.width/2, self.height/2), self.radius_outside)
        pygame.draw.circle(self.blit_surf, (0, 0, 0), (self.width/2, self.height/2), self.radius_inside)

        self.radius_outside += self.radius_grow_rate * dt
        self.radius_inside = max(self.radius_outside - self.rad_width, 0)

        

    # update with position
    def update_with_follow(self, dt, x, y):
        
        super().update(dt)
        self.pos.x = x
        self.pos.y = y
        
        # circle drawing
        pygame.draw.circle(self.blit_surf, self.color, (self.width/2, self.height/2), self.radius_outside)
        pygame.draw.circle(self.blit_surf, (0, 0, 0), (self.width/2, self.height/2), self.radius_inside)

        self.radius_outside += self.radius_grow_rate * dt
        self.radius_inside = max(self.radius_outside - self.rad_width, 0)


# ------------------------------------------------------------------------------------------

class HitCircle(Particle):
    def __init__(self, w, x, y, color=(1, 1, 1), duration=0.1, width=3, alpha=255):
        super().__init__(w, w, x, y, duration=duration)

        self.inner_color = color
        self.outer_color = (255- color[0], 255- color[1], 255- color[2])

        # two cicles, one is the border
        self.radius_outside = w/2
        self.radius_inside = w/2 - width
        self.radius_grow_rate = (w/2 / self.duration) / FRAMERATE
        self.blit_surf.set_colorkey((0, 0, 0))
        self.blit_surf.set_alpha(alpha)

    # update
    def update(self, dt):
        super().update(dt)

        # circle drawing
        pygame.draw.circle(self.blit_surf, self.outer_color, (self.width/2, self.height/2), self.radius_outside)
        pygame.draw.circle(self.blit_surf, self.inner_color, (self.width/2, self.height/2), self.radius_inside)
        

    



        



