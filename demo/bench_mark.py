import os, sys
import time
sys.path.append(os.getcwd())

import numpy as np
from physics import *
from robot import *
from evolution.ga import GA

ga = GA(k_spring=500, omega=2, l0_amplitude=0.5, p0_range=0.1, friction=0.7, robot_shape = [8,1,1], m=4, sim_t=10, pop_size=200)
sim_t = 1

## timer start
t = time.perf_counter()
ga._simulate_robot(ga.spring_params[0], sim_t=sim_t)
cost = time.perf_counter() - t
print("runtime: ", cost)
print("springs calculated: ", len(ga.spring_params[0]) * ga.sim.t / ga.sim.dt)
print("spring per sec: ", len(ga.spring_params[0]) * sim_t / ga.sim.dt / cost)
