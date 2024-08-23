import numpy as np
import opensees.openseespy as ops

def space_truss(ns, Ro, Ri, H):
    """Generate a 3D truss"""

    model = ops.Model(3,3)
    m1 = model.material('default', 1.0)
    s1 = model.xsection('default', 1.0, 1.0)

    # Specify node coordinates for support points
    # angle for supports
    phi = np.arange(ns)/ns*2*np.pi

    # Coordinates for support points
    X  = np.cos(phi)*Ro
    Y  = np.sin(phi)*Ro
    # Generate support points with height Z of 0
    for i in range(ns):
        model.node(i+1, X[i], Y[i], 0.0)

    # Angles for upper ring (offset by pi/ns degrees from supports)
    phi = phi+np.pi/ns

    # Coordinates for upper ring
    X   = np.append(X, np.cos(phi)*Ri)
    Y   = np.append(Y, np.sin(phi)*Ri)

    # Generate coordinates for upper ring with height H
    for i in np.arange(ns, 2*ns):
        model.node(i+1, X[i], Y[i], H)

    for i, j, k in zip(np.arange(ns), np.arange(0, ns), np.arange(ns, 2*ns)):
        model.element("Truss", i+1, j, k, m1, s1)

    model.element("Truss", alpha[ns+1], 0, 2*ns-1, m1, s1)

    for i, j, k in zip(np.arange(ns+1, 2*ns), np.arange(1, ns), np.arange(ns, 2*ns-1)):
        model.element("Truss", i+1, j, k, m1, s1)

    for i, j, k in zip(np.arange(2*ns, 3*ns-1), np.arange(ns, 2*ns-1), np.arange(ns+1, 2*ns)):
        model.element("Truss", i+1, j, k, m1, s1)

    model.element("Truss", 3*ns, ns, 2*ns-1, m1, s1)


    # boundary conditions
    for node in range(ns):
        model.fix(node, (1, 1, 1))


    return model
