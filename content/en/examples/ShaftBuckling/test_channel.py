import sys
import veux
import numpy as np
import pandas as pd
import opensees.openseespy as ops
from steel import Channel, Rectangle

def _test_opensees(section):
    model = ops.Model(ndm=3, ndf=6) 
    E    = 1 #29000*ksi,
    nu   = -0.5 #.2
    model.material("ElasticIsotropic", 1, E, nu, 0.0)
    model.section("ShearFiber", 1, GJ=0)
    for fiber in section.fibers():
        y, z = fiber.location
        model.fiber(y, z, fiber.area, 1, fiber.warp[0], fiber.warp[1], [0,0,0],  section=1)
#               model.fiber(y, z, fiber.area, mat_tag, section=tag)

    tangent = model.invoke("section", 1, [
                           "update  0 0 0 0 0 0;",
                           "tangent"
            ])

    n = int(np.sqrt(len(tangent)))
    Ks = np.array(tangent).reshape(n,n)
    # Ks = np.round(Ks, 4)
    # print(pd.DataFrame(Ks))

    cnn = Ks[:3,:3]
    cmm = Ks[3:6,3:6]
    cnm = Ks[:3,3:6]
    cnw = Ks[:3,6:9]
    cnv = Ks[:3,9:12]
    cmv = Ks[3:6,9:12]
    cww = Ks[6:9,6:9]
    cvv = Ks[9:12,9:12]
    print(f"{cnm = }")
    print(f"{cnw = }")
    print(f"{cnv = }")

    s = ""
    tol=1e-13
    A = cnn[0,0]

    Ay = cnm[0,1] # int z
    Az = cnm[2,0] # int y
    # Compute centroid
    cx, cy = float(Az/A), float(Ay/A)
    cx, cy = map(lambda i: i if abs(i)>tol else 0.0, (cx, cy))


    Ivv = cvv[0,0]
    Irw = cmv[0,0]


    Isv = cmm[0,0] - Ivv

    s += f"""
[nn]  Area                 {A  :>10.4}
[nm]  Centroid             {cx :>10.4},{cy :>10.4}
[mm]  Flexural moments  xx {cmm[0,0] :>10.4}
                        yy {cmm[1,1] :>10.4}
                        zz {cmm[2,2] :>10.4}
                        yz {cmm[1,2] :>10.4}

[mv]                    xx {Irw :>10.4}
[ww]  Warping constant     {cww[0,0] :>10.4}
      Torsion constant     {Isv :>10.4}
[vv]  Bishear           xx {Ivv :>10.4}
    """
    print(s)

if __name__ == "__main__":
    case = "s0002" if len(sys.argv) < 2 else sys.argv[1]

    # shaft-
    benchmarks = dict(
        s0001 = dict(
            section=Rectangle(
                d  = 10,
                b  = .5
            ),
            offset="centroid"
        ),
        s0002 = dict(
            section=Channel(
        # G, S & W, 6.1
                tf =  0.2,
                tw =  0.2,
                b  = 10.0,
                d  = 10.0
            ),
            offset = "centroid"
        ),
        # G, S & W, 6.2
        s0003 = dict(
            section=Channel(
                tf =  1.6,
                tw =  1.0,
                b  = 10.0,
                d  = 30.0
            ),
            offset = (0,0)
        )
    )

    # 
    # Pilkey ?
#   t =  1.0
#   w = t
#   b = 8.50
#   h = 19.0

#   t =  12.7
#   w = t
#   b = 74.0
#   h = 305.0

    # Lacarbonara, Example 6.4
#   t = 10.5
#   w = 7.5
#   d = 160
#   b = 65
#   o = "centroid"


    section = benchmarks[case]["section"].create_model()
    d = benchmarks[case]["section"].d
    o = benchmarks[case]["offset"]

#   section = section.translate(section.torsion.centroid()).translate([-18.4, 0])
#   print(section.summary())

    if o == "shear-center":
        section = section.translate(section.torsion.shear_center())

    elif o == "centroid":
        section = section.translate(section.torsion.centroid())

    else:
        section = section.translate(o)

    print(section.summary())

    _test_opensees(section)

    # 1) create basic section
    basic = section.linearize()

    field = section.torsion.warping()

    # 3) view warping modes
    artist = veux.create_artist((section.mesh.nodes, section.mesh.cells()), ndf=1)

    field = {node: value/100.0 for node, value in enumerate(field)}

    artist.draw_surfaces(field = field, state=field)
    artist.draw_outlines()
    R = artist._plot_rotation

    artist.canvas.plot_vectors([[0,0,0] for i in range(3)], d/5*R.T)
    artist.canvas.plot_vectors([R@[*section.torsion.shear_center(), 0] for i in range(3)], d/5*R.T)
    artist.draw_outlines()
    veux.serve(artist)

