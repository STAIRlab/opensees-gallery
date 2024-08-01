# The following codes construct Example 4.2 in Du and Hajjar (2021). The
# libraries can be found from the OpenSeesWiki. The definition of the angle
# section (L3x2x0_25.tcl) is not provided here, but the mesh information is
# shown in the following Python code. Note that in order for clarity the mesh
# here is coarser than that used in Du and Hajjar (2021).

# --------------------------------------------------------------------------------------------------
# 3D Steel L-section beam subjected to compressive load on shear center
# Xinlong Du, 9/25/2019
# Mixed beam-column element for asymmetric sections
# --------------------------------------------------------------------------------------------------
set systemTime [clock seconds]
puts "Starting Analysis: [clock format $systemTime -format "%d-%b-%Y %H:%M:%S"]"
set startTime [clock clicks -milliseconds];
# SET UP ----------------------------------------------------------------------------
wipe;                             # clear memory of all past model definitions
model BasicBuilder -ndm 3 -ndf 6; # Define the model builder, ndm=#dimension, ndf=#dofs
set dataDir Data;                 # set up name of data directory
file mkdir $dataDir;                      # create data directory
source LibUnits.tcl;                      # define units

# define GEOMETRY ------------------------------------------------------------------
#Nodes, NodeNumber, xCoord, yCoord, zCoord
for {set i 1} {$i<8} {incr i 1} {
      node $i [expr -9.2+9.2*$i] 0 0;
}
# ------ define boundary conditions
# NodeID,dispX,dispY,dispZ,rotX,RotY,RotZ
fix 1  1 1 1 1 1 1;
set StartNode 1;
set EndNode 7;
# Define  SECTIONS -------------------------------------------------------------
set ColSecTag 1
# define MATERIAL properties
set nu 0.3;
set Es [expr 27910.0*$ksi];               # Steel Young's Modulus
set Gs [expr $Es/2./[expr 1+$nu]];  # Torsional stiffness Modulus
set matID 1
uniaxialMaterial Elastic $matID $Es;
set J  [expr  0.02473958*$in4]
set GJ [expr $Gs*$J]
set z0 [expr 0.64625474*$in];
set y0 [expr -0.68720012*$in];
source L3x2x0_25.tcl;
# define ELEMENTS-----------------------------------------------------------------------------------------------
set IDColTransf 1; # all members
set ColTransfType Corotational;           # options for columns: Linear PDelta Corotational
geomTransf $ColTransfType  $IDColTransf 0 0 1;    #define geometric transformation: performs a corotational geometric transformation
set numIntgrPts 2;        # number of Gauss integration points
for {set i 1} {$i<$EndNode} {incr i 1} {
  set elemID $i
  set nodeI $i
  set nodeJ [expr $i+1]
  element mixedBeamColumnAsym $elemID $nodeI $nodeJ $numIntgrPts $ColSecTag $IDColTransf -shearCenter $y0 $z0;
}

# Define RECORDERS -------------------------------------------------------------
recorder Node -file $dataDir/DispMB6.out -time -node $EndNode -dof 1 2 3 4 5 6 disp;                      # displacements of middle node
recorder Node -file $dataDir/ReacMB6.out -time -node $StartNode -dof 1 2 3 4 5 6 reaction;                # support reaction


# define Load-------------------------------------------------------------
set N 15.0;
pattern Plain 2 Linear {
  # NodeID, Fx, Fy, Fz, Mx, My, Mz
  load $EndNode -$N 0 0 0 0 0;
}

# define ANALYSIS PARAMETERS------------------------------------------------------------------------------------
constraints Plain; # how it handles boundary conditions
numberer Plain;      # renumber dof's to minimize band-width
system BandGeneral;# how to store and solve the system of equations in the analysis
test NormDispIncr 1.0e-08 1000; # determine if convergence has been achieved at the end of an iteration step
#algorithm NewtonLineSearch;# use Newton's solution algorithm: updates tangent stiffness at every iteration
algorithm Newton;
set Dincr -0.01;
                               #Node,  dof, 1st incr, Jd, min,   max
integrator DisplacementControl $EndNode 1   $Dincr     1  $Dincr -0.01;
analysis Static   ;# define type of analysis static or transient
analyze 7000;
puts "Finished"
#--------------------------------------------------------------------------------
set finishTime [clock clicks -milliseconds];
puts "Time taken: [expr ($finishTime-$startTime)/1000] sec"
set systemTime [clock seconds]
puts "Finished Analysis: [clock format $systemTime -format "%d-%b-%Y %H:%M:%S"]"

