import veux
import xara
from veux.motion import Motion
from xara.units.fks import kip, sec, foot, inch, pcf, ksi, gravity

import xara
import veux
from veux.motion import Motion
from xara.units.fks import kip, sec, foot, inch, pcf, ksi, gravity

import numpy as np
import matplotlib.pyplot as plt
try:
    plt.style.use("veux-web")
except:
    pass

# ------------------------------------------------------------
# 1. build the model
# ------------------------------------------------------------
def build_model():
    # 3-D, 6 dof per node
    model = xara.Model(ndm=3, ndf=6)

    # Dimensions
    story_height = 12*foot
    bay = 24*foot

    # node tags
    base = [1, 2, 3, 4]
    roof = [5, 6, 7, 8]

    # node coordinates
    coords = {
        1: (-bay/2,  bay/2,          0.0),
        2: ( bay/2,  bay/2,          0.0),
        3: ( bay/2, -bay/2,          0.0),
        4: (-bay/2, -bay/2,          0.0),
        5: (-bay/2,  bay/2, story_height),
        6: ( bay/2,  bay/2, story_height),
        7: ( bay/2, -bay/2, story_height),
        8: (-bay/2, -bay/2, story_height),
    }

    for tag, xyz in coords.items():
        model.node(tag, xyz)

    # base fixities (fully fixed)
    for tag in base:
        model.fix(tag, (1, 1, 1, 1, 1, 1))

    # -----------------------------------------------------------------
    # Materials and Sections
    # -----------------------------------------------------------------
    E       = 29500.0*ksi
    poisson = 0.3
    density = 490.0*pcf
    depth   = 20*inch
    area    = depth**2
    i_zz    = depth**4 / 12.0
    i_yy    = i_zz
    j_tors  = 10*i_zz   # arbitrary large, torsion not important

    # Create a section for the columns with label 1
    model.section("ElasticFrame", 1,
                  E = E, 
                  G = E / (2.0 * (1.0 + poisson)),
                  A = area, 
                  Iz=i_zz, 
                  Iy=i_yy,
                  J=j_tors
    )

    thickness = 6*inch
    model.section("ElasticShell", 2, E, poisson, thickness, density)


    # -----------------------------------------------------------------
    # Elements
    # -----------------------------------------------------------------

    # Columns
    model.geomTransf("Linear", 1, (0, 1, 0))   # local z = global y

    for tag, (ni, nj) in enumerate(zip(base, roof), start=1):
        model.element("PrismFrame", tag, (ni, nj), section=1, transform=1)

    # Create a shell element for the roof
    model.element("ASDShellQ4", 5, roof, section=2)



    # Define gravity loads
    # create a Plain load pattern with Constant scaling
    model.pattern("Plain", 1, "Constant")

    p = density*bay**2*thickness*gravity/len(roof)
    for i in roof:
        model.load(i, (0.0, 0.0, -p, 0.0, 0.0, 0.0), pattern=1)

    # set rayleigh damping factors
    model.rayleigh(0.0, 0.0, 0.0, 0.0018)
    return model



def analyze(model):

    # 1. Define earthquake excitation
    # 
    dt = 0.02
    # Set up the acceleration records for Tabas fault normal and fault parallel
    model.timeSeries("Path", 2, values=np.loadtxt("tabasFN.txt").tolist(), dt=dt, factor=gravity)
    model.timeSeries("Path", 3, values=np.loadtxt("tabasFP.txt").tolist(), dt=dt, factor=gravity)


    # Define the excitation using the Tabas ground motion records
    #                                 tag DOF  accel series
    model.pattern("UniformExcitation", 2,  1,   accel=2)
    model.pattern("UniformExcitation", 3,  2,   accel=3)

    # 
    # 2. Configure the analysis
    # 

    # Use sparse matrix solver
    model.system("UmfPack")
    model.constraints("Plain")

    # Configure the analysis such that iterations are performed until either:
    # 1. the energy increment is less than 1.0e-8 (success)
    # 2. the number of iterations surpasses 20 (failure)
    model.test("EnergyIncr", 1.0e-10, 10)

    # Perform iterations with the Newton-Raphson algorithm
    model.algorithm("Newton")

    # define the integration scheme, the Newmark with gamma=0.5 and beta=0.25
    model.integrator("Newmark", 0.5, 0.25)

    # Define the analysis
    model.analysis("Transient")

    # 
    # 3. Perform the analysis
    # 
    roof = [node for node in model.getNodeTags() if model.nodeCoord(node)[2] != 0.0]

    # record once at time 0
    displacements = {
        node: [model.nodeDisp(node)] for node in roof
    }

    # Perform 2500 analysis steps with a time step of 0.01
    for i in range(2500):
        status = model.analyze(1, 0.02)
        if status != xara.successful:
            raise RuntimeError(f"analysis failed at time {model.getTime()}")

        # Save displacements at the current time
        for node in roof:
            displacements[node].append(model.nodeDisp(node))

    return displacements

if __name__ == "__main__":
    model = build_model()
    displacements = analyze(model)

    artist = veux.create_artist(model, vertical=3)
    motion = Motion(artist)

    for i in range(2500):
        motion.draw_sections(state=lambda node: 1000*np.array(displacements[node][i]) if node in displacements else [0,0,0,0,0,0])

    motion.add_to(artist.canvas)
    veux.serve(artist)
