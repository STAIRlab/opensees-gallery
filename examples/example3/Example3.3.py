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
# Written: GLF/MHS/fmk
# Date: January 2001
from math import cos,sin,sqrt,pi
import opensees.openseespy as ops

#
# source Example3.1.tcl
# print("... Gravity load analysis completed")
#

def dynamic_analysis(model):

  # ----------------------------------------------------
  # Start of additional modeling for dynamic loads
  # ----------------------------------------------------

  # Set the gravity loads to be constant & reset the time in the domain
  model.loadConst(time=0.0)


  # Define nodal mass in terms of axial load on columns
  g = 386.4
  P = 180
  m = P/g;

  #         tag  MX  MY   RZ
  model.mass( 3,  m,  m,   0)
  model.mass( 4,  m,  m,   0)



  outFile = "out/ARL360.in"


  # Set time series to be passed to uniform excitation
  model.timeSeries('Path', 1 filePath=outFile,  dt=dt,  factor=g)


  # Create UniformExcitation load pattern
  #                                 tag  dir 
  model.pattern("UniformExcitation",  2   1  accel=1)


  # set the rayleigh damping factors for nodes & elements
  model.rayleigh(0.0 0.0 0.0 0.000625)

  # ---------------------------------------------------------
  # Start of modifications to analysis for transient analysis
  # ---------------------------------------------------------

  # Delete the old analysis and all it's component objects
  model.wipeAnalysis()


  model.system('BandGeneral')


  model.constraints('Plain')

  # Create the convergence test, the norm of the residual with a tolerance of 
  # 1e-12 and a max number of iterations of 10
  model.test('NormDispIncr', 1.0e-12, 10 )


  model.algorithm('Newton')


  model.numberer('RCM')


  # Create the integration scheme, the Newmark with alpha =0.5 and beta =.25
  model.integrator('Newmark',  0.5  0.25 )


  model.analysis('Transient')




  model.recorder('EnvelopeNode', time=True, file='out)/disp.out', node=[3 4 ], dof=1,  disp
  model.recorder('EnvelopeNode', time=True, file='out)/accel.out', timeSeries=1,  node=[3 4 ], dof=1,  accel



  model.recorder('Element', time=True, file='out)/ele1secForce.out', ele=1, section=[1 ], force
  model.recorder('Element', time=True, file='out)/ele1secDef.out',   ele=1, section=[1 ], deformation



  # ------------------------------
  # Finally perform the analysis
  # ------------------------------



  print("... eigen values at start of transient: [eigen 2]")



  tFinal =  1560 * 0.02
  tCurrent = 2
  status = 0

  step = 0.01
  while  status == 0  and  tCurrent < tFinal:

    status = model.analyze(1, step)

    if status != 0:
        print("... Newton failed, trying initial stiffness")
        model.test('NormDispIncr', 1.0e-12  100 0)
        model.algorithm('ModifiedNewton', initial=True)
        status = model.analyze(1, step)
        if status == 0:
          print("... that worked, back to regular Newton")

        model.test('NormDispIncr', 1.0e-12  10 )
        model.algorithm('Newton')

    tCurrent = 2


  return status


source, 'portal.tcl'

wipe

create_portal

gravity_analysis

dynamic_analysis

# Print a message to indicate if analysis successful or not
if status == 0:
   print("Transient analysis completed SUCCESSFULLY")
else:
   print("Transient analysis completed FAILED")

# Perform an eigenvalue analysis
print("... eigen values at end of transient: [eigen 2]")

# Print state of node 3
print, 'node', 3

