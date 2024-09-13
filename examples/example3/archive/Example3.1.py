# OpenSees -- Open System for Earthquake Engineering Simulation
# Pacific Earthquake Engineering Research Center
# http://opensees.berkeley.edu/
#
# Portal Frame Example 3.1
# ------------------------
#  Reinforced concrete one-bay, one-story frame
#  Distributed vertical load on girder
# 
# Example Objectives
# ------------------
#  Nonlinear beam-column elements
#  Gravity load analysis and eigenvalue analysis
#
# Written: Andreas Schellenberg (andreas.schellenberg@gmail.com)
# Date: June 2017

# import the OpenSees Python module
import opensees.openseespy as ops

# ------------------------------
# Start of model generation
# ------------------------------

# create ModelBuilder (with two-dimensions and 3 DOF/node)
model = ops.Model(ndm=2, ndf=3)

# Create nodes
# ------------
# Set parameters for overall model geometry
width  = 360.0
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
model.patch("rect", 1, 10, 1, cover-y1, cover-z1, y1-cover, z1-cover, section=1)
# Create the concrete cover fibers (top, bottom, left, right)
model.patch("rect", 2, 10, 1, -y1, z1-cover, y1, z1, section=1)
model.patch("rect", 2, 10, 1, -y1, -z1, y1, cover-z1, section=1)
model.patch("rect", 2,  2, 1, -y1, cover-z1, cover-y1, z1-cover, section=1)
model.patch("rect", 2,  2, 1,  y1-cover, cover-z1, y1, z1-cover, section=1)
# Create the reinforcing fibers (left, middle, right, section=1)
model.layer("straight", 3, 3, As, y1-cover, z1-cover, y1-cover, cover-z1, section=1)
model.layer("straight", 3, 2, As, 0.0, z1-cover, 0.0, cover-z1, section=1)
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

# Define gravity loads
# --------------------
# Set a parameter for the axial load
P = 180.0;                # 10% of axial capacity of columns

# create a Linear TimeSeries (load factor varies linearly with time) - command: timeSeries Linear $tag
model.timeSeries("Linear", 1)

# create a Plain load pattern - command: pattern Plain $tag $timeSeriesTag { $loads }
model.pattern("Plain", 1, 1, "-fact", 1.0)

# create the nodal load - command: load nodeID xForce yForce zMoment
model.load(3, 0.0, -P, 0.0)
model.load(4, 0.0, -P, 0.0)

# print model
model.print("-JSON", "-file", "Example3.1.json")

# ------------------------------
# End of model generation
# ------------------------------


# ------------------------------
# Start of analysis generation
# ------------------------------

# create the system of equation
model.system("BandGeneral")

# Create the DOF numberer, the reverse Cuthill-McKee algorithm
model.numberer("RCM")

# Create the constraint handler, a Plain handler is used as homo constraints
model.constraints("Plain")

# Create the convergence test, the norm of the residual with a tolerance of 
# 1e-12 and a max number of iterations of 10
model.test("NormDispIncr", 1.0E-12, 10, 3)

# create the solution algorithm, a Newton-Raphson algorithm
model.algorithm("Newton")

# create the integration scheme, the LoadControl scheme using steps of 0.1
model.integrator("LoadControl", 0.1)

# create the analysis object 
model.analysis("Static")

# ------------------------------
# End of analysis generation
# ------------------------------


# ------------------------------
# Finally perform the analysis
# ------------------------------

# perform the gravity load analysis, requires 10 steps to reach the load level
model.analyze(10)

# Print out the state of nodes 3 and 4
model.print("node", 3, 4)

# Print out the state of element 1
model.print("ele", 1)

