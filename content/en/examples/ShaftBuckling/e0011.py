# Test of the Wagner strain term.
# Battini et al. (2002a), example 7.4
#
import os
import sys
import veux
import pandas as pd
from steel import Rectangle
import opensees.openseespy as ops
import matplotlib.pyplot as plt
try:
    pass
    # plt.style.use("typewriter")
except:
    pass


if __name__ == "__main__":
    d  = 10
    b  = .5

    E = 2.1e6 # MPa
    v = 0.33 #0.5*E/G - 1
    G = 0.5*E/(1+v) # 787500
    print(G)

    L  = 100
    ne = 10 # 20

    model = ops.Model(ndm=3, ndf=6)

    mat = 1
    sec = 1
    model.material('ElasticIsotropic', mat, E, v) #G=G)

    section = Rectangle(d=d, b=b)
    if os.environ["Section"] == "Elastic":
        section.add_to(model, 1, dict(E=E,G=G), "Elastic")
    else:
        section.add_to(model, 1, mat)

    model.geomTransf("Corotational", 1, (0,0,1))
    element = os.environ.get("Element", "ExactFrame")

    model.node(0, (0,0,0))
    for i in range(ne):
        model.node(i+1, ((i+1)*L/ne, 0, 0))
        model.element(element, i+1, (i, i+1), section=1, transform=1)

    model.fix(0,  (1,1,1,  1,1,1))


    # MODEL DONE
    artist = veux.create_artist(model)#, model_config=dict(extrude_outline=section))
    artist.draw_surfaces()
    artist.draw_outlines()

    # Apply torsional moment
    nsteps =  15
    Mmax   = 9e3
    model.pattern("Plain", 1, "Linear")
    model.load(ne, (0,0,0,  1,0,0), pattern=1)

    model.system('Umfpack')
    model.integrator("LoadControl", Mmax/nsteps)
    model.test("NormDispIncr",1e-8,100,1)
#   model.test('NormUnbalance',1e-6,10,1)
    model.algorithm("Newton")
    model.analysis('Static') #,'-noWarnings')

    u = []
    P = []
    while model.getTime() < Mmax:
        u.append(model.nodeDisp(ne, 4))
        P.append(model.getTime())
        if model.analyze(1) != 0:
            print(f"Failed at time = {model.getTime()}")
            break


    fig, ax = plt.subplots()
    ax.set_xlabel(r"Twist, $\vartheta$")
    ax.set_ylabel("Torque, $T$")
    ax.set_xlim([0,    2])
    ax.set_ylim([0, Mmax])
    ax.axvline(0, color='black', linestyle='-', linewidth=1)
    ax.axhline(0, color='black', linestyle='-', linewidth=1)
    ax.plot(u, P)

    plt.show()
#   render_null(model)

    artist.draw_outlines(state=model.nodeDisp)
#   veux.serve(artist)

