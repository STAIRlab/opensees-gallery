# ===----------------------------------------------------------------------===//
# 
#         OpenSees - Open System for Earthquake Engineering Simulation    
#                Structural Artificial Intelligence Laboratory
#                          stairlab.berkeley.edu
# 
# ===----------------------------------------------------------------------===//
#
# This file defines various functions to create and analyze a portal frame. 
# The main function is called main. This calls the following functions:
#
#   create_portal(width, height) - create the model
#   gravity_analysis(model, P) - perform gravity analysis
#   pushover_analysis(model, H) - perform pushover analysis
#   dynamic_analysis(model) - perform dynamic analysis
#
import opensees.openseespy as ops

def eigen(model):
    from scipy.linalg import eig
    m = model.getTangent(m=1)
    k = model.getTangent(k=1)
    w, v = eig(k, m)
    return w

def create_portal(width  = 360.0, height = 144.0):

    # create ModelBuilder (with two-dimensions and 3 DOF/node)
    model = ops.Model(ndm=2, ndf=3)

    # Create nodes
    # ------------
    # create nodes with tag, (x, y)
    model.node(1, (0.0,      0.0))
    model.node(2, (width,    0.0))
    model.node(3, (0.0,   height))
    model.node(4, (width, height))

    # set the boundary conditions - command: fix nodeID uxRestrnt? uyRestrnt? rzRestrnt?
    model.fix(1, (1, 1, 1))
    model.fix(2, (1, 1, 1))

    # Define materials for nonlinear columns
    # ------------------------------------------
    # CONCRETE                          tag  f'c    ec0    f'cu   ecu
    # Core concrete (confined)
    model.uniaxialMaterial("Concrete01", 1, -6.0, -0.004, -5.0, -0.014)
    # Cover concrete (unconfined)
    model.uniaxialMaterial("Concrete01", 2, -5.0, -0.002,  0.0, -0.006)

    # STEEL
    # Reinforcing steel 
    fy =    60.0;      # Yield stress
    E  = 30000.0;      # Young's modulus
    #                                tag fy  E   b
    model.uniaxialMaterial("Steel01", 3, fy, E, 0.01)

    # Define cross-section for nonlinear columns
    # ------------------------------------------
    # set some parameters
    colWidth = 15.0
    colDepth = 24.0
    cover    =  1.5
    As       =  0.6      # area of no. 7 bars

    # some variables derived from the parameters
    y1 = colDepth/2.0
    z1 = colWidth/2.0

    model.section("Fiber", 1)
    # Create the concrete core fibers
    model.patch("rect", 1, 10, 1, cover-y1, cover-z1, y1-cover, z1-cover, section=1)
    # Create the concrete cover fibers (top, bottom, left, right)
    model.patch("rect", 2, 10, 1, -y1, z1-cover, y1, z1, section=1)
    model.patch("rect", 2, 10, 1, -y1, -z1, y1, cover-z1, section=1)
    model.patch("rect", 2,  2, 1, -y1, cover-z1, cover-y1, z1-cover, section=1)
    model.patch("rect", 2,  2, 1,  y1-cover, cover-z1, y1, z1-cover, section=1)
    # Create the reinforcing fibers (left, middle, right, section=1)
    model.layer("straight", 3, 3, As, y1-cover, z1-cover, y1-cover, cover-z1, section=1)
    model.layer("straight", 3, 2, As,      0.0, z1-cover,      0.0, cover-z1, section=1)
    model.layer("straight", 3, 3, As, cover-y1, z1-cover, cover-y1, cover-z1, section=1)
    # define beam integration
    np = 5;  # number of integration points along length of element

    # model.beamIntegration("Lobatto", 1, 1, np)

    # Define column elements
    # ----------------------
    # Geometry of column elements
    #                         tag 
    model.geomTransf("PDelta", 1)

    # Create the columns using Beam-column elements
    #                              tag   nodes trn itg
    model.element("forceBeamColumn", 1, (1, 3), np, 1,  1)
    model.element("forceBeamColumn", 2, (2, 4), np, 1,  1)

    # Define girder element
    # -----------------------------
    # Geometry of girder element
    #                         tag 
    model.geomTransf("Linear", 2)

    # Create the girder element
    #                                tag  nodes     A      E       Iz   transfTag
    model.element("elasticBeamColumn", 3, (3, 4), 360.0, 4030.0, 8640.0, 2)

    return model

def gravity_analysis(model, P=180.0)->int:
  # initialize in case we need to do an initial stiffness iteration
    model.initialize()
    #
    # Define gravity loads
    # --------------------
    # Set a parameter for the axial load
#   P = 180.0;  # 10% of axial capacity of columns

    # Create a Plain load pattern
    #               Type  tag timeSeries loads
    model.pattern("Plain", 1, "Linear", load={
    # nodeID  xForce yForce zMoment
         3:   [ 0.0,   -P,   0.0],
         4:   [ 0.0,   -P,   0.0]
    })

    # Start of analysis generation
    # ------------------------------

    # Create the system of equation
    model.system("ProfileSPD")

    # Create the constraint handler, the transformation method
    model.constraints("Transformation")

    model.numberer("RCM")

    # create the convergence test, the norm of the residual with a tolerance of 
    # 1e-12 and a max number of iterations of 10
    model.test("NormDispIncr", 1.0e-12, 10)

    # create the solution algorithm, a Newton-Raphson algorithm
    model.algorithm("Newton")

    # Define the integration scheme: the LoadControl scheme using steps of 0.1
    model.integrator("LoadControl", 0.1)

    # Define the analysis type
    model.analysis("Static")

    # 
    # FPerform the analysis
    # ------------------------------
    # perform the gravity load analysis in 10 steps to reach the load level
    return model.analyze(10)


def pushover_analysis(model, H=10.0):
    #  Nonlinear pushover analysis
    #
    # Portal Frame Example 3.2
    # ------------------------
    # - Reinforced concrete one-bay, one-story frame
    # - Distributed vertical load on girder
    # - Lateral Load at top of frame

    # ----------------------------------------------------
    # Define lateral loads
    # ----------------------------------------------------

    # Set the gravity loads to be constant & reset the time in the domain
    model.loadConst(time=0.0)


    # Define lateral loads
    # --------------------
    # Set some parameters
    H = 10.0 		# Reference lateral load

    # Define pattern 2  for lateral loads with a Linear TimeSeries
    model.pattern("Plain", 2, "Linear")

    # create the nodal loads - nodeID xForce yForce zMoment
    model.load(3, (H, 0.0, 0.0), pattern=2)
    model.load(4, (H, 0.0, 0.0), pattern=2)


    # ----------------------------------------------------
    # Start of modifications to analysis for push over
    # ----------------------------------------------------

    dU = 0.1;	        # Displacement increment

    # Set the integration scheme to be displacement control
    #                                    node dof init Jd min max
    model.integrator("DisplacementControl", 3, 1, dU, 1, dU, dU)


    # ------------------------------
    # Perform the analysis
    # ------------------------------

    # Set some parameters
    maxU = 15.0;	        # Max displacement
    numSteps = int(maxU/dU)

#   # First try to perform all steps at once
#   status = model.analyze(numSteps)

    u = []
    p = []

    # If the previous attempt was not successful, try
    # more complitated strategies

    u.append(model.nodeDisp(3, 1))
    p.append(model.getTime())

    status = ops.successful

    # Analyze in single steps until either (1) we reach maxU,
    # or (2) the analysis fails
    while status == ops.successful and u[-1] < maxU:

        status = model.analyze(1)

        # if the analysis failed, try initial tangent iteration
        if status != ops.successful:
            print("... Newton failed, trying initial stiffness")
            model.test("NormDispIncr", 1.0e-12, 1000, 5)
            model.algorithm("ModifiedNewton", initial=True)
            status = model.analyze(1)
            if status == ops.successful:
                print("... that worked, back to regular Newton")

            model.test("NormDispIncr", 1.0e-12, 10)
            model.algorithm("Newton")

        u.append(model.nodeDisp(3, 1))
        p.append(model.getTime())

    if status != ops.successful:
        raise Exception("Pushover analysis failed")

    return u, p


def dynamic_analysis(model):

  # ----------------------------------------------------
  # Start of additional modeling for dynamic loads
  # ----------------------------------------------------

  # Set the gravity loads to be constant & reset the time in the domain
  model.loadConst(time=0.0)

  # Define nodal mass in terms of axial load on columns
  g = 386.4
  P = 180
  m = P/g

  #         tag  MX  MY   RZ
  model.mass( 3, (m,  m,  0.0))
  model.mass( 4, (m,  m,  0.0))

  outFile = "out/ARL360.in"
  dt = 0.02

  # Set time series to be passed to uniform excitation
  model.timeSeries('Path', 1, filePath=outFile,  dt=dt,  factor=g)


  # Create UniformExcitation load pattern
  #                                 tag  dir 
  model.pattern("UniformExcitation",  2,  1, accel=1)


  # set the rayleigh damping factors for nodes & elements
  model.rayleigh(0.0, 0.0, 0.0, 0.000625)

  # ---------------------------------------------------------
  # Start of modifications to analysis for transient analysis
  # ---------------------------------------------------------

  # Clear the old analysis settings
  model.wipeAnalysis()

  model.system('BandGeneral')

  model.constraints('Plain')

  # Create the convergence test, the norm of the residual with a tolerance of 
  # 1e-12 and a max number of iterations of 10
  model.test('NormDispIncr', 1.0e-12, 10)

  model.algorithm('Newton')

  # Create the integration scheme, the Newmark with alpha =0.5 and beta =.25
  model.integrator('Newmark',  0.5,  0.25)

  model.analysis('Transient')

#   model.recorder('EnvelopeNode', "disp",  time=True, file='out/disp.out', node=(3, 4), dof=1)
#   model.recorder('EnvelopeNode', "accel", time=True, file='out/accel.out', timeSeries=1,  node=(3, 4), dof=1)

#   model.recorder('Element', "force", time=True, file='out/ele1secForce.out', ele=1, section=1)
#   model.recorder('Element', "deformation", time=True, file='out/ele1secDef.out',   ele=1, section=1)

  # ------------------------------
  # Finally perform the analysis
  # ------------------------------
  print(eigen(model))
  print(f"... eigen values at start of transient: {model.eigen(2)}")

  step = 0.01

  for i in range(2000):
  # while  status == 0  and  tCurrent < tFinal:

      status = model.analyze(1, step)

      if status != 0:
          print("... Newton failed, trying initial stiffness")
          model.test('NormDispIncr', 1.0e-12,  100, 0)
          model.algorithm('ModifiedNewton', initial=True)
          status = model.analyze(1, step)
          if status == 0:
              print("... that worked, back to regular Newton")
          else:
              raise RuntimeError("Dynamic analysis failed")

          model.test('NormDispIncr', 1.0e-12,  10)
          model.algorithm('Newton')

  return status


def main():
    # Create the model
    model = create_portal()

    # perform analysis under gravity loads
    status = gravity_analysis(model)
    if status == ops.successful:
        print("Gravity analysis SUCCESSFUL\n")
    else:
        print(f"Gravity analysis FAILED ({status = })\n")

    # Print the state at node 3
    u3 = model.nodeDisp(3)
    print("u3 = ", u3)

    u,p = pushover_analysis(model)

    # Print the state at node 3
    u3 = model.nodeDisp(3)
    print("u3 = ", u3)

    #
    # Plot the results
    #
    import matplotlib.pyplot as plt
    # Try using a prettier plotting style
    try:
        plt.style.use("typewriter")
    except:
        pass

    fig, ax = plt.subplots()
    ax.plot(u,p)
    ax.set_xlabel("Displacement [in]")
    ax.set_ylabel("Base Shear [kips]")
    plt.show()
    fig.savefig("img/pushover-node-3.svg")


    #
    # Dynamic analysis
    #

    # Create the model
    model = create_portal()
    gravity_analysis(model)

    # Perform the dynamic analysis
    status = dynamic_analysis(model)

    # Print a message to indicate if analysis successful or not
    if status == 0:
        print("Transient analysis SUCCESSFUL")
    else:
        print("Transient analysis FAILED")

    # Perform an eigenvalue analysis
    print(f"... eigen values at end of transient: {model.eigen(2)}")


if __name__ == "__main__":
    main()

