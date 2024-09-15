import numpy as np
import scipy.linalg


# Function to define h matrix
def hMatrix(x, Np):
    h = np.zeros((Np, Np))
    for j in range(Np):
        for i in range(Np):
            h[i, j] = (x[i]**(j + 2) - x[i]) / ((j + 1) * (j + 2))
    return h


# Function to define g (Vandermonde) matrix
def gMatrix(x, Np):
    g = np.zeros((Np, Np))
    for j in range(Np):
        for i in range(Np):
            g[i, j] = x[i]**j
    return g


# Function for buckling analysis by curvature-based displacement interpolation
# returns only the first buckling mode
def PcrCBDI(x, EI, L):
    Np = len(x)

    # h matrix
    h = np.zeros((Np, Np))
    for j in range(Np):
        for i in range(Np):
            h[i, j] = (x[i]**(j + 2) - x[i]) / ((j + 1) * (j + 2))

    # g matrix
    g = np.zeros((Np, Np))
    for j in range(Np):
        for i in range(Np):
            g[i, j] = x[i]**j

    lstar = np.dot(h, np.linalg.inv(g))

    F = np.zeros((Np, Np))
    for i in range(Np):
        F[i, i] = 1 / EI[i]

    [v, d] = np.linalg.eig(np.dot(-(L**2) * lstar, F))

    return min(1 / v)


def element_tangent(EI, L):
    """
    cmp
    """
    pass


### Function for buckling analysis by matrix structural analysis
# returns only the first buckling mode
def PcrMatrix(EI, L):
    N = len(EI)
    if N <= 1:
        raise Exception("This function requires 2 or more segments")
    Ke = np.zeros((2 * N, 2 * N))
    Kg = np.zeros((2 * N, 2 * N))
    for i in range(N):
        ke = EI[i] * np.array(
            [
                [ 12 / L[i]**3,  6 / L[i]**2, -12 / L[i]**3, 6 / L[i]**2],
                [  6 / L[i]**2,  4 / L[i],     -6 / L[i]**2, 2 / L[i]],
                [-12 / L[i]**3, -6 / L[i]**2,  12 / L[i]**3, -6 / L[i]**2],
                [  6 / L[i]**2,  2 / L[i],     -6 / L[i]**2, 4 / L[i]],
            ]
        )
        kg = np.array(
            [
                [ 1.2 / L[i], 0.1, -1.2 / L[i], 0.1],
                [ 0.1, 2 * L[i] / 15, -0.1, -L[i] / 30],
                [-1.2 / L[i], -0.1, 1.2 / L[i], -0.1],
                [ 0.1, -L[i] / 30, -0.1, 2 * L[i] / 15],
            ]
        )

        if i == 0:
            connectivity = {1: 0, 2: 1, 3: 2}
        elif i == (N - 1):
            connectivity = {0: (2 * N - 3), 1: (2 * N - 2), 3: (2 * N - 1)}
        else:
            connectivity = {0: (2 * i - 1), 1: (2 * i), 2: (2 * i + 1), 3: (2 * i + 2)}

        for ikey in connectivity:
            for jkey in connectivity:
                Ke[connectivity[ikey], connectivity[jkey]] += ke[ikey, jkey]
                Kg[connectivity[ikey], connectivity[jkey]] += kg[ikey, jkey]
    a = scipy.linalg.eigh(Ke, Kg, eigvals_only=True)

    return min(a)

