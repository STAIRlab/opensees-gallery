import sys
import veux
from steel import wide_flange

import numpy as np

import opensees.openseespy as ops

import numpy as np
import pandas as pd

import opensees.units.iks as units
pi   = units.pi
ft   = units.ft
ksi  = units.ksi
inch = units.inch


def isotropic_section(model, tag, material, properties, type):

    # Define material
    E = material["E"]
    nu = material["nu"]
    mat_tag = 1      # identifier that will be assigned to the new material

    model.material("ElasticIsotropic", mat_tag, E, nu, 0.0)

    width = 15.0
    depth = 24.0

    model.section(type, tag, GJ=1e6)
    mesh = wide_flange(t=2.0, b=width, d=depth)
    print(mesh.summary())
    for fiber in mesh.fibers():
        y, z = fiber.location
        model.fiber(y, z, fiber.area, mat_tag, fiber.warp[0], fiber.warp[1], section=tag)

    return mesh


def test_isotropic(section):
    # Material
    material = dict(
        E    = 1, #29000*ksi,
        nu   = -0.5
    )
    model = ops.Model(ndm=3, ndf=6)

    mesh = isotropic_section(model, 1, material, {}, section)


    tangent = model.invoke("section", 1, [
                           "update  0 0 0 0 0 0;",
                           "tangent"
            ])

    n = int(np.sqrt(len(tangent)))
    print(pd.DataFrame(np.round(np.array(tangent), 4).reshape(n,n)))

    # Render
    d = 24.0
    artist = veux.create_artist((mesh.model.nodes, mesh.model.cells()), ndf=1)

    field = mesh.torsion.warping()
    artist.draw_surfaces(field = field, state=field, scale=1/100)
    R = artist._plot_rotation

    artist.canvas.plot_vectors([R@[*mesh.torsion.centroid(), 0] for i in range(3)], d/5*R.T)
    artist.canvas.plot_vectors([R@[*mesh.torsion.shear_center(), 0] for i in range(3)], d/5*R.T)

    veux.serve(artist)

if __name__ == "__main__":
    test_isotropic("ShearFiber")
#   test_isotropic("AxialFiber")

