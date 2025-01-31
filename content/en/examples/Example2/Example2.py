# ===----------------------------------------------------------------------===//
# 
#         OpenSees - Open System for Earthquake Engineering Simulation    
#                Structural Artificial Intelligence Laboratory
# 
# ===----------------------------------------------------------------------===//

# Moment-Curvature Example 2.1
# ----------------------------
#  Zero length element with fiber section
#  Single Nodal Load, Static Analysis
# 
# Example Objectives
# ------------------
#  Moment-Curvature Analysis in OpenSees

# import the OpenSees Python module
import opensees.openseespy as ops

def moment_curvature(model, secTag, axialLoad, maxK, numIncr):
    """
    A procedure for performing section analysis (only does
    moment-curvature, but can be easily modified to do any mode
    of section response.

    Arguments
       secTag -- tag identifying section to be analyzed
       axialLoad -- axial load applied to section (negative is compression)
       maxK -- maximum curvature reached during analysis
       numIncr -- number of increments used to reach maxK (default 100)

    Sets up a recorder which writes moment-curvature results to file
    section$secTag.out ... the moment is in column 1, and curvature in column 2

    Written: Andreas Schellenberg (andreas.schellenberg@gmail.com)
    Date: June 2017

    """

    # Define two nodes at (0,0)
    model.node(1, (0.0, 0.0))
    model.node(2, (0.0, 0.0))

    # Fix all degrees of freedom except axial and bending
    model.fix(1, (1, 1, 1))
    model.fix(2, (0, 1, 0))

    # Define element
    #                               tag ndI ndJ secTag
    model.element("zeroLengthSection", 1, 1, 2, secTag)

    # Create recorder
    model.recorder("Node", "disp", file="section"+str(secTag)+".out", time=True, node=2, dof=3)

    # Define constant axial load
    model.pattern("Plain", 1, "Constant", loads={2: [axialLoad, 0.0, 0.0]})

    # Define analysis parameters
    model.system("BandGeneral")
    model.numberer("Plain")
    model.constraints("Plain")
    model.test("NormUnbalance", 1.0e-9, 10)
    model.algorithm("Newton")
    model.integrator("LoadControl", 0.0)
    model.analysis("Static")

    # Do one analysis for constant axial load
    model.analyze(1)

    # Define reference moment
    model.pattern("Plain", 2, "Linear")
    model.load(2, (0.0, 0.0, 1.0), pattern=2)

    # Compute curvature increment
    dK = maxK/numIncr

    # Use displacement control at node 2 for section analysis
    model.integrator("DisplacementControl", 2, 3, dK, 1, dK, dK)

    # Do the section analysis
    model.analyze(numIncr)

def create_section():
    # ------------------------------
    # Start of model generation
    # ------------------------------

    # Create a model (with two-dimensions and 3 DOF/node)
    model = ops.Model(ndm=2, ndf=3)

    # Define materials for nonlinear columns
    # ------------------------------------------
    # CONCRETE                        tag  f'c    ec0    f'cu   ecu
    # Core concrete (confined)
    model.uniaxialMaterial("Concrete01", 1, -6.0, -0.004, -5.0, -0.014)
    # Cover concrete (unconfined)
    model.uniaxialMaterial("Concrete01", 2, -5.0, -0.002, -0.0, -0.006)

    # STEEL
    # Reinforcing steel 
    fy = 60.0;      # Yield stress
    E  = 30000.0;   # Young's modulus
    #                                tag fy  E0  b
    model.uniaxialMaterial("Steel01", 3, fy, E, 0.01)

    # Define cross-section for nonlinear columns
    # ------------------------------------------
    # set some parameters
    width = 15.0
    depth = 24.0
    cover = 1.5
    As = 0.60;     # area of no. 7 bars

    # some variables derived from the parameters
    y1 = depth/2.0
    z1 = width/2.0

    model.section("Fiber", 1)
    # Create the concrete core fibers
    model.patch("rect", 1, 10, 1, cover-y1, cover-z1, y1-cover, z1-cover, section=1)
    # Create the concrete cover fibers (top, bottom, left, right, section=1)
    model.patch("rect", 2, 10, 1, -y1, z1-cover, y1, z1, section=1)
    model.patch("rect", 2, 10, 1, -y1, -z1, y1, cover-z1, section=1)
    model.patch("rect", 2,  2, 1, -y1, cover-z1, cover-y1, z1-cover, section=1)
    model.patch("rect", 2,  2, 1,  y1-cover, cover-z1, y1, z1-cover, section=1)
    # Create the reinforcing fibers (left, middle, right, section=1)
    model.layer("straight", 3, 3, As, y1-cover, z1-cover, y1-cover, cover-z1, section=1)
    model.layer("straight", 3, 2, As, 0.0, z1-cover, 0.0, cover-z1, section=1)
    model.layer("straight", 3, 3, As, cover-y1, z1-cover, cover-y1, cover-z1, section=1)

    # Estimate yield curvature
    # (Assuming no axial load and only top and bottom steel)
    d = depth - cover   # d -- from cover to rebar
    epsy = fy/E            # steel yield strain
    Ky = epsy/(0.7*d)
    return model, Ky


if __name__ == "__main__":

    model, Ky = create_section()

    P   = -180.0    # Axial load
    mu  = 15.0      # Target ductility for analysis
    numIncr = 100   # Number of analysis increments


    print("Estimated yield curvature: ", Ky)

    # Call the section analysis procedure
    moment_curvature(model, 1, P, Ky*mu, numIncr)


    u = model.nodeDisp(2,3)
    if abs(u-0.00190476190476190541) < 1e-12:
        print('PASSED : MomentCurvature.py\n')
        print("Passed!")
    else:
        print('FAILED : MomentCurvature.py\n')
        print("Failed!")


