
import sys

# Linear algebra library
import numpy as np

# import the openseespy interface which contains the "Model" class
import opensees.openseespy as ops
import opensees.section
import quakeio


## Configure units
# Units are based on inch-kip-seconds
import opensees.units.iks as units
pi   = units.pi;
ft   = units.ft;
ksi  = units.ksi;
inch = units.inch;



def create_prism(element,
                 section:   int,
                 transform: str
                 ):

    # generate Model data structure
    model = ops.Model(ndm=3, ndf=6)

    # Length of cantilever column
    L = 8*ft;
    # specify node coordinates
    model.node(1,  0,   0 , 0);  # first node
    model.node(2,  0,   L , 0);  # second node

    # boundary conditions
    model.fix(1, 1, 1, 1 , 1, 1, 1)

    ## specify mass
    model.mass(2, 2.0, 2.0, small_mass)

    # Define material

    mat_tag = 1      # identifier that will be assigned to the new material
    E    = 29000*ksi
    nu   = 0.3
    fy   =    60*ksi
    Hkin =     E*hardening
    Hiso =     E*hardening

    model.nDMaterial("ElasticIsotropic", mat_tag, E, nu)


    #
    #
    #
    sec_tag = 1
    width = 15.0
    depth = 24.0

    model.section("Fiber", sec_tag, GJ=1e6)
    model.patch("rect", 1, (10, 10), -depth/2, -width/2, depth/2, width/2, section=sec_tag)

    # Create element geometric transformation
    model.geomTransf("Linear", 1, (0, 0, 1))

    # Finally, create the element
    #                          CONN   Geom
    model.element(element, 1, (1, 2),  transform=1, section=1)


   #                                                  Force     |  Moment
    model.pattern("Plain", 1, "Linear", load={2: [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]})

    return model


def cantilever(element, small_mass = 1e-4, hardening=0.1, damping=None):

    # generate Model data structure
    model = ops.Model(ndm=3, ndf=6)

    # Length of cantilever column
    L = 8*ft;
    # specify node coordinates
    model.node(1,  0,   0 , 0);  # first node
    model.node(2,  0,   L , 0);  # second node

    # boundary conditions
    model.fix(1, 1, 1, 1 , 1, 1, 1)

    ## specify mass
    model.mass(2, 2.0, 2.0, small_mass)

    # Define material

    mat_tag = 1      # identifier that will be assigned to the new material
    E    = 29000*ksi
    nu   = 0.3
    fy   =    60*ksi
    Hkin =     E*hardening
    Hiso =     E*hardening

    model.nDMaterial("ElasticIsotropic", mat_tag, E, nu)


    #
    #
    #
    sec_tag = 1
    width = 15.0
    depth = 24.0

    model.section("Fiber", sec_tag, GJ=1e6)
    model.patch("rect", 1, (10, 10), -depth/2, -width/2, depth/2, width/2, section=1)

    # Create element geometric transformation
    model.geomTransf("Linear", 1, (0, 0, 1))

    # Finally, create the element
    #                          CONN   Geom
    model.element(element, 1, (1, 2),  transform=1, section=1)


   #                                                  Force     |  Moment
    model.pattern("Plain", 1, "Linear", load={2: [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]})

    return model


def analyze(model):
    model.analysis("Static")

    if False:
        nsteps = 20
        dU = 0.1;	        # Displacement increment
        #                                    node dof init Jd min max
        model.integrator("DisplacementControl", 2, 1, dU, 1, dU, dU)
    else:
        nsteps = 5
        model.integrator("LoadControl", 300.)

    for i in range(nsteps):
        model.analyze(1)
        print(model.nodeDisp(2, 1), model.getTime())



analyze(cantilever(sys.argv[1]))
