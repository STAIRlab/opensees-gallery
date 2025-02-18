import os
import sys
import veux
import pandas as pd
from steel import WideFlange
import opensees.openseespy as ops_

def render_null(model):
    from scipy.linalg import null_space
    model.constraints("Transformation")
    model.analysis("Static")
    K = model.getTangent().T
    v = null_space(K)[:,0] #, rcond=1e-8)

    def clean(number):
        if abs(number) < 1e-18:
            return 0.0
        return float(number)*5000

    u = {
        tag: [clean(v[dof-1]) if dof > 0 else 0 for dof in model.nodeDOFs(tag)]
        for tag in model.getNodeTags()
    }
    for node in model.getNodeTags():
        print(node)
        print("    ", model.nodeDOFs(node))
    print(u)

    artist = veux.create_artist(model, canvas="gltf")
    artist.draw_outlines()
#   artist.draw_nodes(size=1000)
    artist.draw_outlines(state=u)
    artist.draw_nodes(state=u, size=1000)
    veux.serve(artist)

if __name__ == "__main__":
    # Units = N,mm
    d  = 100
    tw = 3
    bf = 75
    tf = 3
    J  = 2223

    E = 2.0e5 # MPa
    v = 0.27
    G = 0.5*E/(1+v)

    L = 6000
    ne = 12

    ops = ops_.Model(ndm=3, ndf=6) #model('basic','-ndm',3,'-ndf',7)

    mat = 1
    sec = 1
    ops.material('ElasticIsotropic', mat, E, v) #G=G)

    section = WideFlange(d=d, b=bf, t=tf, tw=tw)
    if os.environ["Section"] == "Elastic":
        section.add_to(ops, 1, dict(E=E,G=G), "Elastic")
    else:
        section.add_to(ops, 1, mat)


    Np = 3
    ops.beamIntegration('Legendre',1,1,Np)

    ops.geomTransf("Corotational", 1, (0,0,1))

    ops.node(0, (0,0,0))
    for i in range(ne):
        ops.node(i+1, (0, (i+1)*L/ne, 0))
        ops.element("ForceFrame", i+1, (i, i+1), section=1, transform=1)


    ops.fix(0,  (1,0,1,  0,1,0))
    ops.fix(ne, (1,0,1,  0,1,0))

    # Vertical restraint at middle node
    ops.fix(ne//2, (0,1,0,  0,0,0))

    # MODEL DONE
    artist = veux.create_artist(ops)#, model_config=dict(extrude_outline=section))
    artist.draw_surfaces()
    artist.draw_outlines()


    # Apply torsional moment
    ops.pattern("Plain", 1, "Linear")
    ops.load(ne//2, (0,0,0,  485,0,0), pattern=1)

    ops.system('Umfpack')
    ops.integrator("LoadControl",1/10)
    ops.test("NormDispIncr",1e-8,10,1)
#   ops.test('NormUnbalance',1e-6,10,1)
    ops.algorithm("Newton")

    ops.analysis('Static') #,'-noWarnings')
    ops.print(json="model.json")
    if ops.analyze(1) != 0:
        print(f"Failed initial loading, time is {ops.getTime()}")
        render_null(ops)
        sys.exit()
    artist.draw_outlines(state=ops.nodeDisp)

    # Axial load
    ops.loadConst(time=0)
    ops.pattern('Plain',2,"Linear")
    ops.load(0,  (0, 1,0,  0,0,0), pattern=2)
    ops.load(ne, (0,-1,0,  0,0,0), pattern=2)

    Pmax = 200e3 #/100
    Nsteps = 1000
    ops.integrator("LoadControl", Pmax/Nsteps)#, 5, Pmax/(2*Nsteps), 2*Pmax/(Nsteps))
    ops.test("NormDispIncr",1e-7,10,1)

    u = []
    P = []
    while ops.getTime() < Pmax:
        if ops.analyze(1) != 0:
            print(f"Failed at time = {ops.getTime()}")
            break
        u.append(ops.nodeDisp(ne//2, 4))
        P.append(ops.getTime())


    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.set_xlabel(r"Twist, $\vartheta$")
    ax.set_ylabel("Axial load, $P$")
    ax.set_ylim([0, Pmax])
    ax.plot(u, P)

    plt.show()
#   render_null(model)

    artist.draw_outlines(state=ops.nodeDisp)
    veux.serve(artist)



