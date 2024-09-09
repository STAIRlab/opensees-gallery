# ===----------------------------------------------------------------------===//
# 
#         OpenSees - Open System for Earthquake Engineering Simulation    
#                Structural Artificial Intelligence Laboratory
# 
# ===----------------------------------------------------------------------===//
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


# ----------------------------------------------------
# Start of Model Generation & Initial Gravity Analysis
# ----------------------------------------------------

# # Do operations of Example3.1 by sourcing in the tcl file
# source Example3.1.tcl
# puts "... Gravity load analysis completed"
# # ----------------------------------------------------
# # End of Model Generation & Initial Gravity Analysis
# # ----------------------------------------------------

proc dynamic_analysis {} {
  # ----------------------------------------------------
  # Start of additional modeling for dynamic loads
  # ----------------------------------------------------

  # Set the gravity loads to be constant & reset the time in the domain
  loadConst -time 0.0


  # Define nodal mass in terms of axial load on columns
  set g 386.4
  set P 180
  set m [expr $P/$g];       # expr command to evaluate an expression

  #    tag   MX   MY   RZ
  mass  3    $m   $m    0
  mass  4    $m   $m    0


  # Define dynamic loads
  # --------------------

  # Set some parameters
  file mkdir out
  set outFile "out/ARL360.in"

  # Source in TCL proc to read PEER SMD record
  source "ReadSMDFile.tcl"

  # Permform the conversion from SMD record to OpenSees record
  #              inFile     outFile dt
  ReadSMDFile "elCentro.AT2" $outFile dt

  # Set time series to be passed to uniform excitation
  timeSeries Path 1 -filePath $outFile -dt $dt -factor $g
  #set accelSeries "Path -filePath $outFile -dt $dt -factor $g"

  # Create UniformExcitation load pattern
  #                         tag dir 
  pattern UniformExcitation  2   1  -accel 1

  # set the rayleigh damping factors for nodes & elements
  rayleigh 0.0 0.0 0.0 0.000625

  # ----------------------------------------------------
  # End of additional modeling for dynamic loads
  # ----------------------------------------------------


  # ---------------------------------------------------------
  # Start of modifications to analysis for transient analysis
  # ---------------------------------------------------------

  # Delete the old analysis and all it's component objects
  wipeAnalysis

  # Create the system of equation, a banded general storage scheme
  system BandGeneral

  # Create the constraint handler, a plain handler as homogeneous boundary
  constraints Plain

  # Create the convergence test, the norm of the residual with a tolerance of 
  # 1e-12 and a max number of iterations of 10
  test NormDispIncr 1.0e-12  10 

  # Create the solution algorithm, a Newton-Raphson algorithm
  algorithm Newton

  # Create the DOF numberer, the reverse Cuthill-McKee algorithm
  numberer RCM

  # Create the integration scheme, the Newmark with alpha =0.5 and beta =.25
  integrator Newmark  0.5  0.25 

  # Create the analysis object
  analysis Transient

  # ---------------------------------------------------------
  # End of modifications to analysis for transient analysis
  # ---------------------------------------------------------


  # ------------------------------
  # Start of recorder generation
  # ------------------------------

  # Create a recorder to monitor nodal displacements
  recorder EnvelopeNode -time -file out/disp.out -node 3 4 -dof 1 disp
  recorder EnvelopeNode -time -file out/accel.out -timeSeries 1 -node 3 4 -dof 1 accel

  # Create recorders to monitor section forces and deformations
  # at the base of the left column
  recorder Element -time -file out/ele1secForce.out -ele 1 section 1 force
  recorder Element -time -file out/ele1secDef.out   -ele 1 section 1 deformation

  # --------------------------------
  # End of recorder generation
  # ---------------------------------


  # ------------------------------
  # Finally perform the analysis
  # ------------------------------

  # Perform an eigenvalue analysis
  puts "... eigen values at start of transient: [eigen 2]"


  # set some variables
  set tFinal [expr 1560 * 0.02]
  set tCurrent [getTime]
  set status 0

  # Perform the transient analysis
  while {$status == 0 && $tCurrent < $tFinal} {
    
    set status [analyze 1 .01]
    
    # if the analysis fails try initial tangent iteration
    if {$status != 0} {
        puts "... Newton failed, trying initial stiffness"
        test NormDispIncr 1.0e-12  100 0
        algorithm ModifiedNewton -initial
        set status [analyze 1 .01]
        if {$status == 0} {
          puts "... that worked, back to regular Newton"
        }
        test NormDispIncr 1.0e-12  10 
        algorithm Newton
    }
    
    set tCurrent [getTime]
  }

  return $status
}

source portal.tcl

wipe

create_portal

gravity_analysis

dynamic_analysis

# Print a message to indicate if analysis successful or not
if {$status == 0} {
   puts "Transient analysis completed SUCCESSFULLY";
} else {
   puts "Transient analysis completed FAILED";    
}
# Perform an eigenvalue analysis
puts "... eigen values at end of transient: [eigen 2]"

# Print state of node 3
print node 3

