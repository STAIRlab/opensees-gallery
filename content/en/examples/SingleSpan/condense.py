import numpy as np 
import opensees.openseespy as ops 

def condense(K, ic=None, model=None, tol=0.0):
    N = K.shape[0]


    ic = np.array(ic)

    if len(ic.shape) > 1:
        ic = np.array([model.nodeDOF(*i) for i in ic], dtype=int)


    ix = np.setdiff1d(range(N), ic)

    # Static condensation
    Kmm = K[ic,:][:,ic]
    Kmn = K[ic,:][:,ix]
    Knm = K[ix,:][:,ic]
    Knn = K[ix,:][:,ix]

    # Kc = Kmm - Kmn*inv(Knn)*Knm
    if len(ix) > 0:
#       Kc = Kmm - np.dot(Kmn,np.linalg.solve(Knn,Knm))
        Kc = Kmm - Kmn@np.linalg.solve(Knn,Knm)
    else:
        Kc = K

    return Kc


def cantilever(L, E, A, Iz, Iy, G=0, J=1):
    # Create a model
    model = ops.Model(ndm=3, ndf=6)


    # Define nodes
    model.node(1,  (0.0, 0.0, 0.0))
    model.node(2,  (L/2, 0.0, 0.0))
    model.node(2,  ( L , 0.0, 0.0))


    trn = 1
    model.geomTransf("Linear", 1, (0, 0, 1))


    sec = 1
    model.section("ElasticFrame", sec, E, A, Iz, Iy, G, J, mass=2, Ay=100, Az=100)

    model.element("PrismFrame", 1, (1, 2), transform=trn, section=sec, cMass=True)
    model.element("PrismFrame", 1, (2, 3), transform=trn, section=sec, cMass=True)

    model.analysis("Static")

    return model



if __name__ == "__main__":
    model = cantilever()
    K = model.getTangent(k=1)