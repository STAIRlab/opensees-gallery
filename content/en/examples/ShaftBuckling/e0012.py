# GS&W 2000, 6.1
# Simply supported channel
import os
import veux
from veux.motion import Motion
from steel import Channel
import opensees.openseespy as ops
import matplotlib.pyplot as plt
try:
    pass
    # plt.style.use("typewriter")
except:
    pass


if __name__ == "__main__":
    model = ops.Model(ndm=3, ndf=6)

    E = 2.1e4 # MPa
    v = 0.30 #0.5*E/G - 1
    G = 0.5*E/(1+v) # 787500

    L  = 150
    ne = 20


    mat = 1
    sec = 1
    model.material('ElasticIsotropic', mat, E, v) #G=G)

    section = Channel(d=10, b=10, tf=0.2, tw=0.2).create_model()
    section = section.translate(section.centroid())


    # _m = section.mesh
    # veux.serve(veux.render((_m.nodes, _m.cells())))

    print(section.summary())
    if os.environ["Section"] == "Elastic":
        cmm = section.torsion.cmm()
        cnn = section.torsion.cnn()
        A = cnn[0,0]
        model.section("ElasticFrame", 1,
                        E=E,
                        G=G,
                        A=A,
                        Ay=100*A,
                        Az=100*A,
                        Iy=cmm[1,1],
                        Iz=cmm[2,2],
                        J =section.torsion.torsion_constant()
        )
    else:
        model.section("ShearFiber", 1, GJ=0)
        for fiber in section.fibers():
            y, z = fiber.location
            model.fiber(y, z, fiber.area, mat, fiber.warp[0], fiber.warp[1], [0,0,0],  section=1)


    model.geomTransf("Corotational", 1, (0,1,0))
    element = os.environ.get("Element", "ExactFrame")

    model.node(0, (0,0,0))
    for i in range(ne):
        model.node(i+1, ((i+1)*L/ne, 0, 0))
        model.element(element, i+1, (i, i+1), section=1, transform=1)

    model.fix(0,  (1,1,1,  1,0,0))
    model.fix(ne, (0,1,1,  1,0,0))


    artist = veux.create_artist(model, model_config=dict(extrude_outline=section))
    artist.draw_nodes(size=10)
    # artist.draw_sections()
    # veux.serve(artist)
    motion = Motion(artist)

    model.pattern("Plain", 2, "Constant", loads={
        ne: (0,0,-0.01,  0,0,0)
    })
    model.integrator("LoadControl", 1)
    model.analysis("Static")
    model.analyze(1)
    print(model.nodeDisp(ne))
    # Apply vertical load
    speed  = 1/2 # animation frames
    Pmax   = 120 # kN
    model.pattern("Plain", 1, "Linear")
    model.load(ne, (-1,0,0,  0,0,0), pattern=1)

    model.system('Umfpack')
    model.integrator("LoadControl", Pmax/20, 8, Pmax/500, Pmax/2)
    model.test("NormDispIncr", 1e-10, 100, 0)
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
    ax.set_ylim([0,   Pmax])
    ax.axvline(0, color='black', linestyle='-', linewidth=1)
    ax.axhline(0, color='black', linestyle='-', linewidth=1)
    ax.plot(u, P, ".", label="$u(L)$")
    ax.plot(w, P, ".", label="$w(L/2)$")
    ax.legend()
    plt.show()

    motion.add_to(artist.canvas)
    veux.serve(artist)

