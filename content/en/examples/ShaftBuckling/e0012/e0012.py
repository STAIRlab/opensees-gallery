# GS&W 2000, 6.1
# Simply supported channel, free to warp
import os

import veux
from veux.motion import Motion
from shapes import Channel
import opensees.openseespy as ops

import matplotlib.pyplot as plt
try:
    pass
    # plt.style.use("typewriter")
except:
    pass


if __name__ == "__main__":
    model = ops.Model(ndm=3, ndf=7)

    E = 2.1e4 # MPa
    v = 0.30 #0.5*E/G - 1
    G = 0.5*E/(1+v) # 787500

    L  = 150
    ne = 5


    mat = 1
    sec = 1
    model.material('ElasticIsotropic', mat, E, v) #G=G)

    shape = Channel(d=10, b=10, tf=0.2, tw=0.2).create_shape()
    shape = shape.translate(shape.centroid())


    # _m = section.mesh
    # veux.serve(veux.render((_m.nodes, _m.cells())))

    print(shape.summary())
    if os.environ["Section"] == "Elastic":
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
            model.fiber(y, z, fiber.area, mat, fiber.warp[0], section=1)


    model.geomTransf("Linear", 1, (0,0,1))
    element = os.environ.get("Element", "ExactFrame")

    model.node(0, (0,0,0))
    for i in range(ne):
        model.node(i+1, ((i+1)*L/ne, 0, 0))
        model.element(element, i+1, (i, i+1), section=1, transform=1)

    model.fix(0,  (1,1,1,  1,0,0, 0))
    model.fix(ne, (0,1,1,  1,0,0, 0))


    artist = veux.create_artist(model, model_config=dict(extrude_outline=shape))
    artist.draw_nodes(size=10)
    # artist.draw_sections()
    # veux.serve(artist)
    motion = Motion(artist)

    if True:
        model.pattern("Plain", 2, "Constant", loads={
            ne: (0,0,0, -1,0,0, 0)
        })
        model.integrator("LoadControl", 1)
        model.analysis("Static")
        model.analyze(1)
        print(model.nodeDisp(ne))

    # Apply vertical load
    speed  = 1/2 # animation frames
    Pmax   = 300 # kN
    model.pattern("Plain", 1, "Linear")
    model.load(ne, (-1,0,0,  0,0,0, 0), pattern=1)

    model.system('Umfpack')
    model.integrator("LoadControl", Pmax/1000)#, 8, Pmax/500, Pmax/2)
    model.test("NormDispIncr", 1e-8, 5, 1)
#   model.test('NormUnbalance',1e-6,10,1)
    model.algorithm("Newton")
    model.analysis('Static') #,'-noWarnings')

    u = []
    w = []
    P = []
    while model.getTime() < Pmax:
        motion.advance(time=model.getTime()*speed)
        motion.draw_sections(rotation=model.nodeRotation,
                             position=model.nodeDisp)
        print(model.nodeDisp(ne))
        u.append(-model.nodeDisp(ne, 1))
        w.append( model.nodeDisp(ne//2, 2))
        P.append( model.getTime())
        if model.analyze(1) != 0:
            print(f"Failed at time = {model.getTime()}")
            break


    fig, ax = plt.subplots()
    ax.set_xlabel(r"Displ, $v$")
    ax.set_ylabel("Load, $P$")
    # ax.set_xlim([0,    300])
#   ax.set_ylim([0,   Pmax])
    ax.axvline(0, color='black', linestyle='-', linewidth=1)
    ax.axhline(0, color='black', linestyle='-', linewidth=1)
    ax.plot(u, P, ".", label="$u(L)$")
    ax.plot(w, P, ".", label="$w(L/2)$")
    ax.legend()
    plt.show()

    motion.add_to(artist.canvas)
    veux.serve(artist)

