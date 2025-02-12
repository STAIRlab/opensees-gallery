#
# Simply Supported Beam Example 6.1
# ---------------------------------
#  Simply supported beam modeled with
#  two dimensional solid elements
# 
# Example Objectives
# ------------------
#  test different quad elements
#  free vibration analysis starting from static deflection

# import the OpenSees Python module
import opensees.openseespy as ops
from opensees.units.english import gravity as g

# ----------------------------
# Start of model generation
# ----------------------------
def create_model(element: str = "quad"):

    # create ModelBuilder (with two-dimensions and 2 DOF/node)
    model = ops.Model(ndm=2, ndf=2)

    # Define the material
    # -------------------
    thick = 2.0;
    #                                 tag  E      nu      rho
    model.material("ElasticIsotropic", 1, 1000.0, 0.25, 6.75/g)
    model.section("PlaneStrain", 1, material=1, thickness=thick)

    # Define geometry
    # ---------------

    nx = 5*10; # NOTE: nx MUST BE EVEN FOR THIS EXAMPLE
    ny = 2*4
    bn = nx + 1
    l1 = int(nx/2 + 1)
    l2 = int(l1 + ny*(nx+1))

    # now create the nodes and elements using the surface command
    if element in { "quad", "enhancedQuad", "tri31", "LagrangeQuad"}:
        args = (thick, "PlaneStrain", 1)

    elif element == "SSPquad":
#       args = (1, "PlaneStrain", thick)
        args = (thick, "PlaneStrain", 1)

    elif element == "bbarQuad":
        args = (thick, 1)

    surface = model.surface((nx, ny),
                  element=element, args=args,
                  points={
                    1: [  0.0,  0.0],
                    2: [ 40.0,  0.0],
                    3: [ 40.0, 10.0],
                    4: [  0.0, 10.0]
                  })

    # Single point constraints
    #      node u1 u2    
    model.fix( 1, 1, 1)
    model.fix(bn, 0, 1)

    # Define gravity loads
    # create a Plain load pattern with a linear time series
    model.pattern("Plain", 1, "Linear")
    model.load(l1, (0.0, -1.0), pattern=1)
    model.load(l2, (0.0, -1.0), pattern=1)

    return model, (l1, l2)



# --------------------------------------------------------------------
# Start of static analysis (creation of the analysis & analysis itself)
# --------------------------------------------------------------------

def static_analysis(model):
    # Define the system of equation
    model.system("ProfileSPD")

    # Define the DOF numberer
    model.numberer("RCM")

    # Define the constraint handler
    model.constraints("Plain")

    # Define the convergence test
    model.test("EnergyIncr", 1.0e-12, 10)

    # Define the solution algorithm, a Newton-Raphson algorithm
    model.algorithm("Newton")

    # Create the load control with variable load steps
    model.integrator("LoadControl", 1.0, 1, 1.0, 10.0)

    # Declare the analysis type
    model.analysis("Static")

    # Perform static analysis in 10 increments
    model.analyze(10)


def dynamic_analysis(model, l1):
    # ----------------------------
    # Start of recorder generation
    # ----------------------------

    model.recorder("Node", "disp", "-file", "Node.out", "-time", node=l1, dof=2)

    # ---------------------------------------
    # Create and Perform the dynamic analysis
    # ---------------------------------------
    # Remove the static analysis & reset the time to 0.0
    model.wipeAnalysis()
    model.setTime(0.0)

    # Now remove the loads and let the beam vibrate
    model.remove("loadPattern", 1)

    # create the system of equation
    model.system("ProfileSPD")

    # create the DOF numberer
    model.numberer("RCM")

    # create the constraint handler
    model.constraints("Plain")

    # create the convergence test
    model.test("EnergyIncr", 1.0e-12, 10)

    # create the solution algorithm, a Newton-Raphson algorithm
    model.algorithm("Newton")

    # create the integration scheme, the Newmark with gamma=0.5 and beta=0.25
    model.integrator("Newmark", 0.5, 0.25)

    # create the analysis object 
    model.analysis("Transient")

    # record once at time 0
    model.record()

    # Perform the transient analysis (20 sec)
    #        numSteps  dt
    model.analyze(1000, 0.05)


if __name__ == "__main__":
    import time
    for element in "quad", : # "LagrangeQuad": # "SSPquad", "bbarQuad", "enhancedQuad":
        model, (l1, l2) = create_model(element)
        start = time.time()
        static_analysis(model)
        print(f"Finished {element}, {time.time() - start} sec")
        print(model.nodeDisp(l2))

#       dynamic_analysis(model, l1)

#       print(model.nodeDisp(l2))

