# OpenSees -- Open System for Earthquake Engineering Simulation
#
# Portal Frame Example 3.2
# ------------------------
#  Reinforced concrete one-bay, one-story frame
#  Distributed vertical load on girder
#  Lateral Load at top of frame
#
# Example Objectives
# -----------------
#  Nonlinear pushover analysis using Portal Frame Example 3.1 as starting point
# 
#
# Written: Andreas Schellenberg (andreas.schellenberg@gmail.com)
# Date: June 2017

# import the OpenSees Python module
from portal import portal_frame

# ----------------------------------------------------
# Start of Model Generation & Initial Gravity Analysis
# ----------------------------------------------------

# create ModelBuilder (with two-dimensions and 3 DOF/node)
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

# Create the system of equation
model.system("BandGeneral")

# Create the constraint handler, a Plain handler is used as homo constraints
model.constraints("Plain")

# create the convergence test, the norm of the residual with a tolerance of 
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

model.print("Gravity load analysis completed\n")

# Set the gravity loads to be constant & reset the time in the domain
model.loadConst("-time", 0.0)

# ----------------------------------------------------
# End of Model Generation & Initial Gravity Analysis
# ----------------------------------------------------


# ----------------------------------------------------
# Start of additional modelling for lateral loads
# ----------------------------------------------------

# Define lateral loads
# --------------------
# Set some parameters
H = 10.0;		# Reference lateral load

# Set lateral load pattern with a Linear TimeSeries
model.pattern("Plain", 2, 1, "-fact", 1.0)

# create the nodal load - command: load nodeID xForce yForce zMoment
model.load(3, H, 0.0, 0.0)
model.load(4, H, 0.0, 0.0)

# ----------------------------------------------------
# End of additional modelling for lateral loads
# ----------------------------------------------------



# ----------------------------------------------------
# Start of modifications to analysis for push over
# ----------------------------------------------------

# Set some parameters
dU = 0.1;	        # Displacement increment

# Change the integration scheme to be displacement control
#                                    node dof init Jd min max
model.integrator("DisplacementControl", 3, 1, dU, 1, dU, dU)

# ----------------------------------------------------
# End of modifications to analysis for push over
# ----------------------------------------------------


# ------------------------------
# Start of recorder generation
# ------------------------------

# Create a recorder to monitor nodal displacements
model.recorder("Node", "-file", "node32.out", "-time", "-node", 3, 4, "-dof", 1, 2, 3, "disp")
#recorder plot node32.out hi 10 10 300 300 -columns 2 1

# Create a recorder to monitor element forces in columns
model.recorder("EnvelopeElement", "-file", "ele32.out", "-time", "-ele", 1, 2, "localForce")

# --------------------------------
# End of recorder generation
# --------------------------------


# ------------------------------
# Finally perform the analysis
# ------------------------------

# record once at time 0
model.record()

# Set some parameters
maxU = 15.0;	        # Max displacement
numSteps = int(maxU/dU)

# Perform the analysis
ok = model.analyze(numSteps)

if (ok != 0):

    currentDisp = model.nodeDisp(3, 1)
    ok = 0
    while (ok == 0) and (currentDisp < maxU):

        ok = model.analyze(1)

        # if the analysis fails try initial tangent iteration
        if (ok != 0):
            print("regular newton failed .. lets try an initial stiffness for this step")
            model.test("NormDispIncr", 1.0E-12, 1000)
            model.algorithm("ModifiedNewton", "-initial")
            ok = model.analyze(1)
            if ok == 0:
                print("that worked .. back to regular newton")
            model.test("NormDispIncr", 1.0E-12, 10)
            model.algorithm("Newton")

        currentDisp = model.nodeDisp(3, 1)

# Print a message to indicate if analysis successful or not
if ok == 0:
    print("\nPushover analysis completed SUCCESSFULLY\n")
else:
    print("\nPushover analysis FAILED\n")

# Print the state at node 3
model.print("node", 3)

