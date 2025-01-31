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
# -----------------
#  Nonlinear beam-column elements
#  Gravity load analysis and eigenvalue analysis
#
# 
# Units: kips, in, sec
#
# Written: GLF/MHS/fmk
# Date: January 2001

# ------------------------------
# Start of model generation
# ------------------------------

# Create ModelBuilder (with two-dimensions and 3 DOF/node)

proc create_portal {} {
  wipe

  # Set parameters for overall model geometry
  set width    360
  set height   144
  model basic -ndm 2 -ndf 3

  # Create nodes
  # ------------

  # Create nodes
  #    tag        X       Y 
  node  1       0.0     0.0 
  node  2    $width     0.0 
  node  3       0.0 $height
  node  4    $width $height


  # Fix supports at base of columns
  #    tag   DX   DY   RZ
  fix   1     1    1    1
  fix   2     1    1    1


  # Define materials for nonlinear columns
  # ------------------------------------------
  # CONCRETE                  tag   f'c        ec0   f'cu        ecu
  # Core concrete (confined)
  uniaxialMaterial Concrete01  1  -6.0  -0.004   -5.0     -0.014

  # Cover concrete (unconfined)
  uniaxialMaterial Concrete01  2  -5.0   -0.002   0.0     -0.006

  # STEEL
  # Reinforcing steel 
  pset fy 60.0;      # Yield stress
  pset E 30000.0;    # Young's modulus
  #                        tag  fy E0    b
  uniaxialMaterial Steel01  3  $fy $E  0.01

  # Define cross-section for nonlinear columns
  # ------------------------------------------

  # set some parameters
  set colWidth 15
  set colDepth 24 

  set cover  1.5
  set As     0.6;     # area of no. 7 bars

  # some variables derived from the parameters
  set y1 [expr $colDepth/2.0]
  set z1 [expr $colWidth/2.0]

  section Fiber 1 {
      # Create the concrete core fibers
      patch rect 1 10 1 [expr $cover-$y1] [expr $cover-$z1] [expr $y1-$cover] [expr $z1-$cover]

      # Create the concrete cover fibers (top, bottom, left, right)
      patch rect 2 10 1  [expr -$y1] [expr $z1-$cover] $y1 $z1
      patch rect 2 10 1  [expr -$y1] [expr -$z1] $y1 [expr $cover-$z1]
      patch rect 2  2 1  [expr -$y1] [expr $cover-$z1] [expr $cover-$y1] [expr $z1-$cover]
      patch rect 2  2 1  [expr $y1-$cover] [expr $cover-$z1] $y1 [expr $z1-$cover]

      # Create the reinforcing fibers (left, middle, right)
      layer straight 3 3 $As [expr $y1-$cover] [expr $z1-$cover] [expr $y1-$cover] [expr $cover-$z1]
      layer straight 3 2 $As 0.0 [expr $z1-$cover] 0.0 [expr $cover-$z1]
      layer straight 3 3 $As [expr $cover-$y1] [expr $z1-$cover] [expr $cover-$y1] [expr $cover-$z1]
  }


  # Define column elements
  # ----------------------

  # Geometry of column elements
  #                tag 
  geomTransf PDelta 1  

  # Number of integration points along length of element
  set np 5

  # Create the coulumns using Beam-column elements
  #               e            tag ndI ndJ nsecs secID transfTag
  set eleType forceBeamColumn
  element $eleType  1   1   3   $np    1       1 
  element $eleType  2   2   4   $np    1       1 

  # Define girder element
  # -----------------------------

  # Geometry of column elements
  #                tag 
  geomTransf Linear 2  

  # Create the beam element
  #                          tag ndI ndJ     A       E    Iz   transfTag
  element ElasticBeamColumn   3   3   4    360    4030  8640    2

  # Define gravity loads
  # --------------------

  # Set a parameter for the axial load
  set P 180;                # 10% of axial capacity of columns

  # Create a Plain load pattern with a Linear TimeSeries
  pattern Plain 1 "Linear" {
        # Create nodal loads at nodes 3 & 4
        #    nd    FX          FY  MZ 
        load  3   0.0  [expr -$P] 0.0
        load  4   0.0  [expr -$P] 0.0
  }

}

proc gravity_analysis {} {
  # initialize in case we need to do an initial stiffness iteration
  initialize

  # ------------------------------
  # Start of analysis generation
  # ------------------------------

  # Create the system of equation, a sparse solver with partial pivoting
  system ProfileSPD

  # Create the constraint handler, the transformation method
  constraints Transformation

  # Create the DOF numberer, the reverse Cuthill-McKee algorithm
  numberer RCM

  # Create the convergence test, the norm of the residual with a tolerance of 
  # 1e-12 and a max number of iterations of 10
  test NormDispIncr 1.0e-12  10 ; #0

  # Create the solution algorithm, a Newton-Raphson algorithm
  algorithm Newton

  # Create the integration scheme, the LoadControl scheme using steps of 0.1 
  integrator LoadControl 0.1

  # Create the analysis object
  analysis Static

  # Perform the analysis
  # ------------------------------
  # perform the gravity load analysis, requires 10 steps to reach the load level
  analyze 10

# print ele 1 2 3
}

proc pushover_analysis {} {

  # Define lateral loads
  # --------------------

  # Set the gravity loads to be constant & reset the time in the domain
  loadConst -time 0.0

  # Set some parameters
  set H 10.0;		# Reference lateral load

  # Set lateral load pattern with a Linear TimeSeries
  pattern Plain 2 "Linear" {
        # Create nodal loads at nodes 3 & 4
        #    nd    FX  FY  MZ 
        load 3 $H 0.0 0.0 
        load 4 $H 0.0 0.0 
  }


  # ----------------------------------------------------
  # Configure a pushover analysis
  # ----------------------------------------------------

  # Set some parameters
  set dU 0.1;	        # Displacement increment

  # Change the integration scheme to be displacement control
  #                             node dof init Jd min max
  integrator DisplacementControl  3   1   $dU  1 $dU $dU


  # ------------------------------
  # Create recorders
  # ------------------------------
  # Stop the old recorders by destroying them
  remove recorders

  # Create a recorder to monitor nodal displacements
  recorder Node -file out/node32.out -time -node 3 4 -dof 1 2 3 disp

  # Create a recorder to monitor element forces in columns
  recorder EnvelopeElement -file out/ele32.out -time -ele 1 2 localForce


  # ------------------------------
  # Finally perform the analysis
  # ------------------------------

  # Set some parameters
  set maxU 15.0;	        # Max displacement
  set numSteps [expr int($maxU/$dU)]


  # Perform the analysis
  set status [analyze $numSteps]

  if {$status != 0} {

      set currentDisp [nodeDisp 3 1]
      set status 0
      while {$status == 0 && $currentDisp < $maxU} {

          set status [analyze 1]

          # if the analysis fails try initial tangent iteration
          if {$status != 0} {
              puts "... Newton failed, trying an initial stiffness"
              test NormUnbalance 1.0  1000 5
              algorithm ModifiedNewton -initial
              set status [analyze 1]
              if {$status == 0} {
                puts "... that worked, back to regular newton"
              }
              test NormDispIncr 1.0e-12  10 
              algorithm Newton
          }

          set currentDisp [nodeDisp 3 1]
      }
  }
  return $status
}


proc dynamic_analysis {} {
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

  # ----------------------------------------------------
  # Start of additional modeling for dynamic loads
  # ----------------------------------------------------

  # Set the gravity loads to be constant & reset the time in the domain
  loadConst -time 0.0


  # Define nodal mass in terms of axial load on columns
  set g 386.4
  set P 180.0
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
  # numberer RCM

  # Create the integration scheme, the Newmark with alpha =0.5 and beta =.25
  integrator Newmark  0.5  0.25 

  # Create the analysis object
  analysis Transient

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



# -------------------------------------------------------------------
# Begin main execution
# -------------------------------------------------------------------

create_portal

# Apply gravity loads and run static analysis
set status [gravity_analysis]
if {$status == 0} {
    puts "\nGravity analysis completed SUCCESSFULLY";
} else {
    puts "\nGravity analysis FAILED";    
}

# Print the state at node 3
puts "Node 3 Displacement: [nodeDisp 3]"

# Apply lateral loads and run static analysis
set status [pushover_analysis]
if {$status == 0} {
    puts "\nPushover analysis completed SUCCESSFULLY";
} else {
    puts "\nPushover analysis FAILED";    
}

# Print state of node 3
puts "Node 3 Displacement: [nodeDisp 3]"

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
puts "Node 3 Displacement: [nodeDisp 3]"


return $status

