import sys

import numpy as np

import opensees.openseespy as ops
from opensees.units.iks import ft, ksi

import numpy as np
from scipy.linalg import block_diag
import pandas as pd

from fibers import isotropic_section

def create_prism(element,
                 section:   str = "ShearFiber",
#                transform: str
                 ):

    model = ops.Model(ndm=3, ndf=6)

    # Length of cantilever column
    L = 8*ft
    # specify node coordinates
    model.node(1,   0 , 0,  0);  # first node
    model.node(2,   L , 0,  0);  # second node

    # specify mass
    model.mass(2, 2.0, 2.0, 2.0, 0.0, 0.0, 0.0)


    # Material
    material = dict(
        E    = 1, #29000*ksi,
        nu   = 0.2  #-0.5
    )

    #
    properties = dict(
    )
    sec_tag = 1
    isotropic_section(model, sec_tag, material, properties, section)

    # Create element geometric transformation
    model.geomTransf("Linear", 1, (0, 0, 1))

    # Finally, create the element
    model.element(element, 1, (1, 2),  transform=1, section=1)

    # boundary conditions
#   model.fix(1, 1, 1, 1 , 1, 1, 1)

   #                                                  Force     |  Moment
    model.pattern("Plain", 1, "Linear", load={2: [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]})

    return model




def test_stif(elem):
    model = create_prism(elem)

    model.analysis("Transient")
#   model.integrator("Newmark", 1/2, 1/4)
#   model.analyze(1, 0.01)


    tangent = model.invoke("section", 1, [
                           "update  0 0 0 0 0 0;",
                           "tangent"
            ])

    n = int(np.sqrt(len(tangent)))
    print(pd.DataFrame(np.round(np.array(tangent), 4).reshape(n,n)))



    K = model.getTangent(k=1)

    K = np.round(K, 4)

    print(pd.DataFrame(K))


# test("elasticBeamColumn")
# test("ElasticBeamColumn")
# test("elasticBeamColumn", True)
#test("ElasticBeamColumn", True)

#test("CubicFrame", True)
#test("forceBeamColumn", True)
#test("ForceFrame", True)

if __name__ == "__main__":
    test_stif("ExactFrame")



#analyze(cantilever(sys.argv[1]))
