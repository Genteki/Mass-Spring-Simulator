import os, sys
sys.path.append(os.getcwd())

import numpy as np
from physics import *
from robot import *
from entity import *
from ursina import *
from evolution.ga import GA
from datetime import datetime

rbt_params_1 = np.load("output/cube3-1130/phaseb/gen50.npy")
# rbt_params_2 = np.load("output/cube6-1114/phaseb/gen11.npy")

robot1 = CubeRobot(x=3,y=1,z=1)


#
for i in range(len(rbt_params_1)):
    rbt_params_1[i,2]+=10
# for i in range(len(rbt_params_2)):
#     rbt_params_2[i,2]+=30
for m in robot1.mass:
    m.p+= np.array([-2, 0, 0])
for i, spring in enumerate(robot1.spring):
    robot1.spring[i].k = rbt_params_1[i,2]



sim = Simulator(k_ground=0.4, dt=0.0004, damping=0.999,friction_s=0.8, friction_ground=0.8)
for m in robot1.mass:
    sim.mass.append(m)

for s in robot1.spring:
    sim.spring.append(s)


app =Ursina()


d=.1
timestep=int(1/sim.dt/60)
m_app = []; s_app = []
for m in robot1.mass:
    m_app.append(Entity(model="sphere", scale=d, x=m.p[0], y=m.p[2], z=m.p[1],texture="white_cube",color=color.gray))

f_app=[]
for f in robot1.face:
    f_app.append(EntityFace(f, color=color.black, alpha=.5))

plane = Entity(model="plane", scale=(20,1,20),y=-d/2,texture="white_cube", texture_scale=(20,20))
# l1 = PointLight(x=30, y=20)
# pivot = Entity()
EditorCamera()

def update():
    for i in range(timestep):
        for j, s in enumerate(robot1.spring):
            s.l0 = s.l00 * (1 + rbt_params_1[j,0] * np.sin(2*sim.t+rbt_params_1[j,1]*np.pi*2))

        sim.simulate()

    for i, m in enumerate(sim.mass):
        m_app[i].position = Vec3(m.p[0], m.p[2],m.p[1])

app.run()
