import  sys
import xara
import veux
from xara.post import FrameMoments


def create_plane():
    model = xara.Model(ndm=2)
    element = "PrismFrame"
    transform = 1
    section   = 1

    model.node(1, ( 0,  0))
    model.node(2, ( 0,  8))
    model.node(3, (10,  8))
    model.node(4, (20,  8))
    model.node(5, (20, -2))

    model.fix(1, (1, 1, 0))
    model.fix(5, (1, 1, 1))

    model.geomTransf("Linear", 1)
    model.section("Elastic", 1, E=1e3, A=1e6, I=60)


    # Connectivity
    model.element(element, 1, (1, 2), section=section, transform=transform)
    model.element(element, 2, (2, 3), section=section, transform=transform)
    model.element(element, 3, (3, 4), section=section, transform=transform)
    model.element(element, 4, (4, 5), section=section, transform=transform)

    model.pattern("Plain", 1, "Constant")
    model.eleLoad("-type", "BeamUniform",  5, ele=1, pattern=1)
    model.eleLoad("-type", "BeamUniform", 10, ele=2, pattern=1)

    model.analysis("Static")
    model.analyze(1)
    return model


if __name__ == "__main__":

    model = create_plane()

    artist = veux.create_artist(model, vertical=2)
    artist.draw_outlines()
    artist.draw_diagrams(field=FrameMoments(model, artist), scale=1/30)
    artist.draw_axes(extrude=True)
    artist.draw_nodes()

    # Check the number of arguments that were passed when this
    # script was invoked on the command line.
    if len(sys.argv) > 1:
        print(f"Saving to {sys.argv[1]}")
        artist.save(sys.argv[1])
    else:
        veux.serve(artist)

