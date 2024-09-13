# OpenSees -- Open System for Earthquake Engineering Simulation
# Pacific Earthquake Engineering Research Center
# http://opensees.berkeley.edu/
#
# Example 8: Cantilever Beam
# --------------------------
# Cantilever beam modeled with three dimensional brick elements
# 
# Example Objectives
# ------------------
# - test different brick elements
# - free vibration analysis starting from static deflection
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

# create ModelBuilder (with three-dimensions and 3 DOF/node)
model = ops.Model(ndm=3, ndf=3)

# set default units
# defaultUnits("-force", "kip", "-length", "in", "-time", "sec", "-temp", "F")

# Define the material
# -------------------
#                               matTag  E     nu   rho
model.nDMaterial("ElasticIsotropic", 1, 100.0, 0.25, 1.27)

# Define geometry
# ---------------
Brick = "stdBrick"
#Brick = "bbarBrick"
#Brick = "SSPbrick"

nz = 6
nx = 2
ny = 2

nn = int((nz+1)*(nx+1)*(ny+1))

# mesh generation
#          numX numY numZ startNode startEle eleType eleArgs? coords?
model.block3D(nx, ny, nz, 1, 1, Brick, 1, {
              1: [-1.0, -1.0,  0.0],
              2: [ 1.0, -1.0,  0.0],
              3: [ 1.0,  1.0,  0.0],
              4: [-1.0,  1.0,  0.0],
              5: [-1.0, -1.0, 10.0],
              6: [ 1.0, -1.0, 10.0],
              7: [ 1.0,  1.0, 10.0],
              8: [-1.0,  1.0, 10.0]})

# boundary conditions
model.fixZ(0.0, (1, 1, 1))

#
# Define point load (2 steps)
#

# 1) First we create a "Plain" load pattern which serves as a
#    container for the loads. The "Linear" argument prescribes
#    a linear time series which describes how the loading scales 
#    over pseudo time
p = 0.10
model.pattern("Plain", 1, "Linear")

# 2) Finally, create the nodal load and assign it to the
#    pattern we just created
model.load(nn, p, p, 0.0, pattern=1)

# ----------------------- 
# End of model generation
# -----------------------


# ------------------------
# Start of static analysis
# ------------------------

# Load control with variable load steps
#                            init  Jd  min   max
model.integrator("LoadControl", 1.0, 1)

# Convergence test
#                     tolerance maxIter displayCode
model.test("NormUnbalance", 1.0E-10, 20, 0)

# Solution algorithm
model.algorithm("Newton")

# DOF numberer
model.numberer("RCM")

# Constraint handler
model.constraints("Plain")

# System of equations solver
model.system("ProfileSPD")

# Analysis for gravity load
model.analysis("Static")

# Perform the analysis
model.analyze(5)

# --------------------------
# End of static analysis
# --------------------------


# ----------------------------
# Start of recorder generation
# ----------------------------

model.recorder("Node", "-file", "Node.out", "-time", "-node", nn, "-dof", 1, "disp")
model.recorder("Element", "-file", "Elem.out", "-time", "-eleRange", 1, 10, "material", "1", "strains")
#recorder("plot", "Node.out", "CenterNodeDisp", 625, 10, 625, 450, "-columns", 1, 2)

# --------------------------
# End of recorder generation
# --------------------------


# ---------------------------------------
# Create and Perform the dynamic analysis
# ---------------------------------------

# Remove the static analysis & reset the time to 0.0
model.wipeAnalysis()
model.setTime(0.0)

# Now remove the loads and let the beam vibrate
model.remove("loadPattern", 1)

# add some mass proportional damping
model.rayleigh(0.01, 0.0, 0.0, 0.0)

# Create the transient analysis
model.test("EnergyIncr", 1.0E-10, 20, 0)
model.algorithm("Newton")
model.numberer("RCM")
model.constraints("Plain")
model.system("ProfileSPD")
model.integrator("Newmark", 0.5, 0.25)
model.analysis("Transient")

# record once at time 0
model.record()

# Perform the transient analysis (20 sec)
#         numSteps dt
model.analyze(1000, 1.0)

