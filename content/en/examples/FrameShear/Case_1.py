# AISC Benchmark Problem, Case 1
#
# AISC 360-16, Commentary Figure C-C2.2
#
# Pinned-pinned column with uniform lateral load of 0.200 kip/ft and varying axial load
#
# Units: kip, in, sec
import numpy as np
import opensees.openseespy as ops
from opensees.units.iks import ft

def benchmark(model, Mbench, Dbench):
    ne    = len(model.getEleTags())
    Axial = model.getTime()
    Mmid  = model.eleResponse(int(ne//2), "forces")[5]
    u     = model.nodeDisp(int(ne//2)+1, 1)


    # Axial Force  |  Moment at h/2  |  Displacement at h/2 |
    print(f"| {Axial:8.0f} |", end="")
    print(f" {Mmid:8.1f} | {Mbench:8.0f} | %8.2f %% |" % (100*(Mbench-Mmid)/Mbench), end="")
    print(f" {u:8.4f} | {Dbench:8.3f} | %8.2f %% |" % ((100*(Dbench-u)/Dbench)))



def analyze(element="ForceBeamColumn", use_shear = False):
    if  use_shear :
        Mbench_list = [ 235.0, 270.0, 316.0, 380.0]
        Dbench_list = [ 0.202, 0.230, 0.269, 0.322]
    else:
        Mbench_list = [ 235.0, 269.0, 313.0, 375.0]
        Dbench_list = [ 0.197, 0.224, 0.261, 0.311]

    ne = 6

    L = 336.0

    # Material
    E =  29000.0
    G =  11200.0

    # Cross-section
    A =  14.1
    I =  484.0
    d =  13.8
    tw = 0.340

    # Shear coefficient taken from Iyer 2005: A/Av
    k = (d*tw)/A

    model = ops.Model(ndm=2,  ndf=3)

    # Create ne+1 linearly spaced nodes
    for i,y in enumerate(np.linspace(0, L, ne+1)):
        tag = i+1
        model.node(tag, 0.0,   y)

    model.fix(   1, 1, 1, 0)
    model.fix(ne+1, 1, 0, 0)

    # Sections
    if  use_shear :
        model.section("Elastic", 1, E, A, I, G, k)
    else:
        model.section("Elastic", 1, E, A, I)

    if "Exact" in element:
        model.geomTransf("Linear", 1)
    else:
        model.geomTransf("Corotational", 1)

#   model.geomTransf("PDelta", 1)

    # Elements
    for i in range(ne):
        tag = i+1
        nodes = (tag, tag+1)
        model.element(element, i+1, nodes, section=1, transform=1)


    model.pattern("Plain", 1, "Linear")

    for i in range(ne):
        model.eleLoad("-ele", i+1, "-pattern", 1, "-type", "beamUniform",  -0.200/ft)


    model.constraints("Transformation")
    model.numberer("Plain")
    model.system("UmfPack")
    model.test("NormDispIncr", 1.0e-6, 30, 0)
    model.algorithm("Newton")
    model.integrator("LoadControl", 0.1)
    model.analysis("Static")
    model.analyze(10)
    benchmark(model, Mbench_list[0], Dbench_list[0])



    model.loadConst(time=0.0)
    model.pattern("Plain", 2, "Linear", load={ne+1: [0, -1, 0]})


    model.integrator("LoadControl", 15.0)
    model.analyze(10)
    benchmark(model, Mbench_list[1], Dbench_list[1])


    model.analyze(10)
    benchmark(model, Mbench_list[2], Dbench_list[2])


    model.analyze(10)
    benchmark(model, Mbench_list[3], Dbench_list[3])

    return model

if __name__ == "__main__":

#   "DispBeamColumnNL"
#   "DispBeamColumn"
#   "PrismFrame"

    for element in "ForceFrame", "forceBeamColumnCBDI", "PrismFrame", "ExactFrame":
        for shear in True, False:
            print(element, f"({shear = })")
            model = analyze(element, use_shear=shear)

