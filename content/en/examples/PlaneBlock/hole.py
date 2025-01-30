
import opensees.openseespy as ops
from opensees.helpers import find_node, find_nodes
from veux.stress import node_average
import veux
from shps import plane
from shps.block import create_block


def hole():
    d = 24   # Beam depth
    L = 240  # Beam length
    h = 10   # Hole height
    w = 20   # Hole width
    ne = 6,4

    # Define the element type; first-order Lagrange quadrilateral
    element = plane.Lagrange(1)
    points  = {
            1: (    0.0,   0.0),
            2: (L/2-w/2,   0.0),
            3: (L/2-w/2, d/2-h/2),
            4: (    0.0, d/2-h/2),
    }
    nodes, cells = create_block(ne, element, points=points)
#
    points  = {
            1: (L/2+w/2,   0.0),
            2: (   L   ,   0.0),
            3: (   L   , d/2-h/2),
            4: (L/2+w/2, d/2-h/2),
    }
    other = dict(nodes=nodes, cells=cells)
    nodes, cells = create_block(ne, element, points=points, join=other)
#
    points  = {
            1: (L/2+w/2, d/2-h/2),
            2: (   L   , d/2-h/2),
            3: (   L   , d/2+h/2),
            4: (L/2+w/2, d/2+h/2),
    }
    other = dict(nodes=nodes, cells=cells)
    nodes, cells = create_block(ne, element, points=points, join=other)

#
    points  = {
            1: (L/2+w/2, d/2+h/2),
            2: (   L   , d/2+h/2),
            3: (   L   , d    ),
            4: (L/2+w/2, d    ),
    }
    other = dict(nodes=nodes, cells=cells)
    nodes, cells = create_block(ne, element, points=points, join=other)
#
    points  = {
            1: (  0.0  , d/2+h/2),
            2: (L/2-w/2, d/2+h/2),
            3: (L/2-w/2, d      ),
            4: (  0.0  , d      ),
    }
    other = dict(nodes=nodes, cells=cells)
    nodes, cells = create_block(ne, element, points=points, join=other)
#
    points  = {
            1: (  0.0  , d/2-h/2),
            2: (L/2-w/2, d/2-h/2),
            3: (L/2-w/2, d/2+h/2),
            4: (  0.0  , d/2+h/2),
    }
    other = dict(nodes=nodes, cells=cells)
    nodes, cells = create_block(ne, element, points=points, join=other)
#
    ne = 2,4
    points  = {
            1: (L/2-w/2, d/2+h/2),
            2: (L/2+w/2, d/2+h/2),
            3: (L/2+w/2, d      ),
            4: (L/2-w/2, d      ),
    }
    other = dict(nodes=nodes, cells=cells)
    nodes, cells = create_block(ne, element, points=points, join=other)
# 
    points  = {
            1: (L/2-w/2,   0.0),
            2: (L/2+w/2,   0.0),
            3: (L/2+w/2, d/2-h/2),
            4: (L/2-w/2, d/2-h/2),
    }
    other = dict(nodes=nodes, cells=cells)
    nodes, cells = create_block(ne, element, points=points, join=other)
#
    return nodes, cells

def create_model(mesh,
                thickness=1,
                element: str = "LagrangeQuad"):
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

    for tag, node in mesh[0].items():
        model.node(tag, *node)

    for tag, cell in mesh[1].items():
        model.element(element, tag, tuple(cell), *args)

    # Fix all nodes with coordinate x=0.0
    for node in find_nodes(model, x=0):
        print("Fixing node ", node)
        #         tag   (u1 u2)
        model.fix(node, (1, 1))

    # Fix all nodes with coordinate x=L
    for node in find_nodes(model, x=L):
        print("Fixing node ", node)
        model.fix(node, (1, 1))

    # Define gravity loads
    # create a Plain load pattern with a linear time series
    model.pattern("Plain", 1, "Linear")

    # Load all nodes with y-coordinate equal to `d`
    top = list(find_nodes(model, y=d))
    for node in top:
        model.load(node, (0.0, -load/len(top)), pattern=1)

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

    mesh = hole()
    model = create_model(mesh, element="quad")
    start = time.time()
    static_analysis(model)
    print(f"Finished {time.time() - start} sec")
    print(model.nodeDisp(find_node(model, x=240, y=0)))


    import veux
    artist = veux.create_artist(model)

    stress = {node: stress["sxx"] for node, stress in node_average(model, "stressAtNodes").items()}

    artist.draw_surfaces(state=model.nodeDisp, field = stress, scale=10)
    artist.draw_outlines()
    veux.serve(artist)


#       print(model.nodeDisp(l2))



# if __name__ == "__main__":
#     nodes, cells = hole()
# #
#     artist = veux.create_artist((nodes, cells), canvas="gltf")
#     artist.draw_nodes()
#     artist.draw_surfaces()
#     artist.draw_outlines()
#     veux.serve(artist)

