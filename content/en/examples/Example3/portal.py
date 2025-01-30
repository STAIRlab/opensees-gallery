# ===----------------------------------------------------------------------===//
# 
#         OpenSees - Open System for Earthquake Engineering Simulation    
#                Structural Artificial Intelligence Laboratory
#                          stairlab.berkeley.edu
# 
# ===----------------------------------------------------------------------===//
#
#
# Units: kips, in, sec  
#
# Written: GLF/MHS/fmk
# Date: January 2001
#
# OpenSeesPy Version
#   Written: Andreas Schellenberg (andreas.schellenberg@gmail.com)
#   Date: June 2017
#
import opensees.openseespy as ops

def create_portal(width  = 360.0, height = 144.0):

    # create ModelBuilder (with two-dimensions and 3 DOF/node)
    model = ops.Model(ndm=2, ndf=3)

    # Create nodes
    # ------------
    # create nodes & add to Domain - command: node nodeId xCrd yCrd
    model.node(1, 0.0,      0.0)
    model.node(2, width,    0.0)
    model.node(3, 0.0,   height)
    model.node(4, width, height)

    # set the boundary conditions - command: fix nodeID uxRestrnt? uyRestrnt? rzRestrnt?
    model.fix(1, 1, 1, 1)
    model.fix(2, 1, 1, 1)

    # Define materials for nonlinear columns
    # ------------------------------------------
    # CONCRETE                          tag  f'c    ec0    f'cu   ecu
    # Core concrete (confined)
    model.uniaxialMaterial("Concrete01", 1, -6.0, -0.004, -5.0, -0.014)
    # Cover concrete (unconfined)
    model.uniaxialMaterial("Concrete01", 2, -5.0, -0.002, -0.0, -0.006)

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

    model.beamIntegration("Lobatto", 1, 1, np)

    # Define column elements
    # ----------------------
    # Geometry of column elements
    #                       tag 
    model.geomTransf("PDelta", 1)

    # Create the columns using Beam-column elements
    #                              tag   nodes trn itg
    model.element("ForceBeamColumn", 1, (1, 3), 1, 1)
    model.element("ForceBeamColumn", 2, (2, 4), 1, 1)

    # Define girder element
    # -----------------------------
    # Geometry of column elements
    #                         tag 
    model.geomTransf("Linear", 2)

    # Create the beam element
    #                                tag  nodes     A      E       Iz   transfTag
    model.element("ElasticBeamColumn", 3, (3, 4), 360.0, 4030.0, 8640.0, 2)

    return model

def gravity_analysis(model, P=180.0):
    #
    # Define gravity loads
    # --------------------
    # Set a parameter for the axial load
#   P = 180.0;                # 10% of axial capacity of columns

    # Create a Plain load pattern
    #               Type  tag timeSeries loads
    model.pattern("Plain", 1, "Linear", load={
    # nodeID  xForce yForce zMoment
         3:   [ 0.0,   -P,   0.0],
         4:   [ 0.0,   -P,   0.0]
    })

    # ------------------------------
    # Start of analysis generation
    # ------------------------------

    # Create the system of equation
    model.system("BandGeneral")

    # Create the constraint handler, a Plain handler is used as homo constraints
    model.constraints("Plain")

    # create the convergence test, the norm of the residual with a tolerance of 
    # 1e-12 and a max number of iterations of 10
    model.test("NormDispIncr", 1.0e-12, 10, 3)

    # create the solution algorithm, a Newton-Raphson algorithm
    model.algorithm("Newton")

    # Define the integration scheme: the LoadControl scheme using steps of 0.1
    model.integrator("LoadControl", 0.1)

    # Define the analysis type
    model.analysis("Static")

    # ------------------------------
    # Finally perform the analysis
    # ------------------------------

    # perform the gravity load analysis in 10 steps to reach the load level
    status = model.analyze(10)

    return status


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

    # Set some parameters
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
    if True : # status != ops.successful:

        u.append(model.nodeDisp(3, 1))
        p.append(model.getTime())

        status = ops.successful

        # Analyze in single steps until either (1) we reach maxU,
        # or (2) the analysis fails
        while status == ops.successful and u[-1] < maxU:

            status = model.analyze(1)

            # if the analysis failed, try initial tangent iteration
            if status != ops.successful:
                print("regular newton failed .. lets try an initial stiffness for this step")
                model.test("NormDispIncr", 1.0e-12, 1000)
                model.algorithm("ModifiedNewton", "-initial")
                status = model.analyze(1)
                if status == ops.successful:
                    print("that worked .. back to regular Newton")
                model.test("NormDispIncr", 1.0e-12, 10)
                model.algorithm("Newton")

            u.append(model.nodeDisp(3, 1))
            p.append(model.getTime())

    if status != ops.successful:
        raise Exception("Analysis failed")

    return u, p


def main():
    # Create the model
    model = create_portal()

    # perform analysis under gravity loads
    status = gravity_analysis(model)

    if status == ops.successful:
        print("Gravity analysis completed SUCCESSFULLY\n")
    else:
        print(f"Gravity analysis FAILED ({status = })\n")

    u,p = pushover_analysis(model)


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
    

    # Print the state at node 3
    u3 = model.nodeDisp(3)
    print("u3 = ", u3)

if __name__ == "__main__":
    main()

