import pygame
import numpy
from config import *

# clas that returns the correct image for each senario
class Animation:
    # normal 
    def __init__(self, frames, size, tempo):
        # makeing sure to copy to prevent referencing errors
        self.frames = numpy.array(frames.copy())
        self.sizes = numpy.array([size for i in range(len(self.frames))])
        self.tempo = numpy.array(tempo.copy())

        # framedata
        self.frame = 0
        self.clock = 0
        self.frame_clock = self.tempo[self.frame]
        self.tick = FRAMERATE
        self.end_tick = self.tempo.sum() * self.tick

        self.length = len(frames)

    # play animaiton, returns a image object, to be used when drawn
    def animate(self):
        if self.clock > self.frame_clock * self.tick:
            self.frame += 1
            self.frame_clock += self.tempo[self.frame]

        
        if self.clock >= self.end_tick:
            # reset animation
            self.frame = 0
            self.clock = 0
            self.frame_clock = self.tempo[self.frame]
        else:
            self.clock += 1

        # return image
        return_image = pygame.transform.scale(pygame.image.load(self.frames[self.frame]).convert_alpha(), self.sizes[self.frame])
        return return_image
    
    def get_completed(self):
        if self.clock >= self.end_tick:
            # reset animation
            self.frame = 0
            self.clock = 0
            self.frame_clock = self.tempo[self.frame]
            return True
        
        return False
    
    # sets animation to start of frame
    def set_frame(self, frame):
        self.frame = 0
        self.frame_clock = self.tempo[0:self.frame+1].sum()
        self.clock = self.tempo[0:self.frame].sum() * self.tick
