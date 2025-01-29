import sys
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
        model.fiber(y, z, fiber.area, mat_tag, fiber.warp[0], section=tag)


def test_isotropic(section):
    # Material
    material = dict(
        E    = 1, #29000*ksi,
        nu   = -0.5
    )
    model = ops.Model(ndm=3, ndf=6)

    isotropic_section(model, 1, material, {}, section)

    tangent = model.invoke("section", 1, [
                           "update  0 0 0 0 0 0;",
                           "tangent"
            ])

    n = int(np.sqrt(len(tangent)))
    print(pd.DataFrame(np.round(np.array(tangent), 4).reshape(n,n)))


if __name__ == "__main__":
    test_isotropic("ShearFiber")
#   test_isotropic("AxialFiber")

