from opensees.helpers import Prism
import numpy as np

if __name__ == "__main__":

    scale = 1
    steps = 1
    ne = 5
    E  = 1.0
    I  = 2.0
    prism = Prism(
        length = 1.0,
        element = "ExactFrame",
        section = dict(
            E   = E,
            G   = 1.0,
            A   = 2.0,
            J   = 2.0,
            Iy  = I,
            Iz  = I,
            Ay  = 2.0,
            Az  = 2.0),
        boundary = ("fix","free"),
        transform = "Linear",
        divisions = ne
    )

    model = prism.create_model()

    model.test("EnergyIncr", 1e-12, 10, 1)

    model.pattern("Plain", 1, "Linear", load={
        ne+1: [0, 0, 0] + [0, 0, -scale*E*I/prism.length*2*np.pi]}
    )

    model.integrator("LoadControl", scale/steps)
    model.analysis("Static")

    import veux
    artist = veux.create_artist(model)
    artist.draw_axes()
    artist.draw_outlines()

    for i in range(steps):
        if model.analyze(1) != 0:
            raise RuntimeError(f"Failed at step {i}")

        artist.draw_outlines(state=model.nodeDisp)

    veux.serve(artist)


