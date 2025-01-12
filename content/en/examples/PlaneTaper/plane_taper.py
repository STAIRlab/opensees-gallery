#
# Tapered cantilever beam
#
# Description
# -----------
#  Tapered cantilever beam modeled with two dimensional solid elements
# 
# Objectives
# ----------
#  Test different plane elements

# import the OpenSees Python module
import opensees.openseespy as ops

# ----------------------------
# Start of model generation
# ----------------------------
def create_model(mesh,
                 thickness=1,
                 element: str = "LagrangeQuad"):

    nx, ny = mesh

    # create model in two dimensions with 2 DOFs per node
    model = ops.Model(ndm=2, ndf=2)

    # Define the material
    # -------------------
    #                                 tag  E      nu   rho
    model.material("ElasticIsotropic", 1, 1000.0, 0.25, 0, "-plane-strain")

    # Define geometry
    # ---------------

    thick = 2.0;

    bn = nx + 1
    l1 = int(nx/2 + 1)
    l2 = int(l1 + ny*(nx+1))

    b = 30
    r = 7.5/100
    L = 100.0

    # now create the nodes and elements using the surface command
    # {"quad", "enhancedQuad", "tri31", "LagrangeQuad"}:
    args = (thick, "PlaneStrain", 1)

    surface = model.surface((nx, ny),
                  element=element, args=args,
                  points={
                    1: [  0.0,   0.0],
                    2: [   L,    L*r],
                    3: [   L,  b-L*r],
                    4: [  0.0, b]
                  })

    # Single-point constraints
    #            x   (u1 u2)
    model.fixX( 0.0, (1, 1))

    # Define gravity loads
    # create a Plain load pattern with a linear time series
    model.pattern("Plain", 1, "Linear")
    model.load(l1, 0.0, -1.0, pattern=1)
    model.load(l2, 0.0, -1.0, pattern=1)

    return model, (l1, l2)



# --------------------------------------------------------------------
# Start of static analysis (creation of the analysis & analysis itself)
# --------------------------------------------------------------------

def static_analysis(model):

    # Create the load control with variable load steps
    model.integrator("LoadControl", 1.0, 1, 1.0, 10.0)

    # Declare the analysis type
    model.analysis("Static")

    # Perform static analysis in 10 increments
    model.analyze(10)



if __name__ == "__main__":
    import time
    for element in "quad", "LagrangeQuad":
        model, (l1, l2) = create_model(element)
        start = time.time()
        static_analysis(model)
        print(f"Finished {element}, {time.time() - start} sec")
        print(model.nodeDisp(l2))


#       print(model.nodeDisp(l2))

