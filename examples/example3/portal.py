import opensees.openseespy as ops

def portal_frame():
    # create ModelBuilder (with two-dimensions and 3 DOF/node)
    model = ops.Model(ndm=2, ndf=3)

    # Create nodes
    # ------------
    # Set parameters for overall model geometry
    width = 360.0
    height = 144.0

    # create nodes & add to Domain - command: node nodeId xCrd yCrd
    model.node(1, 0.0,   0.0)
    model.node(2, width, 0.0)
    model.node(3, 0.0,   height)
    model.node(4, width, height)

    # set the boundary conditions - command: fix nodeID uxRestrnt? uyRestrnt? rzRestrnt?
    model.fix(1, 1, 1, 1)
    model.fix(2, 1, 1, 1)

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
    E = 30000.0;    # Young's modulus
    #                              tag fy  E0  b
    model.uniaxialMaterial("Steel01", 3, fy, E, 0.01)

    # Define cross-section for nonlinear columns
    # ------------------------------------------
    # set some parameters
    colWidth = 15.0
    colDepth = 24.0
    cover = 1.5
    As = 0.60;     # area of no. 7 bars

    # some variables derived from the parameters
    y1 = colDepth/2.0
    z1 = colWidth/2.0

    model.section("Fiber", 1)
    # Create the concrete core fibers
    model.patch("rect", 1, 10, 1, cover-y1, cover-z1, y1-cover, z1-cover)
    # Create the concrete cover fibers (top, bottom, left, right)
    model.patch("rect", 2, 10, 1, -y1, z1-cover, y1, z1)
    model.patch("rect", 2, 10, 1, -y1, -z1, y1, cover-z1)
    model.patch("rect", 2,  2, 1, -y1, cover-z1, cover-y1, z1-cover)
    model.patch("rect", 2,  2, 1,  y1-cover, cover-z1, y1, z1-cover)
    # Create the reinforcing fibers (left, middle, right)
    model.layer("straight", 3, 3, As, y1-cover, z1-cover, y1-cover, cover-z1)
    model.layer("straight", 3, 2, As, 0.0, z1-cover, 0.0, cover-z1)
    model.layer("straight", 3, 3, As, cover-y1, z1-cover, cover-y1, cover-z1)
    # define beam integration
    np = 5;  # number of integration points along length of element
    model.beamIntegration("Lobatto", 1, 1, np)

    # Define column elements
    # ----------------------
    # Geometry of column elements
    #                       tag 
    model.geomTransf("PDelta", 1)

    # Create the columns using Beam-column elements
    #                   tag ndI ndJ transfTag integrationTag
    eleType = "ForceBeamColumn"
    model.element(eleType, 1, 1, 3, 1, 1)
    model.element(eleType, 2, 2, 4, 1, 1)

    # Define beam element
    # -----------------------------
    # Geometry of column elements
    #                tag 
    model.geomTransf("Linear", 2)

    # Create the beam element
    #                               tag ndI ndJ  A     E       Iz   transfTag
    model.element("ElasticBeamColumn", 3, 3, 4, 360.0, 4030.0, 8640.0, 2)

    return model
