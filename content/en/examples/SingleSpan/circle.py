from single_span import single_span

import numpy as np
from scipy.linalg import block_diag
#import shps.rotor
import pandas as pd

def test_disp(elem):
    model = single_span(elem)
    model.fix(1, *[1]*6)
#   model.setNodeDisp(2, 1, -0.001, '-commit')
    model.pattern("Plain", 1, "Linear", load={2: [0, 1, 0, *[0]*3]})

    model.integrator("LoadControl", 0.01)

    model.analysis("Static")
    model.analyze(1)

    K = model.getTangent(k=1)
    # Round and print
    K = np.around(K, 2)
    print("Stiffness")
    print(pd.DataFrame(K))

    print(model.nodeDisp(2, 1))
