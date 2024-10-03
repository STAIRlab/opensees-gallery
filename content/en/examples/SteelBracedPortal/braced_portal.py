import opensees.openseespy as ops
# --------------------------------------------------------------------------------------------------
# Example: 1-Story 1-Bay Special Concentric Braced Frame
# Braces are defined with two force beam-column elements
# Elements are fully rigid when in touch with gusetplates
#
# Rigid liks of the braces are defined with rigid elastic elements. Beam and
# column reigid elemnts are defined using rigid offs = inside of geometric
# transformation.
#
# This example is written for the OpenSeesRT interpreter.
# Install by running:
#     pip install opensees
#
# To run this example:
#     python -m opensees CB_PortalFrame.tcl
#
# Created by:  Vesna Terzic, UC Berkeley, 2011
# Units: kips, inches, seconds
#
# Element and Node ID conventions:
#        1xy = frame columns
#        2xy = frame beams
#        3xy = braces
#        6xy = rigid links
#
# --------------------------------------------------------------------------------------------------
#       Set Up & Source Definition
# --------------------------------------------------------------------------------------------------
def WSection( secID, matID, d bf, tf, tw, nfdw, nftw, nfbf, nftf):

    dw = (d - 2 * tf)
    y1 = (-d/2)
    y2 = (-dw/2)
    y3 = ( dw/2)
    y4 = ( d/2)

    z1 = (-bf/2)
    z2 = (-tw/2)
    z3 = ( tw/2)
    z4 = ( bf/2)

    model.section("Fiber", secID,  GJ=1e8)

    patch.quadr(matID  nfbf nftf   y1 z4   y1 z1   y2 z1   y2 z4)
    patch.quadr(matID  nftw nfdw   y2 z3   y2 z2   y3 z2   y3 z3)
    patch.quadr(matID  nfbf nftf   y3 z4   y3 z1   y4 z1   y4 z4)


def HSSsection( secID, matID, d t, nfdy, nfty, nfdz, nftz):

    dw = (d - 2 * t)
    y1 = (-d/2)
    y2 = (-dw/2)
    y3 = ( dw/2)
    y4 = ( d/2)

    z1 = (-d/2)
    z2 = (-dw/2)
    z3 = ( dw/2)
    z4 = ( d/2)

    section.fiberSec( secID GJ=1e8,  , [

           patch.quadr(matID  nftz nfdy   y2 z4   y2 z3   y3 z3   y3 z4),
           patch.quadr(matID  nftz nfdy   y2 z2   y2 z1   y3 z1   y3 z2),
           patch.quadr(matID  nfdz nfty   y1 z4   y1 z1   y2 z1   y2 z4),
           patch.quadr(matID  nfdz nfty   y3 z4   y3 z1   y4 z1   y4 z4),


def braced_portal():
    model = ops.Model(ndm=3)

    # --------------------------------------------------------------------------------------------------
    #       Define Building Geometry, Nodes, and Constraints
    # --------------------------------------------------------------------------------------------------
    # define structure-geometry parameters
    NStories = 1;
    NBays = 1;
    WBay = 360.;
    HStory = 180.;
    HBuilding = NStories*HStory;

    # Calculate locations frame nodes:
    Pier1 = 0.0
    Pier2 =  Pier1 + WBay
    Floor1 = 0.0
    Floor2 = Floor1 + HStory


    # Joint offdistance = for beams columns and braces 
    # (it is assumed that the the rigid brace lenght is 0.15*Lbr and the angle alpha for a gusplate = is 25 degrees)
    jOff_col_1 = 27.18;
    jOff_beam_2 = 29.25;
    jOff_braceX = 27.0;
    jOff_braceY = 27.0;

    # Calculate nodal masses -- lump floor masses at frame nodes
    g = 386.4;

    NodalMass2H = 1.26;

    NodalMass2V = 0.105;

    # Define nodes and assign masses to beam-column intersections of frame


    model.node(11 Pier1 Floor1 0);
    model.node(21 Pier2 Floor1 0);
    model.node(12 Pier1 Floor2 0 mass=NodalMass2H,  NodalMass2V 0.0 0 0 0);
    model.node(22 Pier2 Floor2 0 mass=NodalMass2H,  NodalMass2V 0.0 0 0 0);

    # define extra nodes in the braces



    model.node(111, (Pier1)+WBay/4.0) '[expr', Floor1+HStory/2.0] 0
    model.node(112, (Pier2-WBay/4.0) '[expr', Floor1)+HStory/2.0] 0

    # define extra nodes in the beams



    model.node(221,      Pier1, Floor2, 0)
    model.node(222, (WBay/2.0), Floor2, 0)
    model.node(223,      Pier2, Floor2, 0)

    # define extra nodes for rigid links in the braces:



    model.node(411,            (Pier1)+jOff_braceX),  Floor1+jOff_braceY, 0)
    model.node(412,   (Pier1)+WBay/2.0-jOff_braceX),  Floor2-jOff_braceY, 0)
    model.node(413,             (Pier2-jOff_braceX),  Floor1+jOff_braceY, 0)
    model.node(414,   (Pier2-WBay/2.0)+jOff_braceX),  Floor2-jOff_braceY, 0)

    # assign boundary condidtions



    model.fix(11 1 1 1   1 1 1)
    model.fix(21 1 1 1   1 1 1)

    # define constraints for pined beam-to-column connection

    equalDOF 12 221 1 2
    equalDOF 22 223 1 2

    # --------------------------------------------------------------------------------------------------
    #       Define Materials and Sections
    # --------------------------------------------------------------------------------------------------

    # define material for nonlinear beams and columns
    matID_BC = 1
    matID_fatBC = 2
    Es = 29000.0;
    Fy = 50.0;
    b = 0.003;
    model.uniaxialMaterial('Steel02', matID_BC, Fy, Es, b, 20, 0.925, 0.15)
    model.uniaxialMaterial('Fatigue', matID_fatBC, matID_BC)


    # define material for braces
    matID_Brace = 3
    matID_fatBrace = 4
    E0 = 0.095
    m = -0.5
    model.uniaxialMaterial('Steel02', matID_Brace, Fy, Es, b, 20 0.925 0.15 0.0005 0.01 0.0005 0.01)
    model.uniaxialMaterial('Fatigue', matID_fatBrace matID_Brace -E0 E0 m=m, )

    # define sections for columns and beams





    WSection 11 matID_fatBC 15.22 15.65  1.31 0.83  14 2 14 2


    WSection 22 matID_fatBC 26.71 9.96   0.64 0.46  20 2 10 2

    # define sections for braces



    HSSsection 31 matID_fatBrace 12. 0.625 12 2 12 2

    # --------------------------------------------------------------------------------------------------
    #       Define Geometric Transformation
    # --------------------------------------------------------------------------------------------------

    # Columns


    model.geomTransf('PDelta',  11   0 0 1 jntOffset=0.0,  jOff_col_1 0    0.0 0.0 0)

    # Beams


    model.geomTransf('PDelta', 221   0 0 1 jntOffset=0.0,  0.0 0    -jOff_beam_2 0.0 0)
    model.geomTransf('PDelta', 222   0 0 1 -jntOffjOff_beam_2 = 0.0 0   0.0 0.0 0)

    # Braces
    model.geomTransf('Corotational', 31 0 0 1)

    # Rigid links
    model.geomTransf('Linear', 41 0 0 1)

    print("A")

    # --------------------------------------------------------------------------------------------------
    #       Define Elements
    # --------------------------------------------------------------------------------------------------

    # define columns of a braced frame:



    model.element('ForceBeamColumn',   111      11     12        5         11       11)
    model.element('ForceBeamColumn',   121      21     22        5         11       11)
    print("B")
    # define beams of a braced frame:




    model.element('ForceBeamColumn',   221     221    222       5         22       221)
    model.element('ForceBeamColumn',   222     222    223       5         22       222)
    print("C")
    # define braces:

    model.element('ForceBeamColumn',   311     411    111        5         31       31)
    model.element('ForceBeamColumn',   312     111    412        5         31       31)
    model.element('forceBeamColumn',   313     413    112        5         31       31)
    model.element('forceBeamColumn',   314     112    414        5         31       31)
    print("D")

    # define rigid links:
    Arigid1 =  25.7*10.
    Arigid2 =  21.*10.
    Arigid3 =  13.5*10.
    Irigid  = 30000.

    model.section('ElasticFrame', 1010, A=Arigid1,  E=Es,  Iz=Irigid,  Iy=Irigid,  G=Es,  J=60000)

    model.element('PrismFrame',     611,  ( 11,    411),   section=1010,     transform=41)
    model.element('PrismFrame',     612,  (222,    412),   section=1010,     transform=41)
    model.element('PrismFrame',     613,  ( 21,    413),   section=1010,     transform=41)
    model.element('PrismFrame',     614,  (222,    414),   section=1010,     transform=41)

    # --------------------------------------------------------------------------------------------------
    #       Eigenvalue Analysis
    # --------------------------------------------------------------------------------------------------
    pi = 2.0*asin(1.0);
    nEigenI = 1;
    nEigenJ = 2;
    lambdaN = model.eigen(nEigenJ);
    lambdaI = lambdaN[0]
    lambdaJ = lambdaN[nEigenJ-1]
    w1 = lambdaI**0.5;
    w2 = lambdaJ**0.5;
    T1 = 2.0*pi/w1;
    T2 = 2.0*pi/w2;
    print("T1 = T1 s");
    print("T2 = T2 s");

    # --------------------------------------------------------------------------------------------------
    #       Gravity Loads & Gravity Analysis
    # --------------------------------------------------------------------------------------------------
    # Apply gravity loads


    P_F2 = -40.46;
    model.pattern('Plain', 101, "Linear")



    model.load(12, 0.0, P_F2, 0.0,    0, 0, 0, pattern=1);
    model.load(22, 0.0, P_F2, 0.0,    0, 0, 0, pattern=1);


    # Gravity-analysis: load-controlled static analysis
    Tol = 1.0e-6;
    model.constraints(Transformation);

    model.test("NormDispIncr", Tol, 10);
    model.algorithm("Newton");
    NstepGravity = 10;
    DGravity = 1.0/NstepGravity;
    model.integrator('LoadControl', DGravity);
    model.analysis(Static);
    model.analyze(NstepGravity);

    model.loadConst(time=0.0)

    model.print("-json", "model.json")

