
import xara
import veux
from shps.frame.extrude import ExtrudeTetrahedron
from xsection.library import Channel


if __name__ == "__main__":

    shape = Channel(d=16, b=8, tf=1.0, tw=1.0, mesh_scale=0.5, #0.75
                    mesher="gmsh")

#   veux.serve(veux.render(shape.model, hide={"node.marker"}))


    ex = ExtrudeTetrahedron(shape.model)


    model = xara.Model(ndm=3, ndf=3)

    model.material("ElasticIsotropic", 1, 29e3, 0.23)

    model.pattern("Plain", 1, "Linear")

    n = 200
    for i in range(n):

        for tag, coords in ex.nodes():
            # Create the node
            model.node(tag, tuple(coords))

            # if we're at the root, fix this node
            if i==0 and coords[-1] == 0:
                model.fix(tag, (1, 1, 1))
            elif i == n-1:
                model.load(tag, (0, -1, 0), pattern=1)

        for tag, cell in ex.cells():
            model.element("FourNodeTetrahedron", tag, tuple(cell), 1)

        ex.advance()

    model.integrator("LoadControl", 2)
    model.system("Umfpack")
    model.analysis("Static")
    model.analyze(1)
    print("Analysis complete")

    artist = veux.create_artist(model, ndf=3)
    artist.draw_outlines(state=model.nodeDisp)
    artist.draw_surfaces(state=model.nodeDisp)
    veux.serve(artist)

