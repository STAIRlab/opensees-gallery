# OpenSees -- Open System for Earthquake Engineering Simulation
# Pacific Earthquake Engineering Research Center
# http://opensees.berkeley.edu/
#
# Portal Frame Example 3.3
# ------------------------
#  Reinforced concrete one-bay, one-story frame
#  Distributed vertical load on girder
#  Uniform excitation acting at fixed nodes in horizontal direction
#  
# 
# Example Objectives
# -----------------
#  Nonlinear dynamic analysis using Portal Frame Example 1 as staring point
#  Using Tcl Procedures 
#
# 
# Units: kips, in, sec
#
# Written: Andreas Schellenberg (andreas.schellenberg@gmail.com)
# Date: June 2017

# import the OpenSees Python module
from portal import portal_frame
import math

g = 386
# ----------------------------------------------------
# Start of Model Generation & Initial Gravity Analysis
# ----------------------------------------------------
model = portal_frame()

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

# ------------------------------
# End of model generation
# ------------------------------


# ------------------------------
# Start of analysis generation
# ------------------------------

# create the system of equation
model.system("BandGeneral")

# create the DOF numberer, the reverse Cuthill-McKee algorithm
model.numberer("RCM")

# create the constraint handler, a Plain handler is used as homo constraints
model.constraints("Transformation")

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

print("Gravity load analysis completed\n")

# Set the gravity loads to be constant & reset the time in the domain
model.loadConst("-time", 0.0)

# ----------------------------------------------------
# End of Model Generation & Initial Gravity Analysis
# ----------------------------------------------------


# ----------------------------------------------------
# Start of additional modeling for dynamic loads
# ----------------------------------------------------

# Define nodal mass in terms of axial load on columns
m = P/g

#       tag MX MY RZ
model.mass(3, m, m, 0.0)
model.mass(4, m, m, 0.0)

# Define dynamic loads
# --------------------
# Set some parameters
gmFile = "ARL360.g3"
dt = 0.02

# Set time series to be passed to uniform excitation
model.timeSeries("Path", 2, "-filePath", gmFile, "-dt", dt, "-factor", g)

# Create UniformExcitation load pattern
#                               tag dir        tsTag
model.pattern("UniformExcitation", 2, 1, "-accel", 2)

# Set the rayleigh damping factors for nodes & elements
model.rayleigh(0.0, 0.0, 0.0, 0.000625)

# ----------------------------------------------------
# End of additional modeling for dynamic loads
# ----------------------------------------------------


# ---------------------------------------------------------
# Start of modifications to analysis for transient analysis
# ---------------------------------------------------------

# delete the old analysis and all its component objects
model.wipeAnalysis()

# create the system of equation, a banded general storage scheme
model.system("BandGeneral")

# create the DOF numberer, the reverse Cuthill-McKee algorithm
model.numberer("RCM")

# create the constraint handler, a plain handler as homogeneous boundary
model.constraints("Plain")

# create the convergence test, the norm of the residual with a tolerance of 
# 1e-12 and a max number of iterations of 10
model.test("NormDispIncr", 1.0e-12, 10)

# create the solution algorithm, a Newton-Raphson algorithm
model.algorithm("Newton")

# create the integration scheme, the Newmark with gamma=0.5 and beta=0.25
model.integrator("Newmark", 0.5, 0.25)

# create the analysis object 
model.analysis("Transient")

# ---------------------------------------------------------
# End of modifications to analysis for transient analysis
# ---------------------------------------------------------


# ------------------------------
# Start of recorder generation
# ------------------------------

# Create a recorder to monitor nodal displacements
model.recorder("Node", "-time", "-file", "disp.out", "-node", 3, 4, "-dof", 1, 2, 3, "disp")
model.recorder("Node", "-time", "-file", "accel.out", "-node", 3, 4, "-dof", 1, 2, 3, "accel")
model.recorder("Node", "-time", "-file", "totAccel.out", "-timeSeries", 2, 0, 0, "-node", 3, 4, "-dof", 1, 2, 3, "accel")

# Create recorders to monitor section forces and deformations
# at the base of the left column
model.recorder("Element", "-time", "-file", "ele1secForce.out", "-ele", 1, "section", 1, "force")
model.recorder("Element", "-time", "-file", "ele1secDef.out", "-ele", 1, "section", 1, "deformation")

# --------------------------------
# End of recorder generation
# ---------------------------------


# ------------------------------
# Finally perform the analysis
# ------------------------------

# record once at time 0
model.record()

# Perform an eigenvalue analysis
lam = model.eigen(2)
Tstart = 2.0*math.pi/math.sqrt(lam[0])
print("Fundamental period at start of transient analysis: ", Tstart, "sec\n")

# set some variables
tFinal = 2000 * 0.01
tCurrent = model.getTime()
ok = 0

# Perform the transient analysis
while (ok == 0) and (tCurrent < tFinal):
    ok = model.analyze(1, 0.01)

    # If the analysis fails try initial tangent iteration
    if ok != 0:
        print("regular newton failed .. lets try an initial stiffness for this step")
        model.test("NormDispIncr", 1.0e-12, 100, 0)
        model.algorithm("ModifiedNewton", "-initial")
        ok = model.analyze(1, 0.01)

        if ok == 0:
            print("that worked .. back to regular newton")

        model.test("NormDispIncr", 1.0e-12, 10)
        model.algorithm("Newton")

    tCurrent = model.getTime()

# Print a message to indicate if analysis successful or not
if ok == 0:
    print("\nTransient analysis completed SUCCESSFULLY\n")
else:
    print("\nTransient analysis FAILED\n")

# Perform an eigenvalue analysis
lam = model.eigen(2)
Tend = 2.0*math.pi/math.sqrt(lam[0])
print("Fundamental period at end of transient analysis: ", Tend, "sec")

# Print state of node 3
model.print("node", 3)

