from shps import plane
from shps.block import create_block, join, grid
import veux
import sys,pprint

def plot(nodes, cells):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    for cell in cells.values():
        ax.plot(*zip(*[nodes[i] for i in cell], nodes[cell[0]]))
    return ax


if __name__ == "__main__":


    ne = int(sys.argv[1]), int(sys.argv[2])
    if len(sys.argv) > 3:
        nn = int(sys.argv[3]), int(sys.argv[4])

    else:
        nn = 2,2

    # nodes, cells = grid(ne, nn)


# First block
    element = plane.Lagrange(4)
    points  = {
            1: (0.0, 0.0),
            2: (1.1, 0.0),
            3: (1.0, 1.0),
            4: (0.0, 1.0),
            5: (0.5,-0.1),
            6: (1.1, 0.5)
    }

    nodes, cells = create_block(ne, element, points=points)

# Second Block
    element = plane.Serendipity(4)

    points  = {
            1: (1.1, 0.0),
            2: (2.0, 0.0),
            3: (2.0, 1.0),
            4: (1.0, 1.0),
            5: (1.5,-0.1),
#           7: (2.1, 0.5),
            8: (1.1, 0.5)
    }

    other = dict(nodes=nodes, cells=cells)
    nodes, cells = create_block(ne, element, points=points, join=other)

    artist = veux.create_artist((nodes, cells), canvas="plotly")
    artist.draw_nodes()
    artist.draw_surfaces()
    veux.serve(artist)



    from shps.plotting import Rendering
    ax = plot(nodes, cells)
    ax.axis("equal")

    ax = None
    Rendering(ax=ax).draw_nodes(nodes).show()

    first = grid((3,2), (2,3))

    nodes, cells = join(first, grid((3,2), corners=((1, 2),(-1,1))))
    ax = plot(nodes, cells)
    ax.axis("equal")


