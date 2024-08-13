# ===----------------------------------------------------------------------===//
# 
#         OpenSees - Open System for Earthquake Engineering Simulation    
#                Structural Artificial Intelligence Laboratory
#                          stairlab.berkeley.edu
# 
# ===----------------------------------------------------------------------===//
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
# Written: GLF/MHS/fmk/cmp
# Date: January 2001



proc create_portal {} {

  # Set parameters for overall model geometry
  set width    360
  set height   144

  # Create ModelBuilder (with two-dimensions and 3 DOF/node)
  model basic -ndm 3 -ndf 6

  # Create nodes
  # ------------

  # Create nodes
  #    tag        X       Y     Z
  node  1       0.0     0.0   0.0
  node  2    $width     0.0   0.0
  node  3       0.0 $height   0.0
  node  4    $width $height   0.0


  # Fix supports at base of columns
  #    tag   DX   DY  DZ   RX  RY   RZ
  fix   1     1    1   1    1   1    1
  fix   2     1    1   1    1   1    1


  # Define materials for nonlinear columns
  # ------------------------------------------
  # CONCRETE                  tag  f'c     ec0   f'cu      ecu
  # Core concrete (confined)
  uniaxialMaterial Concrete01  1  -6.0  -0.004   -5.0   -0.014

  # Cover concrete (unconfined)
  uniaxialMaterial Concrete01  2  -5.0  -0.002    0.0   -0.006

  # STEEL
  # Reinforcing steel 
  pset fy 60.0;      # Yield stress
  pset E 30000.0;    # Young's modulus
  #                        tag  fy  E0     b
  uniaxialMaterial Steel01  3  $fy  $E  0.01

  # Define cross-section for nonlinear columns
  # ------------------------------------------

  # set some parameters
  set colWidth 15
  set colDepth 24 

  set cover  1.5
  set As    0.60;     # area of no. 7 bars

  # some variables derived from the parameters
  set y1 [expr $colDepth/2.0]
  set z1 [expr $colWidth/2.0]

  section Fiber 1 -GJ 1e5 {
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
  geomTransf PDelta 1   0 0 1

  # Number of integration points along length of element
  set np 5
  # Create the coulumns using Beam-column elements
  #       element  tag ndI ndJ nsecs secID transfTag
  global argv
  set elem_type [lindex $argv 1]; #forceBeamColumn ; # ForceFrame
  puts $elem_type
  element $elem_type  1   1   3   $np    1       1 
  element $elem_type  2   2   4   $np    1       1 

  # Define girder element
  # -----------------------------

  # Geometry of column elements
  #                tag 
  geomTransf Linear 2   0 0 1

  # Create the beam element
  #                          tag ndI ndJ     A       E    Iz  Iy     G   J    transfTag
  element elasticBeamColumn   3   3   4    360    4030  8640 9000   4e3 1e4       2

  # Define gravity loads
  # --------------------

  # Set a parameter for the axial load
  set P 180;                # 10% of axial capacity of columns

  # Create a Plain load pattern with a Linear TimeSeries
  pattern Plain 1 "Linear" {
        # Create nodal loads at nodes 3 & 4
        #    nd    FX          FY   Fz             MZ 
        load  3   0.0  [expr -$P]  0.0  0.0  0.0  0.0
        load  4   0.0  [expr -$P]  0.0  0.0  0.0  0.0
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


  # ------------------------------
  # Start of recorder generation
  # ------------------------------

  # Create a recorder to monitor nodal displacements
  #recorder Node -xml nodeGravity.out -time -node 3 4 -dof 1 2 3 disp
  #recorder Element -file ele.out -ele 1 section  forces


  # ------------------------------
  # Finally perform the analysis
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
        #    node   Fx   Fy  Fz    Mx  My  Mz
        load   3    $H  0.0 0.0   0.0 0.0 0.0 
        load   4    $H  0.0 0.0   0.0 0.0 0.0 
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
  # remove recorders

  # Create a recorder to monitor nodal displacements
  recorder Node -file out/node32.out -time -node 3 4 -dof 1 2 3 disp
  #recorder plot node32.out hi 10 10 300 300 -columns 2 1

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



#
# Main
#
create_portal

# Apply gravity loads and run static analysis
set status [gravity_analysis]
if {$status == 0} {
    puts "\nGravity analysis completed SUCCESSFULLY";
} else {
    puts "\nGravity analysis FAILED";    
}

# Print the state at node 3
print node 3

#return $status


# Apply lateral loads and run static analysis
set status [pushover_analysis]
if {$status == 0} {
    puts "\nPushover analysis completed SUCCESSFULLY";
} else {
    puts "\nPushover analysis FAILED";    
}

# Print the state at node 3
print node 3

return $status

