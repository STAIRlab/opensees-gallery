import xara
import veux
import numpy as np
from shps.frame.extrude import ExtrudeHexahedron
from shps import plane
from shps.block import create_block
from xara.post import NodalStress

def tube_section(order=1):
    d = 24     # depth
    L = 20     # width
    h = d/1.2  # Hole height
    w = L/1.2  # Hole width

    nw  = 2
    nf  = 2
    nh  = 8
    nb  = 8

    # Define the element type; first-order Lagrange quadrilateral
    element = plane.Lagrange(order)
    points  = {
            1: (    0.0,   0.0),
            2: (L/2-w/2,   0.0),
            3: (L/2-w/2, d/2-h/2),
            4: (    0.0, d/2-h/2),
    }
    nodes, cells = create_block((nw,nf), element, points=points)
#
    points  = {
            1: (L/2+w/2,   0.0),
            2: (   L   ,   0.0),
            3: (   L   , d/2-h/2),
            4: (L/2+w/2, d/2-h/2),
    }
    other = dict(nodes=nodes, cells=cells)
    nodes, cells = create_block((nw,nf), element, points=points, join=other)
#
    points  = {
            1: (L/2+w/2, d/2-h/2),
            2: (   L   , d/2-h/2),
            3: (   L   , d/2+h/2),
            4: (L/2+w/2, d/2+h/2),
    }
    other = dict(nodes=nodes, cells=cells)
    nodes, cells = create_block((nw,nh), element, points=points, join=other)

#
    points  = {
            1: (L/2+w/2, d/2+h/2),
            2: (   L   , d/2+h/2),
            3: (   L   , d    ),
            4: (L/2+w/2, d    ),
    }
    other = dict(nodes=nodes, cells=cells)
    nodes, cells = create_block((nw,nf), element, points=points, join=other)
#
    points  = {
            1: (  0.0  , d/2+h/2),
            2: (L/2-w/2, d/2+h/2),
            3: (L/2-w/2, d      ),
            4: (  0.0  , d      ),
    }
    other = dict(nodes=nodes, cells=cells)
    nodes, cells = create_block((nw,nf), element, points=points, join=other)
#
    points  = {
            1: (  0.0  , d/2-h/2),
            2: (L/2-w/2, d/2-h/2),
            3: (L/2-w/2, d/2+h/2),
            4: (  0.0  , d/2+h/2),
    }
    other = dict(nodes=nodes, cells=cells)
    nodes, cells = create_block((nw,nh), element, points=points, join=other)
#
    points  = {
            1: (L/2-w/2, d/2+h/2),
            2: (L/2+w/2, d/2+h/2),
            3: (L/2+w/2, d      ),
            4: (L/2-w/2, d      ),
    }
    other = dict(nodes=nodes, cells=cells)
    nodes, cells = create_block((nb,nf), element, points=points, join=other)
# 
    points  = {
            1: (L/2-w/2,   0.0),
            2: (L/2+w/2,   0.0),
            3: (L/2+w/2, d/2-h/2),
            4: (L/2-w/2, d/2-h/2),
    }
    other = dict(nodes=nodes, cells=cells)
    nodes, cells = create_block((nb,nf), element, points=points, join=other)
#
    return nodes, cells

if __name__ == "__main__":

    nodes, cells = tube_section()
    nodes = np.vstack(list(nodes.values()))
    cells = np.vstack(list(cells.values())) - 1

    ex = ExtrudeHexahedron((nodes, cells))


    model = xara.Model(ndm=3, ndf=3)
    model.material("ElasticIsotropic", 1, 29e3, 0.23)
    model.pattern("Plain", 1, "Linear")

    n = 80
    for i in range(n):

        for tag, coords in ex.nodes():
            model.node(tag, tuple(coords))
            if i==0 and coords[-1] == 0:
                model.fix(tag, (1, 1, 1))
            elif i == n-1:
                model.load(tag, (0.01, -1, 0), pattern=1)

        for tag, cell in ex.cells():
            model.element("stdBrick", tag, tuple(cell), 1)

        ex.advance([0, 0, 1])


    model.integrator("LoadControl", 200)
    model.system("Umfpack")
    model.test("NormUnbalance", 1e-8, 2, 1)
    model.analysis("Static")
    model.analyze(1)
    print("Analysis complete")

    artist = veux.create_artist(model, ndf=3)
    artist.draw_outlines(state=model.nodeDisp)
    artist.draw_surfaces(state=model.nodeDisp, field=NodalStress(model, "szz"))
    artist.save("hexa.glb")
    veux.serve(artist)

