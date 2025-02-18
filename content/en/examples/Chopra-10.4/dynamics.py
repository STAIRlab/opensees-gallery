import numpy as np
from math import cos,sin,sqrt,pi
import opensees.openseespy as ops
from opensees.units.iks import gravity

def create_model():
    # Eigen analysis of a two-storey one-bay frame
    # Example 10.5 from "Dynamics of Structures" by Anil Chopra
    # units: kips, in, sec
    # Vesna Terzic, 2010

    # mass
    m =  100.0/gravity

    #material
    A =    63.41
    I =   320.0
    E = 29000.0

    #geometry
    h = 1 #20.
    L = 2*h

    # define the model
    #---------------------------------
    # model builder
    model = ops.Model(ndm=2,  ndf=3)

    # nodal coordinates:
    model.node(1, 0.,  0.)
    model.node(2, L ,  0.)
    model.node(3, 0.,  h )
    model.node(4, L ,  h )
    model.node(5, 0., 2*h)
    model.node(6, L , 2*h)

    # Single point constraints -- Boundary Conditions
    model.fix(1, 1, 1, 1)
    model.fix(2, 1, 1, 1)

    # assign mass
    model.mass(3,  m,   0., 0.)
    model.mass(4,  m,   0., 0.)
    model.mass(5, m/2., 0., 0.)
    model.mass(6, m/2., 0., 0.)

    # define a geometric transformation
    transform = 1
    model.geomTransf('Linear', transform )

    # define elements:
    # columns
    model.element('ElasticBeamColumn', 1, (1, 3), A, E,  2.*I, transform)
    model.element('ElasticBeamColumn', 2, (3, 5), A, E,     I, transform)
    model.element('ElasticBeamColumn', 3, (2, 4), A, E,  2.*I, transform)
    model.element('ElasticBeamColumn', 4, (4, 6), A, E,     I, transform)
    # beams
    model.element('ElasticBeamColumn', 5, (3, 4), A, E,  2.*I, transform)
    model.element('ElasticBeamColumn', 6, (5, 6), A, E,     I, transform)

    return model

def find_mass(model, ndf=3, tol=0.0):
    return [
        model.nodeDOFs(nd)[j]
        for nd in model.getNodeTags()
            for j in range(ndf)  # NDF is number of DOFs/node
                if abs(model.nodeMass(nd,j+1)) > tol
        ]

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
        Kc = Kmm - Kmn@np.linalg.solve(Knn,Knm)
    else:
        Kc = K

    return Kc


def state_space(M, C, K, im=None, model=None):
    #   https://portwooddigital.com/2020/05/17/gimme-all-your-damping-all-your-mass-and-stiffness-too/

    # Determine number of DOFs with mass
    if im is None:
        im = find_mass(model)

    nm = len(im)

    # Form matrices for D*x = -lam*B*x
    B = np.zeros((2*nm,2*nm)) # = [ 0 M; M C]
    D = np.zeros((2*nm,2*nm)) # = [-M 0; 0 K]

    # Mass
    B[:nm,:][:,nm:2*nm] =  M[im,:][:,im]
    B[nm:2*nm,:][:,:nm] =  M[im,:][:,im]
    D[:nm,:][:,:nm]     = -M[im,:][:,im]

    # Damping
    B[nm:2*nm,:][:,nm:2*nm] = C[im,:][:,im]

    # Stiffness at DOFs with mass

    Kc = condense(K, ic=im)
    D[nm:2*nm,:][:,nm:2*nm] = Kc



def eigen_analysis(model):

    # record eigenvectors
    #----------------------
    for k in range(1, numModes+1):
        model.recorder("Node", f"eigen {k}", file=f"modes/mode{k}.out", 
                       nodeRange=[1, 6], dof=[1, 2, 3]
        )

    # number of modes
    numModes = 2

    # perform eigen analysis
    #-----------------------------
    lamda = model.eigen(numModes)

    # calculate frequencies and periods of the structure
    #---------------------------------------------------
    omega = []
    f = []
    T = []
    pi = 3.141593

    for lam in lamda:
        omega.append(sqrt(lam))
        f.append( sqrt(lam)/(2*pi) )
        T.append( (2*pi)/sqrt(lam) )


    print(f"The periods are {T}")


def static_analysis(model):
    # Run a one step gravity load with no loading (to record eigenvectors)
    #-----------------------------------------------------------------------
    model.integrator('LoadControl', 0, 1, 0, 0)
    
    # Convergence test
    #                     tolerance maxIter displayCode
    model.test('EnergyIncr', 1.0e-10, 100, 0)
    
    # Solution algorithm
    model.algorithm('Newton')
    
    # DOF numberer
    model.numberer('RCM')
    
    # Constraint handler
    model.constraints('Transformation')
    
    
    # System of equations solver
    model.system('ProfileSPD')
    
    model.analysis('Static')
    res = model.analyze(1)
    if res < 0 :
        print("Modal analysis failed")
    
    
    # get values of eigenvectors for translational DOFs
    #---------------------------------------------------
    f11 = model.nodeEigenvector(3, 1, 1)
    f21 = model.nodeEigenvector(5, 1, 1)
    f12 = model.nodeEigenvector(3, 2, 1)
    f22 = model.nodeEigenvector(5, 2, 1)
    
    print(f"eigenvector 1: [{f11/f21},       {f21/f21} ]")
    print(f"eigenvector 2: [{f12/f22},       {f22/f22} ]")
    
