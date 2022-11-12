import numpy as np
from physics import *
from ursina import *

class EntitySpring(Entity):
    def __init__(self, spring, ms, resolution=10, **kwargs):
        super().__init__()
        self.spring = spring
        self.model = Pipe(base_shape=Circle(resolution=resolution,radius=0.04),
                          origin=(0,0), path=((self.spring.m1.p[0], self.spring.m1.p[2],self.spring.m1.p[1]),
                          (self.spring.m2.p[0], self.spring.m2.p[2], self.spring.m2.p[1])), thicknesses=(1,1))
        self.color = color.white
        self.alpha = 0.3
        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_parent(self, ms):
        for m in ms:
            if m.x == self.spring.m1.p[0] and m.y == self.spring.m1.p[2] and m.z == self.spring.m1.p[1]:
                self.reparent_to(m)
                self.model = Pipe(base_shape=Circle(resolution=10,radius=0.04),
                                  origin=(0,0), path=((0,0,0),
                                  (self.spring.m2.p[0] - self.spring.m1.p[0],
                                   self.spring.m2.p[2] - self.spring.m1.p[2],
                                   self.spring.m2.p[1] - self.spring.m1.p[1])), thicknesses=(1,1))
    def update(self):
        compress_rate = (distance(self.spring.m1.p, self.spring.m2.p) - self.spring.l0) / self.spring.l0
        new_rad = 0.04 - 0.08 *compress_rate
        if new_rad < 0.01: new_rad = 0.01
        if new_rad > 0.16: new_rad = 0.16
        self.model = Pipe(base_shape=Circle(resolution=10,radius=new_rad),
                          origin=(0,0), path=((self.spring.m1.p[0], self.spring.m1.p[2],self.spring.m1.p[1]),
                          (self.spring.m2.p[0], self.spring.m2.p[2], self.spring.m2.p[1])), thicknesses=(1,1))
        self.alpha = 0.5 - 1 * (compress_rate)
        if self.alpha >= 1: self.alpha = .99
        if self.alpha <= 0.2: self.alpha = 0.2
        # self.model = Pipe(base_shape=Circle(resolution=10,radius=0.04),
        #                   origin=(0,0), path=((0,0,0),
        #                   (self.spring.m2.p[0] - self.spring.m1.p[0],
        #                    self.spring.m2.p[2] - self.spring.m1.p[2],
        #                    self.spring.m2.p[1] - self.spring.m1.p[1])), thicknesses=(1,1))
