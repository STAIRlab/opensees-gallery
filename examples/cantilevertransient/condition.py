# Linear algebra library
import numpy as np


# import the openseespy interface which contains the "Model" class
import opensees.openseespy as ops
import opensees.section
import quakeio


## Configure units
# Units are based on inch-kip-seconds
import opensees.units.iks as units
pi   = units.pi;
ft   = units.ft;
ksi  = units.ksi;
inch = units.inch;


def state_space(M, C, K, model):
    #   https://portwooddigital.com/2020/05/17/gimme-all-your-damping-all-your-mass-and-stiffness-too/
    # Determine number of DOFs with mass
    NDF = ...

    massDOFs = []
    for nd in model.getNodeTags():
        for j in range(NDF): # NDF is number of DOFs/node
            if ops.nodeMass(nd,j+1) > 0.0:
                massDOFs.append(ops.nodeDOFs(nd)[j])

    # Number of DOFs with mass
    Nmass = len(massDOFs)

    # DOFs without mass
    masslessDOFs = np.setdiff1d(range(N), massDOFs)
    Nmassless = len(masslessDOFs)

    # Form matrices for D*x = -lam*B*x
    B = np.zeros((2*Nmass,2*Nmass)) # = [ 0 M; M C]
    D = np.zeros((2*Nmass,2*Nmass)) # = [-M 0; 0 K]

    # Mass
    B[:Nmass,:][:,Nmass:2*Nmass] =  M[massDOFs,:][:,massDOFs]
    B[Nmass:2*Nmass,:][:,:Nmass] =  M[massDOFs,:][:,massDOFs]
    D[:Nmass,:][:,:Nmass]        = -M[massDOFs,:][:,massDOFs]

    # Damping
    B[Nmass:2*Nmass,:][:,Nmass:2*Nmass] = C[massDOFs,:][:,massDOFs]

    # Static condensation
    Kmm = K[massDOFs,:][:,massDOFs];     Kmn = K[massDOFs,:][:,masslessDOFs]
    Knm = K[masslessDOFs,:][:,massDOFs]; Knn = K[masslessDOFs,:][:,masslessDOFs]

    # Kc = Kmm - Kmn*inv(Knn)*Knm
    if Nmassless > 0:
        Kc = Kmm - np.dot(Kmn,np.linalg.solve(Knn,Knm))
    else:
        Kc = K

    # Stiffness at DOFs with mass
    D[Nmass:2*Nmass,:][:,Nmass:2*Nmass] = Kc

    # State space eigenvalue analysis
    lam, x = slin.eig(D,-B)


def steel_cantilever(small_mass = 1e-4, hardening=0.1, damping=None):

    # generate Model data structure
    model = ops.Model(ndm=2, ndf=3)

    # Length of cantilever column
    L = 8*ft;
    # specify node coordinates
    model.node(1,  0,   0 );  # first node
    model.node(2,  0,   L );  # second node

    # boundary conditions
    model.fix(1, 1, 1, 1 )

    ## specify mass
    model.mass(2, 2.0, 2.0, small_mass)

    # Define material

    mat_tag = 1      # identifier that will be assigned to the new material
    E    = 29000*ksi
    fy   =    60*ksi
    Hkin =     E*hardening
    Hiso =     E*hardening
    model.uniaxialMaterial("Steel01", mat_tag, fy, E, hardening)
#   model.uniaxialMaterial("ElasticPP", mat_tag, E, fy/E)
#   model.uniaxialMaterial("UniaxialJ2Plasticity", mat_tag, E, fy, Hkin, Hiso)


    # Load cross section geometry and add to Model
    sec_tag = 1          # identifier that will be assigned to the new section
    SecData = {}
    SecData["nft"] = 4   # no of layers in flange
    SecData["nwl"] = 8   # no of layers in web
    SecData["IntTyp"] = "Midpoint";
    SecData["FlgOpt"] = True
    section = opensees.section.from_aisc("Fiber", "W24x131", # "W14x426", 
                                         sec_tag, tag=mat_tag, mesh=SecData, ndm=2, units=units)

    cmd = opensees.tcl.dumps(section, skip_int_refs=True)
    model.eval(cmd)

    # Create element integration scheme
    nIP = 4
    int_tag = 1
    model.beamIntegration("Lobatto", int_tag, sec_tag, nIP)

    # Create element geometric transformation
    model.geomTransf("Linear", 1)

    # Finally, create the element
    #                                    CONN   Geom    Int
    model.element("ForceBeamColumn", 1, (1, 2),  1,   int_tag)

    # Apply damping in the first mode
    model.analysis("Transient")
    # model.eigen(1)
    # zeta  = 0.02
    # model.modalDamping(zeta)

#   alphaM, betaK = 0.01, 0.01
#   model.rayleigh(alphaM, betaK, 0, 0)
    return model



# #### Perform integration
def analyze(model, form, init="a", n=None):

    Event = quakeio.read("TAK000.AT2")
    AccHst = Event.data
    Deltat = Event["time_step"]


    load_tag = 1
    model.timeSeries('Path', load_tag, dt=Deltat, factor=1.0,
                             values=units.gravity*AccHst)

#   model.verbosity(0)
    model.test("NormUnbalance", 1e-8,   48, 9)
#   model.test("NormDispIncr",  1e-12, 25, 9)
    model.pattern('UniformExcitation', 1, 1, accel=load_tag)

    model.system("FullGen")
    #                           gam  bet
    model.integrator("Newmark", 1/2, 1/4, form=form, init=init)

    nt   = len(AccHst)
    if n is None:
        n = nt

    u   = np.zeros((n,3))*np.nan
    bad = np.zeros(n, dtype=bool)
    itr = np.zeros(n, dtype=int)

    con = {
        k: np.zeros(n)*np.nan for k in ("A", "K")
    }
    det  = {
        k: np.zeros(n)*np.nan for k in ("A", "K")
    }

    for k in range(n):
        if model.analyze(1, Deltat) != 0:
            model.algorithm("ModifiedNewton", "-initial")
#           model.algorithm("ModifiedNewton", "-initialThenCurrent")
            bad[k] = True
            if model.analyze(1, Deltat) != 0:
                u[k][0] = model.nodeDisp (2, 1)
                u[k][2] = model.nodeDisp (2, 3)
                print("Analysis failed")
                break
            else:
                model.algorithm("Newton")

        # extract values for plotting from response history
        u[k][0] = model.nodeDisp (2, 1)
        u[k][2] = model.nodeDisp (2, 3)
        A = model.getTangent()
        K = model.getTangent(k=1.0)
        con["A"][k] = np.linalg.cond(A)
        con["K"][k] = np.linalg.cond(K)
        det["A"][k] = np.linalg.det(A)
        det["K"][k] = np.linalg.det(K)
        itr[k]      = model.testIter()

    t = np.arange(nt)*Deltat
    return t[:n], u, AccHst[:n], con, det, bad, itr

