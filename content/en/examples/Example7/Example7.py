# OpenSees -- Open System for Earthquake Engineering Simulation
#         Pacific Earthquake Engineering Research Center

#
# 3D Shell Structure
# ------------------
#  Shell roof modeled with three dimensional linear shell elements

# Example Objectives
# ------------------
#  test linear-elastic shell element
#  free vibration analysis starting from static deflection
#
# Units: kips, in, sec
#
# Written: Andreas Schellenberg (andreas.schellenberg@gmail.com)
# Date: September 2017

# import the OpenSees Python module
import opensees.openseespy as ops

    # ----------------------------
    # Start of model generation
    # ----------------------------

def create_model(walk_edge=False):
    # create ModelBuilder (with three-dimensions and 6 DOF/node)
    model = ops.Model(ndm=3, ndf=6)

    E = 3.0e3

    # Define the section
    # ------------------
    #                                           tag E   nu     h    rho
    model.section("ElasticShell", 1, E, 0.25, 1.175, 1.27)
    model.section('ElasticFrame', 2, E, 1, area=10, Iy=1, Iz=1, J=1)

    # Define geometry
    # ---------------
    # these should both be even
    nx = 8
    ny = 2

    # loaded nodes
    mid   = int(((nx+1)*(ny+1) + 1)/2)
    side1 = int((nx+2)/2)
    side2 = int((nx+1)*(ny+1) - side1 + 1)

    # generate the surface nodes and elements
    surface = model.surface((nx, ny),
                  element="ShellMITC4", args=(1,),
                  points={
                      1: [-20.0,  0.0,  0.0],
                      2: [-20.0,  0.0, 40.0],
                      3: [ 20.0,  0.0, 40.0],
                      4: [ 20.0,  0.0,  0.0],
                      5: [-10.0, 10.0, 20.0],
                      7: [ 10.0, 10.0, 20.0],
                      9: [  0.0, 10.0, 20.0]
                  })


    for nodes in surface.walk_edge():
        # Note that supplying "None" as the tag
        # will cause the model to find the next
        # available tag and use it for the new
        # element
        model.element("PrismFrame", None, nodes, section=2, vertical=[0, 0, 1])


    # define the boundary conditions
    # rotation free about x-axis (remember right-hand-rule)
    model.fixZ( 0.0, 1, 1, 1, 0, 1, 1)
    model.fixZ(40.0, 1, 1, 1, 0, 1, 1)

    # create a pattern with a Linear time series
    # and add some loads
    model.pattern("Plain", 1, "Linear")
    model.load(mid  , 0.0, -0.50, 0.0, 0.0, 0.0, 0.0, pattern=1)
    model.load(side1, 0.0, -0.25, 0.0, 0.0, 0.0, 0.0, pattern=1)
    model.load(side2, 0.0, -0.25, 0.0, 0.0, 0.0, 0.0, pattern=1)

    return model

    # ----------------------- 
    # End of model generation
    # -----------------------


    # ------------------------
    # Start of static analysis
    # ------------------------
def static_analysis(model):
    # Load control with variable load steps
    #                              init  Jd  min  max
    model.integrator("LoadControl", 1.0, 1, 1.0, 10.0)

    # Convergence test
    #                  tolerance maxIter displayCode
    model.test("EnergyIncr", 1.0e-10, 20, 0)

    # Solution algorithm
    model.algorithm("Newton")

    # DOF numberer
    model.numberer("RCM")

    # Constraint handler
    model.constraints("Plain")

    # System of equations solver
    model.system("SparseGeneral", "-piv")
    #system("ProfileSPD")

    # Analysis for gravity load
    model.analysis("Static")

    # Perform the gravity load analysis
    return model.analyze(5)


def dynamic_analysis(model):
    # ----------------------------
    # Start of recorder generation
    # ----------------------------

    model.recorder("Node", "-file", "Node.out", "-time", "-node", mid, "-dof", 2, "disp")


    # ------------------------------------------
    # Configure and Perform the dynamic analysis
    # ------------------------------------------

    # Remove the static analysis & reset the time to 0.0
    model.wipeAnalysis()
    model.setTime(0.0)

    # Now remove the loads and let the beam vibrate
    model.remove("loadPattern", 1)

    # Create the transient analysis
    model.test("EnergyIncr", 1.0e-10, 20, 0)
    model.algorithm("Newton")
    model.numberer("RCM")
    model.constraints("Plain")
    model.system("SparseGeneral", "-piv")
    model.integrator("Newmark", 0.50, 0.25)
    model.analysis("Transient")

    # record once at time 0
    model.record()

    # Perform the transient analysis (20 sec)
    return model.analyze(100, 0.2)
    # model.analyze(250, 0.50)


if __name__ == "__main__":
    model = create_model()
    static_analysis(model)
    dynamic_analysis(model)

