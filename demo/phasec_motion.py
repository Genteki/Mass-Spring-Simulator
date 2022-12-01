import os, sys
sys.path.append(os.getcwd())

import numpy as np
from physics import *
from robot import *
from entity import *
from ursina import *
from evolution import *


if __name__ == '__main__':
    if sys.argc == 0:

    ga = GA_C(k_spring=500, omega=2, l0_amplitude=0.5, p0_range=0.1,
               friction=0.7, robot_shape = [3,3,2], m=1, pop_size=150)
    robot = VariableRobot(ga.robot_shape[0], ga.robot_shape[1], ga.robot_shape[2], m=ga.m)
    print(ga.spring_params.shape)
    for i in range(len(robot.spring)):
        robot.spring[i].k = ga.spring_params[0,i,2]
    ga.sim.reset(robot.mass, robot.spring)
    app = Ursina()

    d=.1
    timestep=int(1/ga.sim.dt/24)
    m_app = []; s_app = []
    # for m in ga.sim.mass:
    #     m_app.append(Entity(model="sphere", scale=d, x=m.p[0], y=m.p[2], z=m.p[1],texture="white_cube"))
    # for s in ga.sim.spring:
    #     if np.linalg.norm(s.m1.p-s.m2.p, ord=2) <= 1.1:
    #         s_app.append(EntitySpring(s, m_app, resolution=4))
    f_app=[]
    for f in robot.face:
        f_app.append(EntityFace(f, alpha=1))
    plane = Entity(model="plane", scale=(20,1,20),y=-d/2,texture="white_cube", texture_scale=(20,20))
    # l1 = PointLight(x=30, y=20)
    # pivot = Entity()
    EditorCamera()

    def update():
        for i in range(timestep):
            for j, s in enumerate(ga.sim.spring):
                s.l0 = s.l00 * (1 + ga.spring_params[0,j,0] * np.sin(ga.omega*ga.sim.t+ga.spring_params[0,j,1]))
            ga.sim.simulate()
        # for i, m in enumerate(ga.sim.mass):
        #     m_app[i].position = Vec3(m.p[0], m.p[2],m.p[1])

    app.run()
