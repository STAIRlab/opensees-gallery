#
# Narrow cantilever with a terminal transverse load
#
# TMTE Article 95
#
import os
import xara
import veux
from xara.units.iks import kip, inch, foot, ksi
from xara.load import SurfaceLoad, Line
from xara.helpers import find_node, find_nodes
from veux.stress import node_average
import matplotlib.pyplot as plt
try:
    plt.style.use("veux-web")
except:
    pass


def f(x):
    return [0,  12*(1/4 - (x-1/2)**2)]

def create_beam(splits,          # Number of elements in the x and y directions
                length,
                depth, width, # Shape dimensions
                material,
                order=1,      # Element interpolation order
                element = "quad",
                section = "PlaneStress"
    ):

    nx, ny = splits

    E = material["E"]
    nu = material["nu"]


    #
    # Create model
    #
    # create model in two dimensions with 2 DOFs per node
    model = xara.Model(ndm=2, ndf=2)

    # Define the material
    # -------------------

    model.material("ElasticIsotropic", 1, E, nu, 0)
    model.section(section, 1, 1, width)


    # Define geometry
    # ---------------
    # now create the nodes and elements using the surface command
    L = length
    d = depth
    mesh = model.surface((nx, ny),
                  element=element,
                  args={"section": 1},
                  order=order,
                  points={
                    1: [  0.0,   -d/2],
                    2: [   L,    -d/2],
                    3: [   L,     d/2 ],
                    4: [  0.0,    d/2 ]
            })

    # Fix nodes
    for node in find_nodes(model, x=0):
        if model.nodeCoord(node)[1] == 0:
            model.fix(node, (1, 1))
        else:
            model.fix(node, (1, 0))

    # for node in find_nodes(model, x=0, y=0):
    #     model.fix(node, (1, 1))
    # for node in find_nodes(model, x=0, y=d/2):
    #     model.fix(node, (1, 0))
    # for node in find_nodes(model, x=0, y=-d/2):
    #     model.fix(node, (1, 0))

    #
    # Define loads
    #
    # create a Plain load pattern with a linear time series
    model.pattern("Plain", 1, "Linear")

    tip_nodes = sorted(find_nodes(model, x=L), key=lambda n: model.nodeCoord(n)[1])
    tip_load = SurfaceLoad(Line(model, tip_nodes), f, scale=-1)

    for node, force in tip_load.nodal_loads():
        print(model.nodeCoord(node), force)
        model.load(node, (0, force[1]), pattern=1)

    region = Line(model, sorted(find_nodes(model, x=0), key=lambda n: model.nodeCoord(n)[1]))
    root_load = SurfaceLoad(region, f)


    for node, force in root_load.nodal_loads():
        model.load(node, (0, force[1]), pattern=1)

    #
    # Run Analysis
    #
    model.integrator("LoadControl", 1.0)
    model.analysis("Static")
    model.analyze(1)


    return model




if __name__ == "__main__":
    fig, ax = plt.subplots()
    length = 50*inch
    depth  = 10*inch
    width  = 1.0*inch
    E = 10_000.0*ksi
    nu = 0.25
    G = E / (2*(1 + nu))

    A = depth*width
    Ay = 5/6*A
    I = depth**3*width/12
    P = 20

    u = 1/3*P*length**3/(E*I) + P*length/(Ay*G)

    order = int(os.getenv("Order", 1))
    if order == 1:
        splits = 6,2
    else:
        splits = 3,1

    splits = 6,2

    model = create_beam(splits,
                        length=length,
                        depth = depth,
                        width = width,
                        element="quad",
                        material={"E": E, "nu": nu},
                        order=order
            )

    print(-u)
    print(model.nodeDisp(find_node(model, x=length, y=0), 2))

    artist = veux.create_artist(model, canvas="gltf")

    stress = {node: stress["sxx"] for node, stress in node_average(model, "stressAtNodes").items()}

    artist.draw_nodes()
    artist.draw_outlines()
    artist.draw_surfaces(state=model.nodeDisp, scale=1, field=stress)
#   artist.draw_surfaces(field = stress)
    artist.draw_outlines(state=model.nodeDisp, scale=1)
    veux.serve(artist)



