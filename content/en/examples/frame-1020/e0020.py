# Cantilever beam subjected to follower end load.
# Basic section properties
import sys
import veux
import numpy as np
from veux.motion import Motion
import opensees.openseespy as ops
import matplotlib.pyplot as plt
try:
    pass
    plt.style.use("typewriter")
except:
    pass

def create_cantilever(ne, element):
    model = ops.Model(ndm=3, ndf=6)

    L  = 100

    nen = 2
    nmn = ne*(nen-1)+1
    sec = 1
    A = 1.61538e8
    I = 3.5e7
    model.section("ElasticFrame", sec,
                    E=1,
                    G=1,
                    A=A,
                    Ay=A,
                    Az=A,
                    Iy=I*100,
                    Iz=I,
                    J =I
    )

#   model.geomTransf("Corotational", 1, (0,1,0))
    model.geomTransf("Linear", 1, (0,0,1))

    for i,x in enumerate(np.linspace(0, L, nmn)):
        model.node(i, (x,0,0))

    for i in range(ne):
        start = i * (nen - 1)
        nodes = list(range(start, start + nen))
        model.element(element, i+1, nodes, section=sec, transform=1)

    model.fix(0,  (1,1,1,  1,1,1))
    for i in range(nmn):
        model.nodeRotation(i)

    return model

def analyze(element):
    ne = 10

    model = create_cantilever(ne, element=element)
    artist = veux.create_artist(model, model_config=dict(extrude_outline="square"))
    artist.draw_nodes(size=10)
    artist.draw_sections()
    # veux.serve(artist)
    motion = Motion(artist)

    #
    # Apply vertical load
    #
    speed  = 1/1000 # animation frames
    Pmax   = 150e3 # N
    model.pattern("Plain", 1, "Linear")

    print("Pattern = element")
    model.eleLoad("Frame", "Dirac",
                  force = [0, 1, 0],
                  basis = "director",
                  offset=[1.0,0,0],
                  pattern=1,
                  elements=[ne]
    )

    model.system('FullGeneral')
    model.integrator("LoadControl", Pmax/500)#, 5, Pmax/5000, Pmax/100)
#   model.integrator("ArcLength", Pmax/100, det=True, exp=0.5)
    model.test("NormDispIncr", 1e-12, 10, 1)
#   model.test('NormUnbalance',1e-6,100,1)
    model.algorithm("Newton")
    model.analysis("Static")
    input()

    u = []
    v = []
    w = []
    P = []
#   for i in range(10):
    while model.getTime() < Pmax:
        if model.analyze(1) != 0:
            model.integrator("LoadControl", Pmax/10000)
            if model.analyze(1) != 0:
                print(f"Failed at time = {model.getTime()} with v = {v[-1]}")
                break
            else:
                model.algorithm("Newton")
        motion.advance(time=model.getTime()*speed)
        motion.draw_sections(rotation=model.nodeRotation,
                             position=model.nodeDisp)
        u.append(-model.nodeDisp(ne, 1))
        v.append( model.nodeDisp(ne, 2))
        w.append( model.nodeDisp(ne, 3))
        P.append( model.getTime())



    fig, ax = plt.subplots()
    ax.set_xlabel("Load, $P$")
    ax.set_ylabel(r"Displacement")
    # ax.set_xlim([0,    300])
#   ax.set_ylim([0,   Pmax])
    ax.axvline(0, color='black', linestyle='-', linewidth=1)
    ax.axhline(0, color='black', linestyle='-', linewidth=1)
    ax.plot(P, u, label="$u$")
    ax.plot(P, v, label="$v$")
    ax.plot(P, w, label="$w$")
    ax.legend()
    fig.savefig("img/e0020.png")
    plt.show()

    motion.add_to(artist.canvas)
    if len(sys.argv) > 1:
        artist.save(sys.argv[1])
    else:
        veux.serve(artist)


if __name__ == "__main__":
    import os
    analyze(element = os.environ.get("Element", "ExactFrame")
            )

