import sees
import numpy as np
import opensees.openseespy as ops

def space_truss(ns, Ro, Ri, H):
    """Generate a 3D truss"""

    model = ops.Model(ndm=3,ndf=3)
    A = 1.0

    m1 = 1
    model.uniaxialMaterial("Elastic", m1, 3000.0)

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
    for i in range(ns, 2*ns):
        model.node(i+1, X[i], Y[i], H)

    for i, j, k in zip(range(ns), range(1, ns), range(ns, 2*ns)):
        model.element("Truss", i+1, j, k, A, m1)

#   model.element("Truss", ns+1, 0, 2*ns-1, A, m1)

    for i, j, k in zip(range(ns+1, 2*ns), range(1, ns), range(ns, 2*ns-1)):
        model.element("Truss", i+1, j, k, A, m1)

    for i, j, k in zip(range(2*ns, 3*ns-1), range(ns, 2*ns-1), range(ns+1, 2*ns)):
        model.element("Truss", i+1, j, k, A, m1)

    model.element("Truss", 3*ns, ns, 2*ns-1, A, m1)


    # boundary conditions
    for node in range(ns):
        model.fix(node+1, (1, 1, 1))


    return model

if __name__ == "__main__":
    sees.serve(sees.render(space_truss(5, 10, 20, 15), canvas="gltf"))

