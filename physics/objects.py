import numpy as np

zero_vec = np.array([0,0,0])
class Mass:
    def __init__(self, m, p, v=zero_vec, a=zero_vec, f=zero_vec, id=None):
        self.m = m
        self.p = np.array(p, dtype=np.float64)
        self.v = np.array(v, dtype=np.float64)
        self.a = np.array(a, dtype=np.float64)
        self.f_external = np.array(f, dtype=np.float64)
        self.id = id

def distance(m1,m2):
    return np.linalg.norm(m1.p - m2.p, ord=2)

class Spring:
    def __init__(self, m1, m2, l0, k, name=None):
        self.m1 = m1
        self.m2 = m2
        self.l0 = l0
        self.l00 = l0
        self.k = k
        self.tension = None

    def cal_tension(self):
        l = np.linalg.norm(self.m1.p - self.m2.p, ord=2)
        f_scale = self.k * (l - self.l0)
        vec_norm = (self.m1.p - self.m2.p) / l
        self.tension = -f_scale * vec_norm
        return self.tension

class Simulator:
    def __init__(self, mass=[], spring=[], g=[0.,0.,-9.8], dt=1/2400, k_ground=1, damping=0.999, friction_ground=0):
        self.mass = mass
        self.spring = spring
        self.dt = dt
        self.g = np.array(g, dtype=np.float64)
        self.k_ground = 1e3 * k_ground / dt
        self.friction_ground = friction_ground
        self.damping = damping
        self.t = 0

    def reset(self, mass=[], spring=[]):
        self.t = 0
        if len(mass) and len(spring):
            self.mass = mass
            self.spring = spring   

    def simulate(self):
        # Time increment
        self.t = self.t + self.dt
        # Interaction step
        # reset f_external for mass
        for m in self.mass:
            m.f_external = m.m * self.g
        # calculate tension
        for s in self.spring:
            s.cal_tension()
            s.m1.f_external += s.tension
            s.m2.f_external -= s.tension
        # collision to ground
        for m in self.mass:
            # restoring force
            if m.p[2] < 0:
                m.f_external[2] += -m.p[2] * self.k_ground
                # friction to ground
                if m.f_external[2] > 0 and (m.v[0:2]!=0).any():
                    m.f_external[0:2] += -m.v[0:2] * m.f_external[2] * self.friction_ground / np.linalg.norm(m.v[0:2],2)
        # Integration Step
        for m in self.mass:
            m.a = m.f_external / m.m
            m.v = m.v * self.damping + m.a * self.dt
            m.p = m.p + m.v * self.dt

    def energy_spring(self):
        es = 0
        for s in self.spring:
            es += s.k * (distance(s.m1,s.m2) - s.l0)**2 / 2
        return es

    def energy_kinematics(self):
        ek = 0
        for m in self.mass:
            ek += m.m * np.linalg.norm(m.v, ord=2) ** 2 / 2
        return ek

    def energy_gravity(self):
        eg = 0
        for m in self.mass:
            eg += np.sum(m.p * self.g)
        return eg

    def energy(self):
        return self.energy_spring() + self.energy_gravity() + self.energy_kinematics()

    def cal_per_step(self):
        return len(self.mass)+len(self.spring)

def test_single_ball():
    m1 = Mass(1., [0.,0.,5.])
    m2 = Mass(1., [0.,1.,5.])
    s1 = Spring(m1,m2,2,1)
    s2 = Spring(m1,m2,2,1)
    sim = Simulator([m1,m2],[s1,s2],g=[0,0,-10],damping=1)
    for i in range(960*2):
        if not i%96:
            print(sim.t, m1.p)
        sim.simulate()

if __name__ == '__main__':
    test_single_ball()
