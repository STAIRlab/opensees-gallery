# import the OpenSees Python module
import opensees.openseespy as ops
from opensees.helpers import find_node, find_nodes
from veux.stress import node_average

def create_beam(mesh,
                thickness=1,
                element: str = "LagrangeQuad"):

    nx, ny = mesh
    # Define geometry
    # ---------------

    L = 240.0
    d = 24.0
    thick = 1.0
    load = 20.0 # kips


    # create model in two dimensions with 2 DOFs per node
    model = ops.Model(ndm=2, ndf=2)

    # Define the material
    # -------------------
    #                                 tag  E      nu   rho
    model.material("ElasticIsotropic", 1, 4000.0, 0.25, 0, "-plane-strain")

    # now create the nodes and elements using the surface command
    # {"quad", "enhancedQuad", "tri31", "LagrangeQuad"}:
    args = (thick, "PlaneStrain", 1)

    surface = model.surface((nx, ny),
                  element=element, args=args,
                  points={
                    1: [  0.0,   0.0],
                    2: [   L,    0.0],
                    3: [   L,     d ],
                    4: [  0.0,    d ]
            })

    # Single-point constraints
    #            x   (u1 u2)
    for node in find_nodes(model, x=0):
        print("Fixing node ", node)
        model.fix(node, (1, 1))

    for node in find_nodes(model, x=L):
        print("Fixing node ", node)
        model.fix(node, (1, 1))

    # Define gravity loads
    # create a Plain load pattern with a linear time series
    model.pattern("Plain", 1, "Linear")

    # Fix all nodes with y-coordinate equal to `d`
    tip = list(find_nodes(model, y=d))
    for node in tip:
        model.load(node, (0.0, -load/len(tip)), pattern=1)

    return model


def static_analysis(model):

    # Define the load control with variable load steps
    model.integrator("LoadControl", 1.0, 1, 1.0, 10.0)

    # Declare the analysis type
    model.analysis("Static")

    # Perform static analysis in 10 increments
    model.analyze(10)


if __name__ == "__main__":
    import time
    for element in "LagrangeQuad", "quad":
        model = create_beam((20,8), element=element)
        start = time.time()
        static_analysis(model)
        print(f"Finished {element}, {time.time() - start} sec")
        print(model.nodeDisp(find_node(model, x=100, y=15)))


    import veux
    artist = veux.create_artist(model)

    stress = {node: stress["sxx"] for node, stress in node_average(model, "stressAtNodes").items()}

    artist.draw_surfaces(field = stress)
    artist.draw_outlines()
    veux.serve(artist)


#       print(model.nodeDisp(l2))

