import os, sys
sys.path.append(os.getcwd())

import numpy as np
from physics.objects import *
from ursina import *
from physics import *
from entity.entity_spring import *
from utils import *
from robot.robot import *

robot = CubeRobot(x=1,y=1,z=1,k_spring=1e4)
offset = np.array([0,0,4.])
sim = Simulator(mass=robot.mass, spring=robot.spring, k_ground=1, damping=0.9999,dt=1/2400)
for m in sim.mass:
    m.p = m.p + offset

d=.1
timestep=100
app = Ursina()
m_app = []; s_app = []
for m in sim.mass:
    m_app.append(Entity(model="sphere", scale=d, x=m.p[0], y=m.p[2], z=m.p[1],texture="white_cube"))
for s in sim.spring:
    if np.linalg.norm(s.m1.p-s.m2.p, ord=2) <= 1.1:
        s_app.append(EntitySpring(s, m_app, resolution=4))
plane = Entity(model="plane", scale=(20,1,20),y=-d/2,texture="white_cube", texture_scale=(20,20))
l1 = PointLight(x=30, y=20)
pivot = Entity()
#DirectionalLight(parent=pivot, y=2, z=3, shadows=False)
#SpotLight(parent=pivot,y=2,z=3,shadows=True)
EditorCamera()

# def update():
#     for i in range(timestep):
#         sim.simulate()
#     for i, m in enumerate(sim.mass):
#         m_app[i].position = Vec3(m.p[0], m.p[2],m.p[1])

app.run()
