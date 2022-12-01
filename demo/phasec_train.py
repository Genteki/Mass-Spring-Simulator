import os, sys
sys.path.append(os.getcwd())

import numpy as np
from physics import *
from robot import *
from evolution import *
from phasec_disable import *
from datetime import datetime

if __name__ == '__main__':
    if len(sys.argv) == 1:
        cube_type = "ori"
    else:
        cube_type = sys.argv[1]
    if len(sys.argv) <= 2:
        sim_t=8; pops = 150
    elif sys.argv[2] == "baseline":
        sim_t=.1; pops=100
    else:
        sim_t=8; pops=150
    ga = GA_C(k_spring=1200, omega=2, l0_amplitude=0.5, p0_range=0.3,
              friction=0.8, robot_shape = [3,3,2], m=1, sim_t=sim_t,
              pop_size=pops, dt=1/1200, disable_cube=disable_param_332[cube_type])
    print("shape: ", ga.robot_shape)
    print("pop_size: ", ga.pop_size)
    print("sim_t: ", ga.sim_t)
    print("select_pressure: ", ga.select_pressure)
    ga.cal_fitness()

    for i in range(100):
        ga.evolve()
        np.savetxt(r"output/phasec/{}/best/gen{}.txt".format(cube_type, i), ga.best_param)
        np.savetxt(r"output/phasec/{}/learningcurve/fitness_history.txt".format(cube_type), np.array(ga.fitness_history))
        np.savetxt(r"output/phasec/{}/learningcurve/speed_history.txt".format(cube_type), np.array(ga.speed_history))

        print(r"generation {}, best fitness: {}".format(i, ga.best_fitness))

    robot = ga.get_best_robot()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    np.savetxt("output/phasec/"+cube_type+"/"+dt_string+".txt", ga.best_param)
