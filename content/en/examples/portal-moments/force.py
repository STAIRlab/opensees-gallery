import sys
import xara
import veux
from utilities import MatrixAnalysis, create_field


def create_plane(vertical):
    model = xara.Model(ndm=3, ndf=6)
    element = "ForceFrame"
    section = 1

    if vertical == 2:
        model.node(1, (    0,     0,  0))
        model.node(2, (    0,   8.0,  0))
        model.node(3, ( 10.0,   8.0,  0))
        model.node(4, ( 20.0,   8.0,  0))
        model.node(5, ( 20.0,  -2.0,  0))

        model.geomTransf("Linear", 1, (0, 0, 1))

        model.fix(1, (1,1,1,  1,1,0))
        model.fix(5, (1,1,1,  1,1,1))
    else:
        model.node(1, (    0,  0,    0))
        model.node(2, (    0,  0,  8.0))
        model.node(3, ( 10.0,  0,  8.0))
        model.node(4, ( 20.0,  0,  8.0))
        model.node(5, ( 20.0,  0, -2.0))

        model.geomTransf("Linear", 1, (0,-1, 0))

        model.fix(1, (1,1,1,  1,0,1))
        model.fix(5, (1,1,1,  1,1,1))

    model.section("ElasticFrame", 1, E=1e3, A=1e3, Iz=60, Iy=1e2, G=1e2, J=1e3)


    # Connectivity
    n = 10 # number of integration points
    model.element(element, 1, (1, 2), n, 1, 1, shear=0) #section=section, transform=1, shear=0)
    model.element(element, 2, (2, 3), n, 1, 1, shear=0)
    model.element(element, 3, (3, 4), n, 1, 1, shear=0)
    model.element(element, 4, (4, 5), n, 1, 1, shear=0)


    model.pattern("Plain", 1, "Constant")
    model.eleLoad("-type", "BeamUniform",  5, 1, ele=1, pattern=1)
    model.eleLoad("-type", "BeamUniform", 10, 0, ele=2, pattern=1)


    model.analysis("Static")
    model.analyze(1)
    return model

if __name__ == "__main__":
    vertical = 3
    model = create_plane(vertical)

    artist = veux.create_artist(model, vertical=vertical)
#   artist.draw_outlines()
    artist.draw_sections()
    artist.draw_diagrams(field=create_field(model, artist), scale=1/30)
    artist.draw_axes(extrude=True)
    artist.draw_nodes()

    # Check the number of arguments that were passed when this
    # script was invoked on the command line.
    if len(sys.argv) > 1:
        print(f"Saving to {sys.argv[1]}")
        artist.save(sys.argv[1])
    else:
        veux.serve(artist)

