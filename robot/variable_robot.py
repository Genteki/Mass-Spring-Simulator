import os, sys
sys.path.append(os.getcwd())

from physics.objects import *
import numpy as np

class VariableRobot():
    def __init__(self, x, y, z, k_spring=1000, m=1, disable=[]):
        self.mass = []
        self.spring = []
        self.disable = disable
        self.able = []
        self.k = k_spring
        self.m = m
        self.x = x
        self.y = y
        self.z = z

        for i in range(x):
            for j in range(y):
                for k in range(z):
                    if not [i,j,k] in disable:
                        self.able.append([i,j,k])

        for i in range(x+1):
            for j in range(y+1):
                for k in range(z+1):
                    p = np.array([i, j, k])
                    self.mass.append(Mass(self.m, p))
                    # m2 = self.mass[-1]
        self.mass_dispt = np.zeros_like(self.mass)
        for i in range(len(self.mass_dispt)):
            self.mass_dispt[i] = 8
            if not np.logical_and((self.mass[i].p-np.array([0,0,0])), (self.mass[i].p-np.array([x,y,z]))).any():
                self.mass_dispt[i] = 1
            elif np.logical_and((self.mass[i].p-np.array([0,0,0])), (self.mass[i].p-np.array([x,y,z]))).sum()==2:
                self.mass_dispt[i] = 4
            elif np.logical_and((self.mass[i].p-np.array([0,0,0])), (self.mass[i].p-np.array([x,y,z]))).sum()==1:
                self.mass_dispt[i] = 2


        for dp in disable:
            for i in range(dp[0], dp[0]+2):
                for j in range(dp[1], dp[1]+2):
                    for k in range(dp[2], dp[2]+2):
                        self.mass_dispt[i*(y+1)*(z+1)+j*(z+1)+k] -= 1

        for i in range(len(self.mass_dispt)):
            if self.mass_dispt[i] == 0:
                self.mass[i].disable = True

        # find spring
        for i in range(len(self.mass)):
            for j in range(i+1, len(self.mass)):
                if (np.linalg.norm(self.mass[i].p-self.mass[j].p, ord=2) < 1.8):
                    if self.is_able_spring(self.mass[i], self.mass[j]):
                            self.spring.append(Spring(self.mass[i],
                                                  self.mass[j],
                                                  np.linalg.norm(self.mass[i].p-self.mass[j].p, ord=2),
                                                  k_spring))

        # find face
        self.face = []
        # porint 0
        # for i in range(len(self.mass)):
        #     # point 1
        #     for j in range(len(self.mass)):
        #         if not (self.mass[i].p - self.mass[j].p + np.array([1., 0, 0])).any():
        #             # point 3
        #             for k in range(len(self.mass)):
        #                 if not (self.mass[i].p - self.mass[k].p + np.array([0, 1., 0])).any():
        #                     #point 2
        #                     for r in range(len(self.mass)):
        #                         if not (self.mass[i].p - self.mass[r].p + np.array([1., 1., 0])).any():
        #                             if not (self.mass[i].disable and self.mass[j].disable and self.mass[k].disable or self.mass[r].disable):
        #                                 self.face.append([self.mass[i], self.mass[j], self.mass[r], self.mass[k]])
        #                 if not (self.mass[i].p - self.mass[k].p + np.array([0, 0, 1.])).any():
        #                     # point 2
        #                     for r in range(len(self.mass)):
        #                         if not (self.mass[i].p - self.mass[r].p + np.array([1., 0, 1.])).any():
        #                             if not (self.mass[i].disable and self.mass[j].disable and self.mass[k].disable or self.mass[r].disable):
        #                                 self.face.append([self.mass[i], self.mass[j], self.mass[r], self.mass[k]])
        #         elif not (self.mass[i].p - self.mass[j].p + np.array([0, 1., 0])).any():
        #             # point 3
        #             for k in range(len(self.mass)):
        #                 if not (self.mass[i].p - self.mass[k].p + np.array([0, 0, 1.])).any():
        #                     # point 2
        #                     for r in range(len(self.mass)):
        #                         if not (self.mass[i].p - self.mass[r].p + np.array([0, 1., 1.])).any():
        #                             if not (self.mass[i].disable and self.mass[j].disable and self.mass[k].disable and self.mass[r].disable):
        #                                 self.face.append([self.mass[i], self.mass[j], self.mass[r], self.mass[k]])
        for i in range(x):
            for j in range(y):
                for k in range(z):
                    if not [i,j,k] in self.disable:
                        self.face.append([self.massid(i,j,k), self.massid(i+1,j,k), self.massid(i+1,j+1,k), self.massid(i,j+1,k)])
                        self.face.append([self.massid(i,j,k+1), self.massid(i+1,j,k+1), self.massid(i+1,j+1,k+1), self.massid(i,j+1,k+1)])
                        self.face.append([self.massid(i,j,k), self.massid(i+1,j,k), self.massid(i+1,j,k+1), self.massid(i,j,k+1)])
                        self.face.append([self.massid(i,j,k), self.massid(i,j,k+1), self.massid(i,j+1,k+1), self.massid(i,j+1,k)])
                        self.face.append([self.massid(i+1,j,k), self.massid(i+1,j,k+1), self.massid(i+1,j+1,k+1), self.massid(i+1,j+1,k)])
                        self.face.append([self.massid(i,j+1,k), self.massid(i+1,j+1,k), self.massid(i+1,j+1,k+1), self.massid(i,j+1,k+1)])

    def get_center(self):
        center = np.array([0.,0.,0.])
        for m in self.mass:
            center = center + m.p
        center = center / len(self.mass)
        return center

    def massid(self, i, j, k):
        return self.mass[(self.z+1)*(self.y+1)*i + (self.z+1)*j + k]
        # for l in self.mass:
        #     if not (l.p - np.array([i,j,k])).any():
        #         return l
        # return None

    def is_able_spring(self, m1, m2):
        if np.linalg.norm(m1.p - m2.p, ord=2) > 1.8:
            return False
        for da in self.able:
            if ((m1.p - np.array(da))>=np.array([-.1,-.1,-.1])).all() and ((m1.p - np.array(da))<=np.array([1.1,1.1,1.1])).all():
                if ((m2.p - np.array(da))>=np.array([-.1,-.1,-.1])).all() and ((m2.p - np.array(da))<=np.array([1.1,1.1,1.1])).all():
                    return True
        return False

    def set_spring_param(self, spring_param):
        for i, sp in enumerate(spring_param):
            self.spring[i].k = spring_param[i, 2]
