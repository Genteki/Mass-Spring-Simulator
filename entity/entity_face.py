import numpy as np
from physics import *
from ursina import *

class EntityFace(Entity):
    def __init__(self, ms, **kwargs):
        super().__init__()
        self.mass = ms
        self.verts = []
        for m in self.mass:
            self.verts.append([m.p[0], m.p[2], m.p[1]])
        self.tris = (0,1,2,3,2,1)#(1, 2, 0, 2, 3, 0)
        self.uvs = None #((1.0, 0.0), (0.0, 1.0), (0.0, 0.0), (1.0, 1.0))
        self.norms = ((0,0,1),) * len(self.verts)
        self.colors = color.gray
        self.alpha = 1
        self.model = Mesh(vertices=self.verts, triangles=self.tris, uvs=self.uvs, normals=self.norms, colors=self.colors, mode='ngon')
        # self.color = color.gray
        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        self.verts.clear()
        for m in self.mass:
            self.verts.append([m.p[0], m.p[2], m.p[1]])
        self.model.vertices = self.verts
        self.model.generate()
