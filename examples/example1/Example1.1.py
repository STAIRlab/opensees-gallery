# OpenSees -- Open System for Earthquake Engineering Simulation
# Pacific Earthquake Engineering Research Center
# http://opensees.berkeley.edu/
#
# Basic Truss Example 1.1
# -----------------------
#  2d 3 Element Elastic Truss
#  Single Nodal Load, Static Analysis
#
#
# Written: Andreas Schellenberg (andreas.schellenberg@gmail.com)
# Date: June 2017
#
# import the OpenSeesPy Compatiblity module.
# This module contains a private global variable
# that encapsulates an instance of TclRuntime
import opensees.openseespy as ops

# ------------------------------
# Start of model generation
# ------------------------------

# Create a Model (with two-dimensions and 2 DOF/node)
model = ops.Model("BasicBuilder", "-ndm", 2, "-ndf", 2)

# Create nodes - command: node nodeId xCrd yCrd
model.node(1, 0.0,    0.0)
model.node(2, 144.0,  0.0)
model.node(3, 168.0,  0.0)
model.node(4,  72.0, 96.0)

# set the boundary conditions - command: fix nodeID xRestrnt? yRestrnt?
model.fix(1, 1, 1)
model.fix(2, 1, 1)
model.fix(3, 1, 1)

# Define materials for truss elements
# -----------------------------------
# Create Elastic material prototype - command: uniaxialMaterial Elastic matID E
model.uniaxialMaterial("Elastic", 1, 3000.0)

# Define elements
# ---------------
# Create truss elements - command: element truss trussID node1 node2 A matID
model.element("truss", 1, 1, 4, 10.0, 1)
model.element("truss", 2, 2, 4,  5.0, 1)
model.element("truss", 3, 3, 4,  5.0, 1)

# Define loads
# ------------
# create a Linear TimeSeries (load factor varies linearly with time) - command: timeSeries Linear $tag
model.timeSeries("Linear", 1)

# create a Plain load pattern - command: pattern Plain $tag $timeSeriesTag { $loads }
model.pattern("Plain", 1, 1, "-fact", 1.0)
# create the nodal load 
#       nodeID xForce yForce
model.load(4, 100.0, -50.0, pattern=1)

# print model

model.printModel("-JSON", file="Example1.1.json")

# ------------------------------
# End of model generation
# ------------------------------


# ------------------------------
# Start of analysis generation
# ------------------------------

# create the system of equation, a SPD using a band storage scheme
model.system("BandSPD")

# create the DOF numberer, the reverse Cuthill-McKee algorithm
model.numberer("RCM")

# create the constraint handler, a Plain handler is used as homo constraints
model.constraints("Plain")

# create the solution algorithm, a Linear algorithm is created
model.algorithm("Linear")

# create the integration scheme, the LoadControl scheme using steps of 1.0
model.integrator("LoadControl", 1.0)

# create the analysis object 
model.analysis("Static")

# ------------------------------
# End of analysis generation
# ------------------------------


# ------------------------------
# Start of recorder generation
# ------------------------------

# create a Recorder object for the nodal displacements at node 4
model.recorder("Node", "-file", "example.out", "-time", "-node", 4, "-dof", 1, 2, "disp")

# create a recorder for element forces, one in global and the other local system
model.recorder("Element", "-file", "eleGlobal.out", "-time", "-ele", 1, 2, 3, "forces")
model.recorder("Element", "-file", "eleLocal.out", "-time", "-ele", 1, 2, 3, "basicForces")

# ------------------------------
# End of recorder generation
# ------------------------------


# ------------------------------
# Finally perform the analysis
# ------------------------------

# perform the analysis
model.analyze(1)


# ------------------------------
# Print Stuff to Screen
# ------------------------------

# print the current state at node 4 and at all elements
#print("node 4 displacement: ", nodeDisp(4))
model.printModel("node", 4)
model.printModel("ele")

