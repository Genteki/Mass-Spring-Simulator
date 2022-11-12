import os, sys
sys.path.append(os.getcwd())

from physics.objects import *
import numpy as np

class CubeRobot():
    def __init__(self, x=1, y=1, z=1, k_spring=500, m=1):
        self.mass = []
        self.spring = []
        self.k = k_spring
        self.m = m

        for i in range(x+1):
            for j in range(y+1):
                for k in range(z+1):
                    p = np.array([i, j, k])
                    self.mass.append(Mass(self.m, p))
                    m2 = self.mass[-1]
        # find spring
        for i in range(len(self.mass)):
            for j in range(i+1, len(self.mass)):
                if np.linalg.norm(self.mass[i].p-self.mass[j].p, ord=2) < np.sqrt(3) + 0.1:
                    self.spring.append(Spring(self.mass[i],
                                              self.mass[j],
                                              np.linalg.norm(self.mass[i].p-self.mass[j].p, ord=2),
                                              k_spring))
        # find face
        self.face = []
        # porint 0
        for i in range(len(self.mass)):
            # point 1
            for j in range(len(self.mass)):
                if not (self.mass[i].p - self.mass[j].p + np.array([1., 0, 0])).any():
                    # point 3
                    for k in range(len(self.mass)):
                        if not (self.mass[i].p - self.mass[k].p + np.array([0, 1., 0])).any():
                            #point 2
                            for r in range(len(self.mass)):
                                if not (self.mass[i].p - self.mass[r].p + np.array([1., 1., 0])).any():
                                    self.face.append([self.mass[i], self.mass[j], self.mass[r], self.mass[k]])
                        if not (self.mass[i].p - self.mass[k].p + np.array([0, 0, 1.])).any():
                            # point 2
                            for r in range(len(self.mass)):
                                if not (self.mass[i].p - self.mass[r].p + np.array([1., 0, 1.])).any():
                                    self.face.append([self.mass[i], self.mass[j], self.mass[r], self.mass[k]])
                elif not (self.mass[i].p - self.mass[j].p + np.array([0, 1., 0])).any():
                    # point 3
                    for k in range(len(self.mass)):
                        if not (self.mass[i].p - self.mass[k].p + np.array([0, 0, 1.])).any():
                            # point 2
                            for r in range(len(self.mass)):
                                if not (self.mass[i].p - self.mass[r].p + np.array([0, 1., 1.])).any():
                                    self.face.append([self.mass[i], self.mass[j], self.mass[r], self.mass[k]])
        # print("face: ", len(self.face))
        # for f in self.face:
        #     print(f[0].p, f[1].p, f[2].p, f[3].p)


    def get_center(self):
        center = np.array([0.,0.,0.])
        for m in self.mass:
            center = center + m.p
        center = center / len(self.mass)
        return center

    def set_spring_param(self, spring_param):
        for i, sp in enumerate(spring_param):
            self.spring[i].k = spring_param[i, 2]
