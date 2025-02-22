# Test of the warping DOF and Wagner term.
# Lin and Hsiao (2001), Example 1
#
import os
import sys

import veux
from veux.motion import Motion
from shps.shapes import WideFlange
import opensees.openseespy as ops

# External libraries
import numpy as np
import matplotlib.pyplot as plt
try:
    pass
    # plt.style.use("typewriter")
except:
    pass

def create_cantilever(case="a", element="ExactFrame", section="Elastic"):

    E = 29e3 # ksi
    v = 0.33 #0.5*E/G - 1
    G = 0.5*E/(1+v) # 11,200 ksi

    L  = 240
    ne =  5 # 20
    nen = 2
    nn = ne*(nen-1)+1

    model = ops.Model(ndm=3, ndf=7)

    mat = 1
    sec = 1
    model.material('ElasticIsotropic', mat, E, v)

    shape = WideFlange(
                tf = 0.93,
                tw = 0.58,
                d  = 21.62,
                b  = 8.42,
                # saint_venant="linear"
            ).create_shape()

    if section == "Elastic":
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
    else:
        model.section("ShearFiber", 1, GJ=0)
        for fiber in shape.fibers():
            y, z = fiber.location
            model.fiber(y, z, fiber.area, mat, fiber.warp[0], [0,0,0], [0,0,0], section=1)


    model.geomTransf("Linear", 1, (0,0,1))

    for i,x in enumerate(np.linspace(0, L, nn)):
        model.node(i, (x,0,0))

    for i in range(ne):
        start = i * (nen - 1)
        nodes = list(range(start, start + nen))
        model.element(element, i+1, nodes, section=sec, transform=1)

    model.fix(0,     (1,1,1,  1,1,1, int(case in "cb")))
    model.fix(nn-1,  (0,0,0,  0,0,0, int(case in "c")))
    return model, shape


if __name__ == "__main__":
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()

    speed = 1/10
    for case in "abc":
        model, shape = create_cantilever(case,
                                         section = os.environ.get("Section", "ShearFiber"),
                                         element = os.environ.get("Element", "ExactFrame"))
        end = len(model.getNodeTags()) - 1

        # Render
        if case == "c":
            artist = veux.create_artist(model,model_config=dict(
                                        extrude_outline=shape,
                                        section_warping=shape.torsion.model.create_handle(shape.torsion.solution())
                                        ))
            artist.draw_surfaces()
            artist.draw_outlines()
            motion = Motion(artist)
        else:
            motion = None

        # Apply torsional moment
        nsteps =  15
        Mmax   = 1.2e3
        model.pattern("Plain", 1, "Linear")
        model.load(end, (0,0,0,  1,0,0, 0), pattern=1)

        model.system('Umfpack')
        model.integrator("LoadControl", Mmax/nsteps)
        model.test("NormDispIncr",1e-12,5,1)
    #   model.test('NormUnbalance',1e-6,10,1)
        model.algorithm("Newton")
        model.analysis("Static")

        u = []
        P = []
        while model.getTime() < Mmax:
            u.append(model.nodeDisp(end, 4))
            P.append(model.getTime())
            if model.analyze(1) != 0:
                print(f"Failed at time = {model.getTime()}")
                break
            if motion is not None:
                motion.advance(time=model.getTime()*speed)
                motion.draw_sections(rotation=model.nodeRotation,
                                     position=model.nodeDisp,
                                     )
                motion.set_field(lambda tag: model.nodeDisp(tag, 7))

        ax.plot(u, P, "-xo"["abc".index(case)], label=case)

        ax2.plot(
                *zip(*[(model.nodeCoord(node,1), model.nodeDisp(node,7))
                    for node in model.getNodeTags()]),
            label=case
        )


    ax.set_xlabel(r"Twist, $\vartheta$")
    ax.set_ylabel("Torque, $T$")
    ax.set_xlim([0,    2])
    ax.set_ylim([0, Mmax])
    ax.axvline(0, color='black', linestyle='-', linewidth=1)
    ax.axhline(0, color='black', linestyle='-', linewidth=1)
    ax.legend()
    ax2.legend()

    plt.show()

    plt.show()
    plt.savefig("img/e0011.png")

    if motion is not None:
        motion.add_to(artist.canvas)
        if len(sys.argv) > 1:
            artist.save(sys.argv[1])
        else:
            veux.serve(artist)



    # artist.draw_outlines(state=model.nodeDisp)
#   veux.serve(artist)

