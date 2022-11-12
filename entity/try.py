from ursina import *
import numpy as np
from ursina.shaders import normals_shader
from ursina.shaders import lit_with_shadows_shader

d = 0.2
vertices = []
for i in range(2):
    for j in range(2):
        for k in range(2):
            vertices.append([i,j,k])

def cylinder(pta, ptb, offset=[0,0,0]):
    return Entity(model=Pipe(base_shape=Circle(resolution=10,radius=0.04),
                  origin=(0,0), path=((pta[0]+offset[0],pta[2]+offset[2],pta[1]+offset[1]),
                   (ptb[0]+offset[0],ptb[2]+offset[2],ptb[1]+offset[1])),
                  thicknesses=(1,1)), color=color.white)

def main():
    app = Ursina()
    v = []
    l = []
    for vertex in vertices:
        v.append(Entity(model="sphere", scale=d, x=vertex[0], y=vertex[2]+d/2, z=vertex[1]))
    pairs = [[0,1], [0,2], [1,3],[2,3], [0,4],[1,5],[2,6],[3,7],[4,5],[4,6],[5,7],[6,7]]
    for p in pairs:
        l.append(cylinder(vertices[p[0]],vertices[p[1]], offset=[0,0,d/2]))
    # link1 = cylinder(vertices[0],vertices[1], offset=[0,0,d/2])
    # link2 = cylinder(vertices[0],vertices[4], offset=[0,0,d/2])
    #link1 = Entity(model=Cylinder(20, start=0, radius=0.05,direction=(0,1,0),height=1), x=0,y=r/2,z=0, color=color.color(1,1,1))
    #link2 = Entity(model=Cylinder(20, stardt=0, radius=0.05,direction=(0,0,1),height=1), x=0,y=r/2,z=0, color=color.color(1,1,1))
    #link1.animate_color((1,1,1,0.5), duration=2, interrupt='finish')
    #link =Entity(model=Pipe(base_shape=Circle(resolution=20,radius=0.04), origin=(0,0),
    #                         path=((0,0,0),(0,1,0)), thicknesses=((1,1))), color=color.white)
    plane = Entity(model="plane", scale=(20,1,20),y=0,texture="white_cube", texture_scale=(20,20))
    l1 = PointLight(x=10, y=10)
    pivot = Entity()
    #DirectionalLight(parent=pivot, y=2, z=3, shadows=False)
    SpotLight(parent=pivot,y=2,z=3,shadows=True)
    EditorCamera()

    app.run()


if __name__ == '__main__':
    main()
