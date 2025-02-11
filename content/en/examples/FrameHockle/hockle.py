from opensees.helpers import Prism
from shps.rotor import exp
import numpy as np

if __name__ == "__main__":

    scale = 5.0 #0.0
    steps = 65
    ne = 40
    E  = 71_240
    G  = 27_190
    I  = 0.0833
    A  = 10.0
    prism = Prism(
        length = 240.,
        element = "ExactFrame",
        section = dict(
            E   = E,
            G   = G,
            A   = A,
            J   = 2.16,
            Iy  = I,
            Iz  = I,
            Ay  = A,
            Az  = A),
        boundary = ((1,1,1, 1,1,1),
                    (0,1,1, 0,1,1)),
        transform = "Linear",
        divisions = ne,
        rotation = exp([0,  0.000, 0.005])
    )

    model = prism.create_model()
#   model.fix(ne+1, (0, 1, 1, 0, 1, 1))

    model.test("EnergyIncr", 1e-8, 50, 1)
#   model.test("NormDispIncr", 1e-8, 50, 1)
#   model.test("RelativeNormDispIncr", 1e-6, 50, 1)

    f = [0, 0, 0] + list(map(float, prism.rotation@[scale/steps*2*E*I/prism.length, 0, 0]))
    model.pattern("Plain", 1, "Linear", load={
        ne+1: f
    })

    model.integrator("MinUnbalDispNorm", 1.0) #scale/steps)
    model.analysis("Static")

    import veux
    artist = veux.create_artist(model)
    artist.draw_axes()
    artist.draw_outlines()

    u = []
    lam = []

    for i in range(steps):
        if model.analyze(1) != 0:
            break
            raise RuntimeError(f"Failed at step {i}")
        u.append(-model.nodeDisp(ne+1, 4))
        lam.append(model.getTime())

#       artist.draw_outlines(state=model.nodeDisp)
    import matplotlib.pyplot as plt
    plt.plot(u, lam)
    plt.show()

#   veux.serve(artist)


