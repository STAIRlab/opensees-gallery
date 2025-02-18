
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

def create_cantilever(ne, offset):
    model = ops.Model(ndm=3, ndf=6)

    E = 2.1e4 # MPa
    v = 0.30 #0.5*E/G - 1
    G = 0.5*E/(1+v) # 787500

    L  = 900


    mat = 1
    sec = 1
    model.material('ElasticIsotropic', mat, E, v) #G=G)

    section = Channel(d=30, b=10, tf=1.6, tw=1.0)\
              .create_model()\
              .translate(offset)


    _m = section.mesh
    # veux.serve(veux.render((_m.nodes, _m.cells())))

    print(section.summary())
    if os.environ["Section"] == "Elastic":
        cmm = section.torsion.cmm()
        cnn = section.torsion.cnn()
        cnv = section.torsion.cnv()
        cnm = section.torsion.cnm()
        cmw = section.torsion.cmw()
        A = cnn[0,0]
        model.section("ElasticFrame", sec,
                        E=E,
                        G=G,
                        A=A,
                        Ay=100*A,
                        Az=100*A,
                        Qy=cnm[0,1],
                        Qz=cnm[2,0],
                        Iy=cmm[1,1],
                        Iz=cmm[2,2],
                        J =section.torsion.torsion_constant(),
                        Ry= cnv[1,0],
                        Rz=-cnv[2,0],
                        Sy= cmw[1,0],
                        Sz=-cmw[2,0]
        )
    else:
        model.section("ShearFiber", sec, GJ=0)
        for fiber in section.fibers():
            y, z = fiber.location
            model.fiber(y, z, fiber.area, mat, fiber.warp[0], fiber.warp[1], [0,0,0],  section=sec)
#               model.fiber(y, z, fiber.area, mat_tag, section=tag)


    model.geomTransf("Corotational", 1, (0,1,0))
    element = os.environ.get("Element", "ExactFrame")

    model.node(0, (0,0,0))
    for i in range(ne):
        model.node(i+1, ((i+1)*L/ne, 0, 0))
        model.element(element, i+1, (i, i+1), section=1, transform=1)

    model.fix(0,  (1,1,1,  1,1,1))

    return model, section

def analyze(concentric=True):
    ne = 20
    if concentric:
        offset = (0, 15)
    else:
        offset = (0,  0)

    model,section = create_cantilever(ne, offset)
    artist = veux.create_artist(model, model_config=dict(extrude_outline=section))
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
    if concentric:
        model.load(ne, (0,-1,0,  0,0,0), pattern=1)
    else:
        model.eleLoad("Frame", "Dirac",
                      force = [0, -1, 0],
                      basis = "global",
                      offset=[1.0, 0, 15],
                      pattern=1,
                      elements=[ne]
        )

    # model.system('Umfpack')
    model.integrator("LoadControl", Pmax/5000)#, 8, Pmax/500, Pmax/2)
    model.test("NormDispIncr", 1e-8, 100, 1)
#   model.test('NormUnbalance',1e-6,10,1)
    model.algorithm("Newton")
    model.analysis('Static') #,'-noWarnings')

    v = []
    w = []
    P = []
    while model.getTime() < Pmax:
        motion.advance(time=model.getTime()*speed)
        motion.draw_sections(rotation=model.nodeRotation,
                             position=model.nodeDisp)
        v.append(-model.nodeDisp(ne, 2))
        w.append( model.nodeDisp(ne, 3))
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
    ax.plot(v, P, ".", label="$v$")
    ax.plot(w, P, ".", label="$w$")
    ax.legend()
    plt.show()

    motion.add_to(artist.canvas)
    veux.serve(artist)

if __name__ == "__main__":
    analyze(True)

