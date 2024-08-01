# AISC Benchmark Problem, Case 2
# AISC 360-16, Commentary Figure C-C2.3
#
# Cantilever column with a 1-kip lateral point load at the end and a varying
# axial load
#
import numpy as np
from math import cos,sin,sqrt,pi
import opensees.openseespy as ops
# import units (inch-kip-sec)
from opensees.units.iks import ft, inch, ksi


use_shear = False

if  use_shear :
    Mbench = [ 336.0, 470.0, 601.0, 856.0]
    Dbench = [ 0.907,  1.34,  1.77,  2.60]

else:
    Mbench = [ 336.0, 469.0, 598.0, 848.0]
    Dbench = [ 0.901, 1.33 , 1.75 , 2.56 ]


def check(model, Mbench, Dbench):
    nn = len(model.getNodeTags())
    Axial  = model.getTime()
    Mbase  = model.eleResponse( 1, "forces")[2]
    Dtip   = model.nodeDisp(nn, 1)
    print("                       Computed       Exact     Error")
    print(f"Axial Force (kips)     {Axial:8.0f}")
    print(f"Base moment (kip-in)   {Mbase:8.0f}    {Mbench:8.0f} %8.2f %%" % (100*(Mbench-Mbase)/Mbench))
    print(f"Tip displacement (in)  {Dtip:8.4f}    {Dbench:8.3f} %8.2f %%\n" % (100*(Dbench-Dtip)/Dbench))

def create_column(element, use_shear=False):
    L = 28*ft
    # Material
    E =  29000.0*ksi
    G =  11200.0*ksi

    # Cross-section (W14x48)
    A =  14.1
    I =  484.0
    d =  13.8
    tw = 0.340
    # shear coefficient A/Av
    k = (d*tw)/A

    ne = 4
    ndm = 2

    if ndm == 2:
        vecxz = ()
    else:
        vecxz = (0, 0, 1)

    model = ops.Model(ndm=2,  ndf=3)

    # Create ne+1 linearly spaced nodes
    for i,y in enumerate(np.linspace(0, L, ne+1)):
        tag = i+1
        model.node(tag, 0.0,   y)


    model.fix(1, 1, 1, 1)

    # Cross-Section
    if  use_shear :
        model.section("Elastic", 1, E, A, I, G, k)
    else:
        model.section("Elastic", 1, E, A, I)

    model.geomTransf("Corotational", 1, *vecxz)

    # Elements
    for i in range(ne):
        tag = i+1
        nodes = (tag, tag+1)
#       model.element('PrismFrame', i+1, nodes, A, E, I, 1, "-order", 1)

        model.element(element, i+1, nodes, 3, 1, 1)
#       model.element('ForceBeamColumnCBDI', i+1, node_i, node_j, 3, 1, 1)
#       model.element('DispBeamColumnNL', i+1, node_i, node_j, 3, 1, 1)
#       model.element('DispBeamColumn', i+1, node_i, node_j, 3, 1, 1)

    model.pattern("Plain", 1, "Linear", load={
            ne+1: [1, 0, 0]
    })

    return model


def analyze(model, Mbench, Dbench):
    model.constraints('Transformation')
    model.numberer('Plain')
    model.system('UmfPack')
    model.test('NormDispIncr', 1.0e-6, 30, 0)
    model.algorithm('Newton')
    model.integrator('LoadControl', 0.1)
    model.analysis('Static')
    model.analyze(10)

    ne = len(model.getNodeTags()) - 1

    model.loadConst(time=0.0)

    check(model, Mbench[0], Dbench[0])

    model.pattern("Plain", 2, "Linear", load={ne+1: [0, -1, 0]})

    model.integrator("LoadControl", 10.0)
    model.analyze(10)

    check(model, Mbench[1], Dbench[1])

    model.analyze(5)

    check(model, Mbench[2], Dbench[2])

    model.analyze(5)

    check(model, Mbench[3], Dbench[3])


if __name__ == "__main__":
    analyze(create_column("forceBeamColumn"), Mbench, Dbench)
    analyze(create_column("forceBeamColumnCBDI"), Mbench, Dbench)


