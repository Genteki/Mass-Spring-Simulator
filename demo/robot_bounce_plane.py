import os, sys
sys.path.append(os.getcwd())

import numpy as np
from physics.objects import *
from ursina import *
from physics import *
from entity import *
from utils import *
from robot import *
from phasec_disable import disable_param_332

if __name__ == '__main__':
    if len(sys.argv) == 1:
        pk = 'ori'
    else:
        pk = sys.argv[1]
    robot = VariableRobot(x=3,y=3,z=2,k_spring=10000, disable=disable_param_332[pk])
    offset = np.array([0,0,1])
    sim = Simulator(mass=robot.mass, spring=robot.spring, k_ground=1, damping=0.9999)
    for m in sim.mass:
        m.p = m.p + offset

    d=.1
    timestep=24
    app = Ursina()
    m_app = []; s_app = []; f_app = []
    for m in sim.mass:
        m_app.append(Entity(model="sphere", scale=d, x=m.p[0], y=m.p[2], z=m.p[1],texture="white_cube"))
    # for s in sim.spring:
    #     if np.linalg.norm(s.m1.p-s.m2.p, ord=2) <= 1.1:
    #         s_app.append(EntitySpring(s, m_app))
    for f in robot.face:
        f_app.append(EntityFace(f))


    plane = Entity(model="plane", scale=(20,1,20),y=-d/2,texture="white_cube", texture_scale=(20,20))
    # l1 = PointLight(x=30, y=20)
    # pivot = Entity()
    #DirectionalLight(parent=pivot, y=2, z=3, shadows=False)
    #SpotLight(parent=pivot,y=2,z=3,shadows=True)
    EditorCamera()

    def update():
        for i in range(timestep):
            sim.simulate()
        for i, m in enumerate(sim.mass):
            if not m.disable:
                m_app[i].position = Vec3(m.p[0], m.p[2],m.p[1])

    app.run()
