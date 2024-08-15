from single_span import single_span

import numpy as np
from scipy.linalg import block_diag
#import shps.rotor
import pandas as pd

def test_elem(elem):
    model = single_span(elem)

    model.analysis("Transient")
    model.integrator("Newmark", 1/2, 1/4)
    model.analyze(1, 0.01)

    print(elem)

    if False:
        for i in range(500):
            model.analyze(1)
            model.getTangent(k=1)



    K = model.getTangent(k=1)

    # Transform to global coordinates
    R = np.eye(3) #shps.rotor.exp((0.1, 0.2, 0))
    T = block_diag(*[R]*4)
    K = T.T@K@T

    # Round and print
    K = np.around(K, 2)
    print("Stiffness")
    print(pd.DataFrame(K))

#   K = model.getTangent(m=1)
#   K = np.around(T.T@K@T, 2)
#   print("Mass")
#   print(pd.DataFrame(K))


# test("elasticBeamColumn")
# test("ElasticBeamColumn")
# test("elasticBeamColumn", True)
#test("ElasticBeamColumn", True)

#test("CubicFrame", True)
#test("forceBeamColumn", True)
#test("ForceFrame", True)
import sys
test_elem(sys.argv[1])

