# ===----------------------------------------------------------------------===//
# 
#         OpenSees - Open System for Earthquake Engineering Simulation    
#                Structural Artificial Intelligence Laboratory
#                               gallery.stairlab.io
# 
# ===----------------------------------------------------------------------===//
#
# Claudio Perez
#
# Adapted from https://portwooddigital.com/2022/08/14/parametric-oscillator/
#
import opensees.openseespy as ops
from opensees.units.ips import inch, sec, gravity as g

def create_pendulum3D(m, k, L, W):
    # Create a model with 3 dimensions (ndm) 
    # and 3 degrees of freedom per node (ndf)
    model = ops.Model(ndm=3, ndf=3)


    # Create a node for the pivot point and fix it
    model.node(1, (0, 0, 0))
    model.fix(1, (1, 1, 1))

    # Create a free node with the mass
    model.node(2, 0, -L, 0)
    model.mass(2, m, m, m)

    # Create a corotational truss between nodes 1 and 2
    model.uniaxialMaterial('Elastic', 1, k*L)
    model.element('CorotTruss', 1, 1, 2, 1.0, 1)

    # Initial displacements
    model.setNodeDisp(2, 1,         0.05*L, '-commit')
    model.setNodeDisp(2, 2, -W/k-(W/k+L)/3, '-commit')

    # Pendulum weight
    model.pattern("Plain", 1, "Constant")
    model.load(2, (0, -W, 0))
    return model

def create_pendulum(m, k, L, W):
    # Create a model with 2 dimensions (ndm) 
    # and 2 degrees of freedom per node (ndf)
    model = ops.Model(ndm=2, ndf=2)


    # Create a node for the pivot point and fix it
    model.node(1, 0, L)
    model.fix(1, 1, 1)

    # Create a free node with the mass
    model.node(2, 0, 0)
    model.mass(2, m, m)

    # Create a corotational truss between nodes 1 and 2
    model.uniaxialMaterial('Elastic', 1, k*L)
    model.element('CorotTruss', 1, 1, 2, 1.0, 1)

    # Initial displacements
    model.setNodeDisp(2, 1, 0.05*L, '-commit')
    model.setNodeDisp(2, 2, -W/k-(W/k+L)/3, '-commit')

    # Pendulum weight
    model.pattern("Plain", 1, "Constant")
    model.load(2, 0, -W)
    return model


def analyze_pendulum(model):
    model.algorithm('Newton')
    model.integrator('Newmark',0.5,0.25)

    model.analysis('Transient')

    Tmax = 12*sec
    dt = 0.01*sec
    Nsteps = int(Tmax/dt)
    u = []
    for i in range(Nsteps):
        model.analyze(1, dt)
        u.append(model.nodeDisp(2))

    return u



if __name__ == "__main__":
    # Length of pendulum
    L = 10*inch

    # Pendulum mass
    m = 1.0

    # Linearized frequency of pendulum
    omega = (g/L)**0.5

    # Frequency of oscillator
    w = 2*omega

    # Stiffness of spring
    k = m*w**2

    model = create_pendulum(m, k, L, m*g)

    u = analyze_pendulum(model)
    print(u)

