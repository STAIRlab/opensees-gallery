import veux
import numpy as np
from xara.units.iks import kip, ksi, foot, inch
import xsection as xs
from xsection.analysis import SectionInteraction
from xsection.library import Circle, Equigon
from collections import defaultdict
import matplotlib.pyplot as plt
plt.style.use("veux-web")


def render(model, tag):
    for section in model["StructuralAnalysisModel"]["properties"]["sections"]:
        if int(section["name"]) == int(tag):
            break

    fibers = defaultdict(lambda : {"coords": [], "areas": []})
    for fiber in section["fibers"]:
        fibers[int(fiber["material"])]["coords"].append(fiber["coord"])
        fibers[int(fiber["material"])]["areas"].append(fiber["area"])

    fig, ax = plt.subplots()
    for i, fiber in enumerate(fibers):
        print(f"A_{fiber} = {sum(fibers[fiber]["areas"])}")
        ax.plot(*zip(*fibers[fiber]["coords"]), label=f"{fiber}", marker="o", markersize=2, linestyle="None")

    fig.legend()
    ax.axis("equal")
    plt.show()


if __name__ == "__main__":

    d = 11/8*inch
    ds = 4/8*inch # diameter of the shear spiral
    cover = (3 + 1/8)*inch
    core_radius = 5/2*foot - cover - ds - d/2
    nr = 12

    octagon  = Equigon(5*foot/2, z=0,
                      name="cover", divisions=8)

    interior = Equigon(core_radius, z=1,
                      name="core", divisions=nr)

    bar = Circle(d/2, z=2, mesh_scale=1/2, divisions=4, name="rebar")

    xr = [(5*foot/2) - cover - ds - d/2,   0]

    bar_list = bar.linspace(xr, xr, nr, endpoint=False, center=(0,0))

    shape = xs.CompositeSection([
                octagon,
                interior,
                *bar_list
            ])


    # print(shape.summary())

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    for patch in shape._patches[:2]:
        for outline in patch.interior():
            ax[0].plot(*zip(*outline))
    
        ax[1].plot(*zip(*patch.exterior()))
    
    ax[0].axis("equal")
    ax[1].axis("equal")
    plt.show()


    artist = veux.create_artist(shape.model) #veux.model.FiberModel(shape.create_fibers()))
    # artist.draw_samples()
    artist.draw_outlines()
    artist.draw_surfaces()
    veux.serve(artist)


    mat = [
        { # Confined
            "name": "core",
            "type": "Concrete01",
            "Fc":   6*ksi,
            "ec0":  0.004,
            "Fcu":  5*ksi,
            "ecu":  0.014,
        },
        { # Unconfined
            "name": "cover",
            "type": "Concrete01",
            "Fc":  -5*ksi,
            "ec0": -0.002,
            "Fcu":  0,
            "ecu": -0.006,
        },
        {
            "name": "rebar",
            "type": "Steel01",
            "E":   30e3*ksi,
            "Fy":    60*ksi,
            "b":   0.01
        }
    ]

    axial = np.linspace(-1200*kip, 250*kip, 15)

    si = SectionInteraction(("Fiber", shape, mat), axial=axial)
    # si.surface2(nstep=100, incr=1e-4)

    render(si.create_model().asdict(), 1)



    fig, ax = plt.subplots(1,2, sharey=True, constrained_layout=True)
    mmax = []

    for n, m, k in si.moment_curvature():

        ax[0].plot(k, m, '.-', lw=0.2, markersize=0.5)

        ax[1].plot([n]*len(m), m, '.-', lw=0.2, markersize=0.5)
        ax[1].plot([n], [m[-1]], 'o')

    ax[0].axvline(0, color="k", lw=1)
    ax[0].axhline(0, color="k", lw=1)
    ax[1].axvline(0, color="k", lw=1)
    ax[1].axhline(0, color="k", lw=1)
    ax[0].set_xlabel("Curvature, $\\kappa$")
    ax[0].set_ylabel("Moment, $M(\\varepsilon, \\kappa)$")
    ax[1].set_xlabel("Axial force, $P$")
    plt.show()
