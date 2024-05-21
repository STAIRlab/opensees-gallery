# PortalFrame: Reinforced concrete one bay frame 
# Distributed vertical load on girder 
# Horizontal load at girder # Linear girder, non-linear columns
#
# Units: kips, in, sec
#
# Written: MHS
# Date: 3 August 1999
#
set ANALYSIS Static
#set ANALYSIS Dynamic
set PUSHOVER LoadControl
#set PUSHOVER DispControl

# Create ModelBuilder
model basic -ndm 3 -ndf 6
# -----
set PI [expr 2*asin(1.0)]
set g 386.4
set hCol 72.0; # Column diameter
set colAspect 4; # Column aspect ratio
set blTocl 1; # Beam length to column length ratio
set biToci 1; # Beam Ig to column Ig ratio
set v 0.05; # Column axial load --> P = v*f'c*Ag
set hBeam 96.0; # Beam depth
set lenCol  [expr $hCol*2*$colAspect]; # Column length
set lenBeam [expr $lenCol*$blTocl]; # Beam length
set fc  -5.5; # Concrete compressive strength
set Ec      [expr 57000*sqrt(-$fc*1000)]; # Elastic concrete modulus (psi)
set Ec      [expr $Ec/1000]; # Elastic concrete modulus (ksi)
set colArea [expr $PI*pow($hCol,2)/4]; # Column cross-section area
set P       [expr $v*$fc*$colArea]; # Column axial load
set m       [expr -$P/$g]; # Beam nodal mass
set cover   [expr $hCol/15]; # Column cover
set rhoCol  0.015; # Column r/f ratio
set numBars 20; # Number of r/f bars in columns
set barArea [expr $rhoCol*$colArea/$numBars]; # r/f bar area
set beamArea $colArea; # Beam cross-section area
set Icol    [expr $PI*pow($hCol,4)/64]; # Column gross second moment of area
set Ibeam   [expr $Icol*$biToci]; # Beam gross second moment of area
set GJ 1.0e12; # Torsional stiffness
# Define uniaxial materials
# CONCRETE tag f'c ec0 f'cu ecu
# Core concrete (confined)
uniaxialMaterial Concrete01 1 [expr 1.26394*$fc] -0.004639 [expr 1.002753*$fc] -0.013667
# Cover concrete (unconfined)
uniaxialMaterial Concrete01 2 $fc -0.003 [expr 0.1*$fc] -0.006
# STEEL
# Reinforcing steel
# tag fy E0 b
uniaxialMaterial Steel01 3 60 30000 0.05
# -----
set lp [expr $lenCol/3]; # Plastic hinge length
# Define nodes
# tag X Y Z
node 1 0.0 0.0 0.0
node 2 $lenBeam 0.0 0.0
node 3 0.0 $lp 0.0
node 4 $lenBeam $lp 0.0
node 5 0.0 [expr $lenCol-$lp] 0.0
node 6 $lenBeam [expr $lenCol-$lp] 0.0
node 7 0.0 $lenCol 0.0
node 8 $lenBeam $lenCol 0.0
# Nodal mass
# node MX MY MZ RX RY RZ
mass 7 $m $m $m 0.0 0.0 0.0
mass 8 $m $m $m 0.0 0.0 0.0
# -----
# Boundary conditions
# node DX DY DZ RX RY RZ
fix 1 1 1 1 1 1 1
fix 2 1 1 1 1 1 1
fix 3 0 0 1 1 1 0
fix 4 0 0 1 1 1 0
fix 5 0 0 1 1 1 0
fix 6 0 0 1 1 1 0
fix 7 0 0 1 1 1 0
fix 8 0 0 1 1 1 0
# -----
# Define column section
set rCol [expr $hCol/2.0]; # Column radius
# Source in procedure to define circular fiber section
source RCcircSection.tcl
# tag ri ro cover coreID coverID steelID num area nfCoreR nfCoreT nfCoverR nfCoverT
RCcircSection 2 0.0 $rCol $cover 1 2 3 $numBars $barArea 8 16 2 10
# Define torsional stiffness and attach it to RC section
uniaxialMaterial Elastic 10 $GJ
# tag uniTag uniCode secTag
section Aggregator 1 10 T -section 2
# -----
set np 4; # Number of integration points
# Define column elements
# tag vecxz
geomTransf Linear 1 0 0 1
# Plastic region
# tag ndI ndJ nsecs secID transfTag
element nonlinearBeamColumn 1 1 3 $np 1 1
element nonlinearBeamColumn 2 2 4 $np 1 1
element nonlinearBeamColumn 5 5 7 $np 1 1
element nonlinearBeamColumn 6 6 8 $np 1 1
# Elastic region
# tag ndI ndJ A E G J Iy Iz transfTag
element elasticBeamColumn 3 3 5 $colArea $Ec $GJ 1.0 $Icol $Icol 1
element elasticBeamColumn 4 4 6 $colArea $Ec $GJ 1.0 $Icol $Icol 1
# Define beam element
# tag vecxz
geomTransf Linear 2 0 0 1
# tag ndI ndJ A E G J Iy Iz transfTag
element elasticBeamColumn 7 7 8 $beamArea $Ec $GJ 1.0 $Ibeam $Ibeam 2
# -----
# Record nodal displacements
recorder Node -file nodeDisp.out disp -time -node 7 8 -dof 1
# Record element forces
recorder Element 1 -time -file ele1Force.out force
recorder Element 2 -time -file ele2Force.out force
# Record section forces and deformations
recorder Element 1 -time -file ele1sec1Force.out section 1 forces
recorder Element 1 -time -file ele1sec1Def.out section 1 deformations
# -----
# Constant gravity load
pattern Plain 1 Constant {
  # FX FY FZ MX MY MZ
  load 7 0.0 $P 0.0 0.0 0.0 0.0
  load 8 0.0 $P 0.0 0.0 0.0 0.0
}
system ProfileSPD
constraints Plain
numberer Plain
# tol max dispCode
test NormUnbalance 1.0e-5 20
algorithm Newton
# Integrator with zero time step for initial gravity analysis
integrator LoadControl 0 1 0 0
analysis Static
analyze 1
# -----
if {$ANALYSIS == "Static"} {
  set H 28.0; # Reference lateral load
  # Set lateral load pattern
  pattern Plain 2 Linear {
    load 7 $H 0.0 0.0 0.0 0.0 0.0
    load 8 $H 0.0 0.0 0.0 0.0 0.0
  }
  if {$PUSHOVER == "LoadControl"} {
    # init Jd min max
    integrator LoadControl 0.2 4 0.1 2.0
    set numSteps 20
    analysis Static
    analyze $numSteps
  } elseif {$PUSHOVER == "DispControl"} {
    set dU 0.1; # Displacement increment
    set maxU 12.0; # Max displacement
    # node dof init Jd min max
    integrator DisplacementControl 7 1 $dU 1 $dU $dU
    set numSteps [expr int($maxU/$dU)]
    analysis Static
    analyze $numSteps
  } else {
    puts stderr "Invalid PUSHOVER option"
  }
} elseif {$ANALYSIS == "Dynamic"} {
  wipeAnalysis
  system BandGeneral
  constraints Plain
  test NormUnbalance 1.0e-5 20
  algorithm Newton
  numberer RCM
  # gamma beta
  integrator Newmark 0.5 0.25
  analysis Transient
  # Source in TCL proc to read PEER SMD record
  source ReadSMDFile.tcl
  set outFile A-e06230.g3
  # inFile outFile dt
  ReadSMDFile A-e06230.at2 $outFile dt
  # Create EQ load pattern
  # tag dir factor file dt
  pattern UniformExcitation 2 1 $g -accel $outFile $dt
  # N dt
  analyze 2000 0.01
} else {
  puts stderr "Invalid ANALYSIS option"
}
