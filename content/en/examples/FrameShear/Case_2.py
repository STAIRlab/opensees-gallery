# AISC Benchmark Problem, Case 2
#
# AISC 360-16, Commentary Figure C-C2.3
#
# Cantilever column with a 1-kip lateral point load at the end and a varying
# axial load
#
import numpy as np
from math import cos,sin,sqrt,pi
import opensees.openseespy as ops

# import units (inch-kip-sec)
from opensees.units.iks import ft, ksi



def check_cantilever(model, Mbench, Dbench):
    nn = len(model.getNodeTags())
    Axial  = model.getTime()
    Mbase  = model.eleResponse( 1, "forces")[2]
    Dtip   = model.nodeDisp(nn, 1)

    print(f"  {Axial:5.0f}", end="   ")
    print(f"  {Mbase:5.0f}    {Mbench:8.0f} %8.2f %%" % (100*(Mbench-Mbase)/Mbench), end="   ")
    print(f"  {Dtip:5.4f}    {Dbench:8.3f} %8.2f %%" % (100*(Dbench-Dtip)/Dbench))


def create_column(element, use_shear=False, ndm=3):
    ne = 3
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

    model = ops.Model(ndm=ndm)

    # Create ne+1 linearly spaced nodes
    for i,y in enumerate(np.linspace(0, L, ne+1)):
        tag = i+1
        if ndm == 3:
            location = (0.0, y, 0.0)
        else:
            location = (0.0, y)

        model.node(tag, location)


    boundary = [1, 1, 1]
    if ndm == 3:
        boundary = boundary + [1, 1, 1]

    model.fix(1, *boundary)

    # Cross-Section
    if ndm == 2:
        if  use_shear :
            model.section("Elastic", 1, E, A, I, G, k)
        else:
            model.section("Elastic", 1, E, A, I)
    else:
        #                     Iy  G   J
        properties = [E, A, I, I, G, 100*I]
        if use_shear:
            properties.extend(["-Ay", k*A, "-Az", k*A])
        model.section("FrameElastic", 1, *properties)


    if ndm == 2:
        vecxz = ()
    else:
        vecxz = (0, 0, 1)
    model.geomTransf("Corotational", 1, *vecxz)

    # Elements
    for i in range(ne):
        tag = i+1
        nodes = (tag, tag+1)
        model.element(element, i+1, nodes, transform=1, section=1)


    model.pattern("Plain", 1, "Linear", load={
            ne+1: [1, 0, 0] + ([0, 0, 0] if ndm == 3 else [])
    })

    return model


def analyze_case2(model, Mbench, Dbench, ndm=3):
    model.constraints("Transformation")
    model.numberer("Plain")
    model.system("UmfPack")
    model.test("NormDispIncr", 1.0e-6, 30, 0)
    model.algorithm("Newton")
    model.integrator("LoadControl", 0.1)
    model.analysis("Static")
    model.analyze(10)

    ne = len(model.getNodeTags()) - 1

    model.loadConst(time=0.0)

    check_cantilever(model, Mbench[0], Dbench[0])

    model.pattern("Plain", 2, "Linear", load={
        ne+1: [0, -1, 0] + ([0, 0, 0] if ndm == 3 else [])
        }
    )

    model.integrator("LoadControl", 10.0)
    model.analyze(10)

    check_cantilever(model, Mbench[1], Dbench[1])

    model.analyze(5)

    check_cantilever(model, Mbench[2], Dbench[2])

    model.analyze(5)

    check_cantilever(model, Mbench[3], Dbench[3])


if __name__ == "__main__":
    ndm = 2

    for shear in False, True:

        if  shear :
            Mbench = [ 336.0, 470.0, 601.0, 856.0]
            Dbench = [ 0.907,  1.34,  1.77,  2.60]

        else:
            Mbench = [ 336.0, 469.0, 598.0, 848.0]
            Dbench = [ 0.901, 1.33 , 1.75 , 2.56 ]

        for element in "ForceFrame", "ExactFrame", "PrismFrame":
            if "Exact" in element and (ndm == 2 or not shear):
                continue
            print(f"{element} ({shear = })")
            model = create_column(element, shear, ndm=ndm)
            analyze_case2(model, Mbench, Dbench, ndm=ndm)

