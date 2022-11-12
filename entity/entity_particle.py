import numpy as np
from physics import *
from ursina import *

class EntityParticle(Entity):
    def __init__(self, m, **kwargs):
        super().__init__()
        self.m = m
        self.color = color.white
        for key, value in kwargs.items():
            setattr(self, key, value)
