import pygame
import numpy
from config import *

# clas that returns the correct image for each senario
class Animation:
    # for cases where the size changes
    def __init__(self, frames, size, size_per_frame_ratio, tempo):
        pass
    
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

    # play animaiton, returns a image object, to be used when drawn
    def animate(self):
        if self.clock > self.frame_clock * self.tick:
            self.frame += 1
            self.frame_clock += self.tempo[self.frame]

        if self.clock >= self.end_tick:
            # end of animation => reset
            self.frame = 0
            self.clock = 0
            self.frame_clock = self.tempo[self.frame]
        else:
            self.clock += 1

        # return image
        return_image = pygame.transform.scale(pygame.image.load(self.frames[self.frame]).convert_alpha(), self.sizes[self.frame])
        return return_image
