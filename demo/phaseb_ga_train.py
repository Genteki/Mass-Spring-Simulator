import os, sys
sys.path.append(os.getcwd())

import numpy as np
from physics import *
from robot import *
from evolution.ga import GA
from datetime import datetime

if __name__ == '__main__':
    ga = GA(k_spring=1200, omega=2, l0_amplitude=0.5, p0_range=0.1, friction=0.8, robot_shape = [3,1,1], m=1, sim_t=20, pop_size=150)
    print("shape: ", ga.robot_shape)
    print("pop_size: ", ga.pop_size)
    print("sim_t: ", ga.sim_t)
    print("select_pressure: ", ga.select_pressure)
    ga.cal_fitness()

    for i in range(100):
        ga.evolve()
        np.save(r"output/phaseb/gen{}.npy".format(i), ga.best_param)
        print(r"generation {}, best fitness: {}".format(i, ga.best_fitness))

    robot = ga.get_best_robot()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    np.save("output/phaseb/"+dt_string+".npy", ga.best_param)
