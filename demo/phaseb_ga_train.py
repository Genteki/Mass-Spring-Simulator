import os, sys
sys.path.append(os.getcwd())

import numpy as np
from physics import *
from robot import *
from evolution.ga import GA
from datetime import datetime

ga = GA(k_spring=500, omega=2, l0_amplitude=0.5, p0_range=0.1, friction=0.7, robot_shape = [8,1,1], m=4, sim_t=10, pop_size=200)
for i in range(100):
    ga.evolve()
    np.save(r"output/phaseb/gen{}.npy".format(i), ga.best_param)
    print(r"generation {}, best fitness: {}".format(i, ga.best_fitness))

robot = ga.get_best_robot()
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
np.save("output/phaseb/"+dt_string+".npy", ga.best_param)
