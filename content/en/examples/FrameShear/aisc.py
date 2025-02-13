#
# AISC Benchmark Problems
#
from opensees.units.iks import ft, ksi
from opensees.helpers import Prism

def check_case1(model, Mbench, Dbench, ndm):
    ne    = len(model.getEleTags())
    Axial = model.getTime()
    Mmid  = (-1)**ndm*model.eleResponse(int(ne//2), "forces")[5 if ndm==2 else 11]
    u     = model.nodeDisp(int(ne//2)+1, 2)

    # Axial Force  |  Moment at h/2  |  Displacement at h/2 |
    print(f"| {Axial:8.0f} |", end="")
    print(f" {Mmid:8.1f} | {Mbench:8.0f} | %8.2f %% |" % (100*(Mbench-Mmid)/Mbench), end="")
    print(f" {u:8.4f} | {Dbench:8.3f} | %8.2f %% |" % ((100*(Dbench-u)/Dbench)))


def check_case2(model, Mbench, Dbench, ndm):
    nn = len(model.getNodeTags())
    Axial  = model.getTime()
    Mbase  = model.eleResponse( 1, "forces")[2 if ndm==2 else 5]
    Dtip   = -model.nodeDisp(nn, 2)

    print(f"| {Axial:8.0f} |", end="")
    print(f" {Mbase:8.1f} | {Mbench:8.0f} | %8.2f %% |" % (100*(Mbench-Mbase)/Mbench), end="")
    print(f" {Dtip:8.4f} | {Dbench:8.3f} | %8.2f %% |" % (100*(Dbench-Dtip)/Dbench))


def analyze_case1(model, Mbench, Dbench, ndm=3):

    ne = len(model.getNodeTags()) - 1

    model.pattern("Plain", 1, "Linear")
    for i in range(ne):
        model.eleLoad("-ele", i+1, "-pattern", 1, "-type", "beamUniform",  ( 0.200/ft, 0.0))

    model.constraints("Transformation")
    model.numberer("Plain")
    model.system("UmfPack")
    model.test("NormDispIncr", 1.0e-6, 30, 0)
    model.algorithm("Newton")
    model.integrator("LoadControl", 0.1)
    model.analysis("Static")
    model.analyze(10)

    check_case1(model, Mbench[0], Dbench[0], ndm=ndm)

    model.loadConst(time=0.0)
    model.pattern("Plain", 2, "Linear", load={
        ne+1: [-1, 0, 0]+([0, 0, 0] if ndm == 3 else [])
    })


    model.integrator("LoadControl", 15.0)
    model.analyze(10)
    check_case1(model, Mbench[1], Dbench[1], ndm=ndm)

    model.analyze(10)
    check_case1(model, Mbench[2], Dbench[2], ndm=ndm)

    model.analyze(10)
    check_case1(model, Mbench[3], Dbench[3], ndm=ndm)

    return model

def analyze_case2(model, Mbench, Dbench, ndm=3):

    ne = len(model.getNodeTags()) - 1

    model.pattern("Plain", 1, "Linear", load={
            ne+1: [0, -1, 0] + ([0, 0, 0] if ndm == 3 else [])
    })

    model.constraints("Transformation")
    model.numberer("Plain")
    model.system("UmfPack")
    model.test("NormDispIncr", 1.0e-6, 30, 0)
    model.algorithm("Newton")
    model.integrator("LoadControl", 0.1)
    model.analysis("Static")
    model.analyze(10)

    model.loadConst(time=0.0)

    check_case2(model, Mbench[0], Dbench[0], ndm=ndm)

    model.pattern("Plain", 2, "Linear", load={
            ne+1: [-1, 0, 0] + ([0, 0, 0] if ndm == 3 else [])
        }
    )

    model.integrator("LoadControl", 10.0)

    model.analyze(10)
    check_case2(model, Mbench[1], Dbench[1], ndm=ndm)

    model.analyze(5)
    check_case2(model, Mbench[2], Dbench[2], ndm=ndm)

    model.analyze(5)
    check_case2(model, Mbench[3], Dbench[3], ndm=ndm)

if __name__ == "__main__":

    ndm = 3
    A =  14.1
    I =  484.0
    d =  13.8
    tw = 0.340
    section = dict(
            E  = 29000.0,
            G =  11200.0,
            A  = A,
            J  = 100*I,
            Iy = I,
            Iz = I,
            Ay = d*tw,
            Az = d*tw
    )

    #
    # Case 1
    #
    for element in "ForceFrame", "ForceDeltaFrame", "PrismFrame":
        for shear in (True, False):

            if "Exact" in element and (ndm == 2 or not shear):
                continue

            prism = Prism(
                length = 336.0,
                element = element,
                section = section,
                boundary = ("pin", "pin"),
                geometry  = "Linear",
                transform = "Corotational",
                divisions = 6
            )

            if  shear :
                Mbench = [ 235.0, 270.0, 316.0, 380.0]
                Dbench = [ 0.202, 0.230, 0.269, 0.322]
            else:
                Mbench = [ 235.0, 269.0, 313.0, 375.0]
                Dbench = [ 0.197, 0.224, 0.261, 0.311]

            print(f"Case 1: {element} ({shear = })")
            model = prism.create_model(ndm=ndm)
            analyze_case1(model, Mbench, Dbench, ndm=ndm)
        # veux.serve(veux.render(model, model.nodeDisp, scale=100, ndf=(3 if ndm == 2 else 6)))


    #
    # Case 2
    #

    for shear in  (True, False):

        if  shear :
            Mbench = [ 336.0, 470.0, 601.0, 856.0]
            Dbench = [ 0.907,  1.34,  1.77,  2.60]

        else:
            Mbench = [ 336.0, 469.0, 598.0, 848.0]
            Dbench = [ 0.901, 1.33 , 1.75 , 2.56 ]

        for element in "ForceFrame", "ExactFrame", "PrismFrame":
            if "Exact" in element and (ndm == 2 or not shear):
                continue

            prism = Prism(
                length  = 336.0,
                element = element,
                section = section,
                boundary = ("fix", "free"),
                geometry  = "delta",
                transform = "Corotational",
                divisions = 3
            )

            print(f"Case 2: {element} ({shear = })")
            model = prism.create_model(ndm=ndm)
            analyze_case2(model, Mbench, Dbench, ndm=ndm)
            # veux.serve(veux.render(model, model.nodeDisp, scale=100, ndf=(3 if ndm == 2 else 6)))

