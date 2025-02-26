# Cantilever with channel section and eccentric loading
#
import veux
from veux.motion import Motion
from shps.shapes import Channel
import opensees.openseespy as ops

# External libraries
import numpy as np
import matplotlib.pyplot as plt
try:
    plt.style.use("veux-web")
except:
    pass

def create_cantilever(ne, offset, element, section, nen=2):
    model = ops.Model(ndm=3, ndf=6)

    E = 2.1e4 # MPa, or 210 GPa
    v = 0.30 #0.5*E/G - 1
    G = 0.5*E/(1+v) # 8076.92

    nmn = ne*(nen-1)+1
    L  = 900


    mat = 1
    sec = 1
    model.material('ElasticIsotropic', mat, E, v) #G=G)

    shape = Channel(d=30, b=10, tf=1.6, tw=1.0).create_shape()

    shape = shape.translate(offset)


    # _m = shape.mesh
    # veux.serve(veux.render((_m.nodes, _m.cells())))

    if "fiber" in section.lower():
        warp = os.environ.get("Warp", None)
        print(f"Section = Fiber; ", warp)
        model.section("ShearFiber", sec, GJ=0)

        for fiber in shape.fibers(warp=warp):
            y, z = fiber.location
            model.fiber(y, z, fiber.area, mat, fiber.warp[0], section=sec) #fiber.warp[1], section=sec)

    else:
        print("Section = Elastic")
        cmm = shape.torsion.cmm()
        cnn = shape.torsion.cnn()
        cnv = shape.torsion.cnv()
        cnm = shape.torsion.cnm()
        cmw = shape.torsion.cmw()
        A = cnn[0,0]
        model.section("ElasticFrame", sec,
                        E=E,
                        G=G,
                        A=A,
                        Ay=1*A,
                        Az=1*A,
                        Qy=cnm[0,1],
                        Qz=cnm[2,0],
                        Iy=cmm[1,1],
                        Iz=cmm[2,2],
                        J =shape.torsion.torsion_constant(),
                        Ry= cnv[1,0],
                        Rz=-cnv[2,0],
                        Sy= cmw[1,0],
                        Sz=-cmw[2,0]
        )


#   model.geomTransf("Corotational", 1, (0,1,0))
    model.geomTransf("Corotational", 1, (0,0,1))

    for i,x in enumerate(np.linspace(0, L, nmn)):
        model.node(i, (x,0,0))

    model.fix(0,  (1,1,1,  1,1,1))

    for i in range(ne):
        start = i * (nen - 1)
        nodes = list(range(start, start + nen))
        model.element(element, i+1, nodes, section=sec, transform=1)


    return model, shape

def analyze(element, section, pattern="node", nen=2):
    ne = 20
    en = ne*(nen-1)
    if pattern == "node":
        offset = (0, 15)
    else:
        offset = (0,  0)

    model,shape = create_cantilever(ne, offset, element=element, section=section, nen=nen)
    if False:
        artist = veux.create_artist(model, model_config=dict(extrude_outline=shape))
        artist.draw_nodes(size=10)
        # artist.draw_sections()
        # veux.serve(artist)
        motion = Motion(artist)

    #
    # Apply vertical load
    #
    speed  = 1 # animation frames
    Pmax   = 20 # kN
    model.pattern("Plain", 1, "Linear")
    if pattern == "node":
        print("Pattern = node")
        model.load(en, (0,0,-1,  0,0,0), pattern=1)
#       model.load(ne, (0,-1,0,  0,0,0), pattern=1)

    else:
        print("Pattern = element")
        model.eleLoad("Frame", "Dirac",
                      force = [0, 0, -1],
                      basis = "global",
                      offset=[1.0,0, -15],
                      pattern=1,
                      elements=[ne]
        )

    model.system('Umfpack')
    model.integrator("LoadControl", Pmax/1000)#, 8, Pmax/500, Pmax/2)
    model.test("NormDispIncr", 1e-8, 100, 0)
#   model.test('NormUnbalance',1e-6,10,1)
    model.algorithm("Newton")
    model.analysis("Static")
#   input()

    u = []
    v = []
    w = []
    P = []
#   for i in range(50):
    while model.getTime() < Pmax:
#       motion.advance(time=model.getTime()*speed)
#       motion.draw_sections(rotation=model.nodeRotation,
#                            position=model.nodeDisp)
#       u.append(-model.nodeDisp(ne, 1))
#       v.append( model.nodeDisp(ne, 2))
#       w.append(-model.nodeDisp(ne, 3))
#       P.append( model.getTime())
        if model.analyze(1) != 0:
            print(f"Failed at time = {model.getTime()} with v = {v[-1]}")
            break


    if False:
        fig, ax = plt.subplots()
        ax.set_xlabel(r"Displ, $v$")
        ax.set_ylabel("Load, $P$")
        # ax.set_xlim([0,    300])
        ax.set_ylim([0,   Pmax])
        ax.axvline(0, color='black', linestyle='-', linewidth=1)
        ax.axhline(0, color='black', linestyle='-', linewidth=1)
        ax.plot(u, P, label="$u$")
        ax.plot(v, P, label="$v$")
        ax.plot(w, P, label="$w$")
        ax.legend()
        fig.savefig("img/e0013.png")
        plt.show()

        motion.add_to(artist.canvas)
        veux.serve(artist)

if __name__ == "__main__":
    import os
    analyze(pattern = os.environ.get("Pattern", "node"),
            element = os.environ.get("Element", "ExactFrame"),
            section = os.environ.get("Section", "ShearFiber"),
            nen=2
            )

