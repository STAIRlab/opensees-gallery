 Free-standing beam element
#
#  ^
#  |
#  o======================o--->
#
#
import opensees.openseespy as ops
import numpy as np


def single_span(elem):
    L  =  1.3
    A  =  1.0
    E  =  1.0
    G  =  1.0
    J  =  5.0
    Iy =  3.0
    Iz =  1.0

    # Create a model
    model = ops.Model(ndm=3, ndf=6)


    # Define nodes
    model.node(1,  0.0, 0.0, 0.0)
    model.node(2,   (L, 0, 0.0))


    trn = 1
    model.geomTransf("Linear", 1, (0, 0, 1))


    sec = 1
    model.section("ElasticFrame", sec, E, A, Iz, Iy, G, J, mass=2, Ay=100, Az=100)

    model.element(elem, 1, (1, 2), transform=trn, section=sec, cMass=True)

    return model


