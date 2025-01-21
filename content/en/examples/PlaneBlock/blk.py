
import veux
from shps import plane
from shps.block import create_block, join, grid



if __name__ == "__main__":
    d = 15
    L = 100
    h = 5
    w = 10
# First block
    ne = 6,4
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

#
    artist = veux.create_artist((nodes, cells), canvas="gltf")
    artist.draw_nodes()
    artist.draw_surfaces()
    artist.draw_outlines()
    veux.serve(artist)

