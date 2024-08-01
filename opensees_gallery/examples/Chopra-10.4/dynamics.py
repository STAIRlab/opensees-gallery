import numpy as np
from math import cos,sin,sqrt,pi
import opensees.openseespy as ops
from opensees.units.iks import gravity

# set input variables
#--------------------
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

    # define geometric transformation:
    TransfTag = 1
    model.geomTransf('Linear', TransfTag )

    # define elements:
    # columns
    model.element('ElasticBeamColumn', 1, 1, 3, A, E,  2.*I, TransfTag)
    model.element('ElasticBeamColumn', 2, 3, 5, A, E,     I, TransfTag)
    model.element('ElasticBeamColumn', 3, 2, 4, A, E,  2.*I, TransfTag)
    model.element('ElasticBeamColumn', 4, 4, 6, A, E,     I, TransfTag)
    # beams
    model.element('ElasticBeamColumn', 5, 3, 4, A, E,  2.*I, TransfTag)
    model.element('ElasticBeamColumn', 6, 5, 6, A, E,     I, TransfTag)

    return model

def find_mass(model, ndf=3, tol=0.0):
    return [
        model.nodeDOFs(nd)[j]
        for nd in model.getNodeTags()
            for j in range(ndf)  # NDF is number of DOFs/node
                if abs(model.nodeMass(nd,j+1)) > tol
        ]

def static_condensation(M, K, mass_dofs=None, model=None, tol=0.0):
    # DOFs without mass
    ndf = 3
#   N = model.systemSize()
    N = K.shape[0]

    if mass_dofs is None:
        assert model is not None
        mass_dofs = find_mass(model, tol=tol)
    else:
        mass_dofs = np.array(mass_dofs)

    if len(mass_dofs.shape) > 1:
        mass_dofs = np.array([model.nodeDOF(*i) for i in mass_dofs], dtype=int)


    masslessDOFs = np.setdiff1d(range(N), mass_dofs)

    # Static condensation
    Kmm = K[mass_dofs,:][:,mass_dofs]
    Kmn = K[mass_dofs,:][:,masslessDOFs]
    Knm = K[masslessDOFs,:][:,mass_dofs]
    Knn = K[masslessDOFs,:][:,masslessDOFs]

    # Kc = Kmm - Kmn*inv(Knn)*Knm
    if len(masslessDOFs) > 0:
#       Kc = Kmm - np.dot(Kmn,np.linalg.solve(Knn,Knm))
        Kc = Kmm - Kmn@np.linalg.solve(Knn,Knm)
    else:
        Kc = K

    return M[mass_dofs,:][:,mass_dofs], Kc

def state_space(M, C, K, mass_dofs):
    #   https://portwooddigital.com/2020/05/17/gimme-all-your-damping-all-your-mass-and-stiffness-too/
    # Determine number of DOFs with mass

    N = K.shape[0]
    masslessDOFs = np.setdiff1d(range(N), mass_dofs)

    # Number of DOFs with mass
    nm     = len(mass_dofs)

    # Form matrices for D*x = -lam*B*x
    B = np.zeros((2*nm,2*nm)) # = [ 0 M; M C]
    D = np.zeros((2*nm,2*nm)) # = [-M 0; 0 K]

    # Mass
    B[:nm,:][:,nm:2*nm] =  M[mass_dofs,:][:,mass_dofs]
    B[nm:2*nm,:][:,:nm] =  M[mass_dofs,:][:,mass_dofs]
    D[:nm,:][:,:nm]     = -M[mass_dofs,:][:,mass_dofs]

    # Damping
    B[nm:2*nm,:][:,nm:2*nm] = C[mass_dofs,:][:,mass_dofs]

    # Stiffness at DOFs with mass
    Mc, Kc = static_condensation(M, K, mass_dofs=mass_dofs)
    D[nm:2*nm,:][:,nm:2*nm] = Kc

    # State space eigenvalue analysis
    lam, x = slin.eig(D,-B)



def eigen_analysis():

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


def static_analysis():
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
    
