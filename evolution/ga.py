import os, sys
sys.path.append(os.getcwd())

import numpy as np
from physics import *
from robot import *

class GA:
    def __init__(self, **kwargs):
        # evolving parameters
        self.pop_size = 200
        self.weight_distance = 1.
        self.weight_drift = -0.1
        self.evolve_rate = np.array([0.94, 0.04, 0.02])  # crossover, mutation
        self.select_pressure = 0.04
        # simulation parameters
        self.robot_shape = [2,1,1]
        self.robot = []
        self.friction = 0.8
        self.k_spring = 500
        self.l0_amplitude = 0.4
        self.p0_range = 0.5
        self.omega = 1
        self.m = 1
        self.sim_t = 5

        for key, value in kwargs.items():
            setattr(self, key, value)

        tmp_robot = CubeRobot(self.robot_shape[0], self.robot_shape[1], self.robot_shape[2])
        self.num_spring = len(tmp_robot.spring)
        self.spring_params = np.zeros((self.pop_size, self.num_spring, 3)) # k = 1*(1 + b * sin(omega * (t)+t0))
        self.sim = Simulator(dt=1/2400, k_ground=1, damping=0.999, friction_ground=self.friction, friction_s=self.friction)
        # initial spring_params
        for i in range(self.pop_size):
            for j in range(self.num_spring):
                self.spring_params[i,j,0] = np.random.rand() *  self.l0_amplitude# b
                self.spring_params[i,j,1] = np.random.rand() * 2 * np.pi * self.p0_range # t0
                self.spring_params[i,j,2] = int(np.random.rand() * self.k_spring/200) * 200 # k

        self.fitness = np.zeros(self.pop_size, dtype=np.float64)
        self.best_fitness = 0.
        self.best_param = None
        # self._cal_fitness()
        # self._update_best()

    def cal_fitness(self):
        self._cal_fitness()
        self._update_best()

    def _simulate_robot(self, spring_param, sim_t=0):
        robot = CubeRobot(self.robot_shape[0], self.robot_shape[1], self.robot_shape[2])
        robot.set_spring_param(spring_param)
        self.sim.reset(robot.mass, robot.spring)
        if sim_t == 0: sim_t = self.sim_t

        init_postion = robot.get_center()
        while self.sim.t < sim_t:
             self.sim.simulate()
        final_position = robot.get_center()
        displacement = final_position - init_postion
        return displacement

    def _cal_fitness(self):
        for i, spring_param in enumerate(self.spring_params):
            displacement = self._simulate_robot(spring_param)
            self.fitness[i] = self.weight_distance * displacement[0] + self.weight_drift * displacement[1]
            # sys.stdout.write("*")

    def _update_best(self):
        if self.best_fitness <= self.fitness.max():
            self.best_fitness = self.fitness.max()
            self.best_param = self.spring_params[np.argmax(self.fitness)]

    def _tournament(self):
        tournament_size = int(self.select_pressure * self.pop_size)
        candidates = np.random.randint(self.pop_size, size=tournament_size)
        parent = candidates[self.fitness[candidates].argmax()]
        return parent

    def _mutate_point(self, spring_param):
        p = np.random.randint(low=0, high=len(spring_param), size=1)
        spring_param[p, 0] = np.random.rand() *  self.l0_amplitude# b
        spring_param[p, 1] = np.random.rand() * 2 * np.pi * self.p0_range # t0
        spring_param[p, 2] = int(np.random.rand() * self.k_spring/200) * 200  # k
        return spring_param

    def _mutate_segment(self, spring_param):
        segment = np.random.randint(low=0, high=len(spring_param), size=2)
        for p in range(segment.min(), segment.max()+1):
            spring_param[p, 0] = np.random.rand() *  self.l0_amplitude# b
            spring_param[p, 1] = np.random.rand() * 2 * np.pi * self.p0_range # t0
            spring_param[p, 2] = int(np.random.rand() * self.k_spring/200) * 200 # k # k
        return spring_param

    def _crossover(self, parent1, parent2):
        segment = np.random.randint(low=0, high=len(parent1), size=2)
        parent1[segment.min():segment.max()] = parent2[segment.min():segment.max()]
        return parent1

    def _cut_off(self, offspring, last_size=10):
        fn = np.ones(len(offspring))
        for i in range(len(offspring)):
            off_displacement = self._simulate_robot(offspring[i])
            fn[i] = self.weight_distance * off_displacement[0] + self.weight_drift * off_displacement[1]
        idx_off = fn.argsort()[::-1][0:self.pop_size-last_size]
        idx_pop = self.fitness.argsort()[::-1][0:last_size]
        new_pop = []
        for i in idx_off:
            new_pop.append(offspring[i])
        for i in idx_pop:
            new_pop.append(self.spring_params[i])
        self.spring_params = np.array(new_pop)
        self.fitness = np.r_[fn[idx_off], self.fitness[idx_pop]]

    def evolve(self):
        offspring = np.zeros_like(self.spring_params)
        for i in range(self.pop_size):
            parent_i = self._tournament()
            parent = np.copy(self.spring_params[parent_i])
            p = np.random.rand()
            if p < self.evolve_rate[0]:                # crossover
                parent2_i = self._tournament()         # select parent2 by _tournament()
                parent2 = np.copy(self.spring_params[parent2_i])
                parent = self._crossover(parent, parent2)          # crossover
            elif p < self.evolve_rate[0:2].sum():      # point mutate
                parent = self._mutate_point(parent) # point mutate
            elif p < self.evolve_rate[0:3].sum():      # partial mutate
                pass                                # segment mutate
            offspring[i] = parent
        self._cut_off(offspring)
        self._update_best()

    def get_best_param(self):
        return self.best_param

    def get_best_robot(self):
        robot = CubeRobot(self.robot_shape[0], self.robot_shape[1], self.robot_shape[2])
        robot.set_spring_param(self.best_param)
        return robot
