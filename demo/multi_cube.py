import os, sys
sys.path.append(os.getcwd())

import numpy as np
from physics.objects import *
from ursina import *
from physics import *
from entity.entity_spring import *
from utils import *

def rand_rot():
    return (Rot(2 * np.pi * np.random.rand(),"x") @
            Rot(2 * np.pi * np.random.rand(),"x") @
            Rot(2 * np.pi * np.random.rand(),"x"))
vertices = []

for i in range(2):
    for j in range(2):
        for k in range(2):
            vertices.append([i,j,k])
vectices = np.array(vertices)

p0 = np.array([0., 0., 5.])
trans_p = np.array([[-3., 2., 0.], [0.,2.,1.], [-2., 0, -0.5], [0, -2,-2]])
timestep = 24
mass = []
spring = []
k0 = 10000
T = 200
d = 0.2
for k, t in enumerate(trans_p):
    R = rand_rot()
    for vertex in vertices:
        v = np.cross(np.array([0,0,10*np.random.rand()*np.pi*2-10*np.pi]), np.array(vertex) - np.array([0.5,0.5,0.5]) )
        mass.append(Mass(1., R@vertex+p0+t, v=R@v))
    for i in range(8*k, 8+8*k):
        for j in range(i+1, 8+8*k):
            spring.append(Spring(mass[i],mass[j],distance(mass[i].p,mass[j].p),k0))
sim = Simulator(mass=mass, spring=spring, k_ground=1, damping=0.9999)

app = Ursina()
m_app = []; s_app = []
for m in sim.mass:
    m_app.append(Entity(model="sphere", scale=d, x=m.p[0], y=m.p[2], z=m.p[1],texture="white_cube"))
for s in sim.spring:
    if np.linalg.norm(s.m1.p-s.m2.p, ord=2) <= 1.1:
        s_app.append(EntitySpring(s, m_app))
plane = Entity(model="plane", scale=(20,1,20),y=-d/2,texture="white_cube", texture_scale=(20,20))
l1 = PointLight(x=30, y=20)
pivot = Entity()
#DirectionalLight(parent=pivot, y=2, z=3, shadows=False)
#SpotLight(parent=pivot,y=2,z=3,shadows=True)
EditorCamera()

def update():
    for i in range(timestep):
        for j in sim.spring:
            j.l0 = j.l00 + j.l00 / 2 * np.sin(sim.t / T * 2 * np.pi)
        sim.simulate()
    for i, m in enumerate(sim.mass):
        m_app[i].position = Vec3(m.p[0], m.p[2],m.p[1])

app.run()
