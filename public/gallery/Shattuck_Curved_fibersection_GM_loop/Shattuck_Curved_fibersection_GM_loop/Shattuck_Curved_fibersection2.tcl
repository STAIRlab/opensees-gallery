# --------------------------------------------------------------------------------------------------
# Curved BART aerial structure, located midway between Rockridge and MacArthur Stations 
#
#

# SET UP ----------------------------------------------------------------------------
wipe;				# clear memory of all past model definitions
model BasicBuilder -ndm 3 -ndf 6;	# Define the model builder, ndm=#dimension, ndf=#dofs
set dataDir Data;			# set up name of data directory -- remove
file mkdir $dataDir; 			# create data directory
set GMdir "../GMfiles";		# ground-motion file directory
set ViewScale 0.25;			# scaling factor for viewing deformed shape, it depends on the dimensions of the model
source LibUnits.tcl;			# define units
source DisplayPlane.tcl;		# procedure for displaying a plane in model
source DisplayModel3D.tcl;		# procedure for displaying 3D perspectives of model
source BuildRCrectSection1.tcl;		# procedure for definining RC fiber section

# define GEOMETRY -------------------------------------------------------------

# define NODAL COORDINATES
# Abutment 47
node 471	117302.3244	20222.29524	1601.64;
node 472	117305.0871	20186.01622	1601.64;
node 473	117308.0823	20146.68381	1601.64;
node 474	117318.996	20003.30411	1617.96;
node 475	117321.7585	19967.02785	1617.96;
node 476	117324.7542	19927.68834	1617.96;

# Intermediate nodes Abutment 47 - Pier 48
node 111	117495.2429	20199.78856	1603.58;
node 211	117510.0133	19980.53711	1620.31;
node 112	117685.5192	20211.86194	1605.53;
node 212	117698.3789	19992.40159	1622.66;
node 113	117875.8948	20222.25595	1607.47;
node 213	117886.841	20002.62045	1625.02;
node 114	118066.3545	20230.96982	1609.42;
node 214	118075.3852	20011.19275	1627.37;

# Pier 48
node 481	118260.44	20128.06	1320.00;
node 482	118260.44	20128.06	1516.11;
node 483	118260.44	20128.06	1620.54;
node 484	118256.88	20238.00	1611.36;
node 485	118264.00	20018.12	1629.72;

# Intermediate nodes Pier 48 - Pier 49
node 121	118539.1172	20245.32917	1614.38;
node 221	118543.3861	20025.34629	1633.18;
node 122	118821.4223	20248.96739	1617.41;
node 222	118822.8453	20028.96049	1636.63;
node 123	119103.7507	20248.91697	1620.43;
node 223	119102.3279	20028.96008	1640.09;
node 124	119386.0545	20245.17784	1623.46;
node 224	119381.7872	20025.34493	1643.54;

# Pier 49
node 491	119664.78	20127.93	1356.00;
node 492	119664.78	20127.93	1531.23;
node 493	119664.78	20127.93	1636.74;
node 494	119668.29	20237.75	1626.48;
node 495	119661.18	20018.12	1647.00;

# Intermediate nodes Pier 49 - Abutment 50
node 131	119833.1633	20231.70342	1628.33;
node 231	119779.9242	20013.94764	1648.44;
node 132	119997.9903	20224.39757	1630.18;
node 232	119898.6475	20009.1266	1649.88;
node 133	120162.7567	20215.83339	1632.02;
node 233	120017.3424	20003.65293	1651.32;
node 134	120327.4529	20206.01149	1633.87;
node 234	120136.0055	19997.52665	1652.76;

# Abutment 50
node 501	120494.6558	20231.3041	1635.72;
node 502	120492.0694	20194.93225	1635.72;
node 503	120489.2658	20155.50613	1635.72;
node 504	120256.8134	20027.14623	1654.20;
node 505	120254.6331	19990.74791	1654.20;
node 506	120252.2697	19951.29292	1654.20;

# Boundary conditions
fix 481 1  1  1  1  1  1;    # Bent 48 Column Bottom, piles will be added later
fix 491 1  1  1  1  1  1;    # Bent 49 Column Bottom, piles will be added later

fix 471	1  1  1  0  0  0;    # Abutment 47 nodes, will be replaced by springs later
fix 472	1  1  1  1  1  1;
fix 473	1  1  1  0  0  0;
fix 474	1  1  1  0  0  0;
fix 475	1  1  1  0  0  0;
fix 476	1  1  1  0  0  0;

fix 501	1  1  1  0  0  0;    # Abutment 50 nodes, will be replaced by springs later
fix 502	1  1  1  1  1  1;
fix 503	1  1  1  0  0  0;
fix 504	1  1  1  0  0  0;
fix 505	1  1  1  1  1  1;
fix 506	1  1  1  0  0  0;


# ELEMENTS
# Use rigid links for the rigid elements
# rigidLink beam 472 471;     # Abutment 47
# rigidLink beam 472 473;

# rigidLink beam 502 501;     # Abutment 50
# rigidLink beam 502 503;

# rigidLink beam 483 482;     # Bent 48  
# rigidLink beam 483 484;
# rigidLink beam 483 485;

# rigidLink beam 493 492;     # Bent 49  
# rigidLink beam 493 494;
# rigidLink beam 493 495;

# columns and aerial girders
geomTransf Linear 1 0 1 0;                # transformation for girders, consider the rigid end offset later
geomTransf PDelta 2 0 1 0;                # transformation for columns, update later considering the actual

# correct values for the beam, double check
set E 4595.4;
set G 1838.2;
set A 7577.8750;
set Iy 4987074.7140;
set Iz 8119339.1141;
set J [expr $Iy+$Iz];
set wconc 2.246520588911893e-07; # computed as (0.150kip/386.4)/(12 inch)^3

# correct values for the column, double check
set hcol 106.0;
set bcol 60.0;
set Ecol 4595.4;
set Gcol 1838.2;
set Acol [expr $hcol*$bcol];
set Iycol [expr $hcol*$hcol*$hcol*$bcol/12.0];
set Izcol [expr $bcol*$bcol*$bcol*$hcol/12.0];
set Jcol [expr $Iycol+$Izcol];
set wconc 2.246520588911893e-07; # computed as (0.150kip/386.4)/(12 inch)^3

# Define the column section
BuildRCrectSection1 1;  #left column


#element elasticBeamColumn $eleTag $iNode $jNode $A $E $G $J $Iy $Iz $transfTag <-mass $massDens> <-cMass>
# span 1 (Abutment 47 - Pier 48) CL 
element elasticBeamColumn 111 472 111 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 112 111 112 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 113 112 113 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 114 113 114 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 115 114 484 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;

# span 1 (Abutment 47 - Pier 48) CR
element elasticBeamColumn 211 475 211 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 212 211 212 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 213 212 213 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 214 213 214 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 215 214 485 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;

# Pier 48
#element elasticBeamColumn 481 481 482 $Acol $Ecol $Gcol $Jcol $Iycol $Izcol 2 -mass [expr $wconc*$Acol] -cMass;
#element forceBeamColumn $eleTag $iNode $jNode $numIntgrPts $secTag $transfTag 
element forceBeamColumn 481 481 482 4 1 2 -mass [expr $wconc*$Acol];

# span 2 (Pier 48 - Pier 49) CL
element elasticBeamColumn 121 484 121 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 122 121 122 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 123 122 123 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 124 123 124 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 125 124 494 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;

# span 2 (Pier 48 - Pier 49) CR
element elasticBeamColumn 221 485 221 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 222 221 222 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 223 222 223 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 224 223 224 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 225 224 495 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;

# Pier 49
#element elasticBeamColumn 491 491 492 $Acol $Ecol $Gcol $Jcol $Iycol $Izcol 2 -mass [expr $wconc*$Acol] -cMass;
#element forceBeamColumn $eleTag $iNode $jNode $transfTag
element forceBeamColumn 491 491 492 4 1 2 -mass [expr $wconc*$Acol];

# span 3 (Pier 49 - Abutment 50) CL
element elasticBeamColumn 131 494 131 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 132 131 132 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 133 132 133 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 134 133 134 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 135 134 502 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;

# span 3 (Pier 49 - Abutment 50) CR
element elasticBeamColumn 231 495 231 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 232 231 232 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 233 232 233 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 234 233 234 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 235 234 505 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;

# rigid elements
element elasticBeamColumn 471 471 472 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 472 472 473 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 501 501 502 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 502 502 503 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 482 482 483 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 483 483 484 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 485 483 485 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 492 492 493 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 493 493 494 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
element elasticBeamColumn 495 493 495 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;


# Eigenvalue Analysis
set lambdaN [eigen -fullGenLapack 4];

puts "Eigenvalue analysis complete"
set lambda1 [lindex $lambdaN 0];
set lambda2 [lindex $lambdaN 1];
set lambda3 [lindex $lambdaN 2];

set omega1 [expr pow($lambda1,0.5)];
set omega2 [expr pow($lambda2,0.5)];
set omega3 [expr pow($lambda3,0.5)];

set pi 3.14159265359;

set T1 [expr 2.0*$pi/$omega1];
set T2 [expr 2.0*$pi/$omega2];
set T3 [expr 2.0*$pi/$omega3];

puts "T1 = $T1; T2 = $T2; T3=$T3"



# set LCol [expr 12*$ft];		# column height (parallel to Y axis)
# set LBeam [expr 20*$ft];		# beam length (parallel to X axis)
# set LGird [expr 20*$ft];		# girder length (parallel to Z axis)

# # ------ frame configuration
# set NStory 3;			# number of stories above ground level
# set NBay 1;			# number of bays in X direction
# set NBayZ 1;			# number of bays in Z direction
# puts "Number of Stories in Y: $NStory; Number of bays in X: $NBay; Number of bays in Z: $NBayZ"

# # define NODAL COORDINATES
# # calculate locations of beam/column intersections:
# set X1 0.;
# set X2 [expr $X1 + $LBeam];
# set Y1 0.;
# set Y2 [expr $Y1 + $LCol];
# set Y3 [expr $Y2 + $LCol];
# set Y4 [expr $Y3 + $LCol];
# set Z1 0.0;
# set Z2 [expr $Z1 + $LGird];

# node 111 $X1 $Y1 $Z1;	# frame 1
# node 112 $X2 $Y1 $Z1;
# node 121 $X1 $Y2 $Z1;
# node 122 $X2 $Y2 $Z1;
# node 131 $X1 $Y3 $Z1;
# node 132 $X2 $Y3 $Z1;
# node 141 $X1 $Y4 $Z1;
# node 142 $X2 $Y4 $Z1;
# node 211 $X1 $Y1 $Z2;	# frame 2
# node 212 $X2 $Y1 $Z2;
# node 221 $X1 $Y2 $Z2;
# node 222 $X2 $Y2 $Z2;
# node 231 $X1 $Y3 $Z2;
# node 232 $X2 $Y3 $Z2;
# node 241 $X1 $Y4 $Z2;
# node 242 $X2 $Y4 $Z2;


# # define Rigid Floor Diaphragm
# set RigidDiaphragm ON ;		# options: ON, OFF. specify this before the analysis parameters are set the constraints are handled differently.
# set Xa [expr ($X2+$X1)/2];		# mid-span coordinate for rigid diaphragm
# set Za [expr ($Z2+$Z1)/2];
# # rigid-diaphragm nodes in center of each diaphram
# set RigidDiaphragm ON ;		# this communicates to the analysis parameters that I will be using rigid diaphragms
# node 1121 $Xa $Y2 $Za;		# master nodes for rigid diaphragm -- story 2, bay 1, frame 1-2
# node 1131 $Xa $Y3 $Za;		# master nodes for rigid diaphragm -- story 3, bay 1, frame 1-2
# node 1141 $Xa $Y4 $Za;		# master nodes for rigid diaphragm -- story 4, bay 1, frame 1-2
# # Constraints for rigid diaphragm master nodes
# fix 1121 0  1  0  1  0  1
# fix 1131 0  1  0  1  0  1
# fix 1141 0  1  0  1  0  1
# # ------------------------define Rigid Diaphram, dof 2 is normal to floor
# set perpDirn 2;
# rigidDiaphragm $perpDirn 1121 121 122 221 222;	# level 2
# rigidDiaphragm $perpDirn 1131 131 132 231 232;	# level 3 
# rigidDiaphragm $perpDirn 1141 141 142 241 242;	# level 4 

# # determine support nodes where ground motions are input, for multiple-support excitation
# set iSupportNode "111 112 211 212"

# # BOUNDARY CONDITIONS
# fixY 0.0  1 1 1 0 1 0;		# pin all Y=0.0 nodes

# # calculated MODEL PARAMETERS, particular to this model
# # Set up parameters that are particular to the model for displacement control
# set IDctrlNode 141;		# node where displacement is read for displacement control
# set IDctrlDOF 1;			# degree of freedom of displacement read for displacement control
# set LBuilding [expr $Y4];		# total building height

# # Define SECTIONS -------------------------------------------------------------
# set SectionType FiberSection ;		# options: Elastic FiberSection
# #set SectionType Elastic ;		# options: Elastic FiberSection

# # define section tags:
# set ColSecTag 1
# set BeamSecTag 2
# set GirdSecTag 3
# set ColSecTagFiber 4
# set BeamSecTagFiber 5
# set GirdSecTagFiber 6
# set SecTagTorsion 70

# # Section Properties:
# set HCol [expr 28*$in];		# square-Column width
# set BCol $HCol
# set HBeam [expr 24*$in];		# Beam depth -- perpendicular to bending axis
# set BBeam [expr 18*$in];		# Beam width -- parallel to bending axis
# set HGird [expr 24*$in];		# Girder depth -- perpendicular to bending axis
# set BGird [expr 18*$in];		# Girder width -- parallel to bending axis

# if {$SectionType == "Elastic"} {
	# # material properties:
	# set fc 4000*$psi;			# concrete nominal compressive strength
	# set Ec [expr 57*$ksi*pow($fc/$psi,0.5)];	# concrete Young's Modulus
	# set nu 0.2;			# Poisson's ratio
	# set Gc [expr $Ec/2./[expr 1+$nu]];  	# Torsional stiffness Modulus
	# set J $Ubig;			# set large torsional stiffness
	# # column section properties:
	# set AgCol [expr $HCol*$BCol];		# rectuangular-Column cross-sectional area
	# set IzCol [expr 0.5*1./12*$BCol*pow($HCol,3)];	# about-local-z Rect-Column gross moment of inertial
	# set IyCol [expr 0.5*1./12*$HCol*pow($BCol,3)];	# about-local-z Rect-Column gross moment of inertial
	# # beam sections:
	# set AgBeam [expr $HBeam*$BBeam];		# rectuangular-Beam cross-sectional area
	# set IzBeam [expr 0.5*1./12*$BBeam*pow($HBeam,3)];	# about-local-z Rect-Beam cracked moment of inertial
	# set IyBeam [expr 0.5*1./12*$HBeam*pow($BBeam,3)];	# about-local-y Rect-Beam cracked moment of inertial
	# # girder sections:
	# set AgGird [expr $HGird*$BGird];		# rectuangular-Girder cross-sectional area
	# set IzGird [expr 0.5*1./12*$BGird*pow($HGird,3)];	# about-local-z Rect-Girder cracked moment of inertial
	# set IyGird [expr 0.5*1./12*$HGird*pow($BGird,3)];	# about-local-y Rect-Girder cracked moment of inertial
		
	# section Elastic $ColSecTag $Ec $AgCol $IzCol $IyCol $Gc $J
	# section Elastic $BeamSecTag $Ec $AgBeam $IzBeam $IyBeam $Gc $J
	# section Elastic $GirdSecTag $Ec $AgGird $IzGird $IyGird $Gc $J

	# set IDconcCore  1;		# material numbers for recorder (this stressstrain recorder will be blank, as this is an elastic section)
	# set IDSteel  2;			# material numbers for recorder (this stressstrain recorder will be blank, as this is an elastic section)

# } elseif {$SectionType == "FiberSection"} {
	# # MATERIAL parameters 
	# source LibMaterialsRC.tcl;	# define library of Reinforced-concrete Materials

	# # FIBER SECTION properties 
	# # Column section geometry:
	# set cover [expr 2.5*$in];	# rectangular-RC-Column cover
	# set numBarsTopCol 8;		# number of longitudinal-reinforcement bars on top layer
	# set numBarsBotCol 8;		# number of longitudinal-reinforcement bars on bottom layer
	# set numBarsIntCol 6;		# TOTAL number of reinforcing bars on the intermediate layers
	# set barAreaTopCol [expr 1.*$in*$in];	# longitudinal-reinforcement bar area
	# set barAreaBotCol [expr 1.*$in*$in];	# longitudinal-reinforcement bar area
	# set barAreaIntCol [expr 1.*$in*$in];	# longitudinal-reinforcement bar area

	# set numBarsTopBeam 6;		# number of longitudinal-reinforcement bars on top layer
	# set numBarsBotBeam 6;		# number of longitudinal-reinforcement bars on bottom layer
	# set numBarsIntBeam 2;		# TOTAL number of reinforcing bars on the intermediate layers
	# set barAreaTopBeam [expr 1.*$in*$in];	# longitudinal-reinforcement bar area
	# set barAreaBotBeam [expr 1.*$in*$in];	# longitudinal-reinforcement bar area
	# set barAreaIntBeam [expr 1.*$in*$in];	# longitudinal-reinforcement bar area

	# set numBarsTopGird 6;		# number of longitudinal-reinforcement bars on top layer
	# set numBarsBotGird 6;		# number of longitudinal-reinforcement bars on bottom layer
	# set numBarsIntGird 2;		# TOTAL number of reinforcing bars on the intermediate layers
	# set barAreaTopGird [expr 1.*$in*$in];	# longitudinal-reinforcement bar area
	# set barAreaBotGird [expr 1.*$in*$in];	# longitudinal-reinforcement bar area
	# set barAreaIntGird [expr 1.*$in*$in];	# longitudinal-reinforcement bar area

	# set nfCoreY 20;		# number of fibers in the core patch in the y direction
	# set nfCoreZ 20;		# number of fibers in the core patch in the z direction
	# set nfCoverY 20;		# number of fibers in the cover patches with long sides in the y direction
	# set nfCoverZ 20;		# number of fibers in the cover patches with long sides in the z direction
	# # rectangular section with one layer of steel evenly distributed around the perimeter and a confined core.
	# BuildRCrectSection $ColSecTagFiber $HCol $BCol $cover $cover $IDconcCore  $IDconcCover $IDSteel $numBarsTopCol $barAreaTopCol $numBarsBotCol $barAreaBotCol $numBarsIntCol $barAreaIntCol  $nfCoreY $nfCoreZ $nfCoverY $nfCoverZ
	# BuildRCrectSection $BeamSecTagFiber $HBeam $BBeam $cover $cover $IDconcCore  $IDconcCover $IDSteel $numBarsTopBeam $barAreaTopBeam $numBarsBotBeam $barAreaBotBeam $numBarsIntBeam $barAreaIntBeam  $nfCoreY $nfCoreZ $nfCoverY $nfCoverZ
	# BuildRCrectSection $GirdSecTagFiber $HGird $BGird $cover $cover $IDconcCore  $IDconcCover $IDSteel $numBarsTopGird $barAreaTopGird $numBarsBotGird $barAreaBotGird $numBarsIntGird $barAreaIntGird  $nfCoreY $nfCoreZ $nfCoverY $nfCoverZ

	# # assign torsional Stiffness for 3D Model
	# uniaxialMaterial Elastic $SecTagTorsion $Ubig
	# section Aggregator $ColSecTag $SecTagTorsion T -section $ColSecTagFiber
	# section Aggregator $BeamSecTag $SecTagTorsion T -section $BeamSecTagFiber
	# section Aggregator $GirdSecTag $SecTagTorsion T -section $GirdSecTagFiber
# } else {
	# puts "No section has been defined"
	# return -1
# }
# set GammaConcrete [expr 150*$pcf];   			# Reinforced-Concrete weight density (weight per volume) 
# set QdlCol [expr $GammaConcrete*$HCol*$BCol];	# self weight of Column, weight per length
# set QBeam [expr $GammaConcrete*$HBeam*$BBeam];	# self weight of Beam, weight per length
# set QGird [expr $GammaConcrete*$HGird*$BGird];	# self weight of Gird, weight per length

# # define ELEMENTS -------------------------------------------------------
# # set up geometric transformations of element
# #   separate columns and beams, in case of P-Delta analysis for columns
# #   in 3D model, assign vector vecxz
# set IDColTransf 1; # all columns
# set IDBeamTransf 2; # all beams
# set IDGirdTransf 3; # all girders
# set ColTransfType Linear ;			# options, Linear PDelta Corotational 
# geomTransf $ColTransfType $IDColTransf  0 0 1 ; 	# only columns can have PDelta effects (gravity effects)
# geomTransf Linear $IDBeamTransf 0 0 1
# geomTransf Linear $IDGirdTransf 1 0 0

# # Define Beam-Column Elements
# set np 5;	# number of Gauss integration points for nonlinear curvature distribution

# # Frame 1
# # columns
# element nonlinearBeamColumn 1111 111 121 $np $ColSecTag $IDColTransf;		# level 1-2
# element nonlinearBeamColumn 1112 112 122 $np $ColSecTag $IDColTransf
# element nonlinearBeamColumn 1121 121 131 $np $ColSecTag $IDColTransf;		# level 2-3
# element nonlinearBeamColumn 1122 122 132 $np $ColSecTag $IDColTransf
# element nonlinearBeamColumn 1131 131 141 $np $ColSecTag $IDColTransf;		# level 3-4
# element nonlinearBeamColumn 1132 132 142 $np $ColSecTag $IDColTransf
# # beams
# element nonlinearBeamColumn 1221 121 122 $np $BeamSecTag $IDBeamTransf;	# level 2
# element nonlinearBeamColumn 1231 131 132 $np $BeamSecTag $IDBeamTransf;	# level 3
# element nonlinearBeamColumn 1241 141 142 $np $BeamSecTag $IDBeamTransf;	# level 4

# # Frame 2
# # columns
# element nonlinearBeamColumn 2111 211 221 $np $ColSecTag $IDColTransf;		# level 1-2
# element nonlinearBeamColumn 2112 212 222 $np $ColSecTag $IDColTransf
# element nonlinearBeamColumn 2121 221 231 $np $ColSecTag $IDColTransf;		# level 2-3
# element nonlinearBeamColumn 2122 222 232 $np $ColSecTag $IDColTransf
# element nonlinearBeamColumn 2131 231 241 $np $ColSecTag $IDColTransf;		# level 3-4
# element nonlinearBeamColumn 2132 232 242 $np $ColSecTag $IDColTransf
# # beams
# element nonlinearBeamColumn 2221 221 222 $np $BeamSecTag $IDBeamTransf;	# level 2
# element nonlinearBeamColumn 2231 231 232 $np $BeamSecTag $IDBeamTransf;	# level 3
# element nonlinearBeamColumn 2241 241 242 $np $BeamSecTag $IDBeamTransf;	# level 4

# # girders connecting frames
# # Frame 1-2
# element nonlinearBeamColumn  1321 121 221 $np $GirdSecTag $IDGirdTransf;	# level 2
# element nonlinearBeamColumn  1322 122 222 $np $GirdSecTag $IDGirdTransf;
# element nonlinearBeamColumn  1331 131 231 $np $GirdSecTag $IDGirdTransf;	# level 3
# element nonlinearBeamColumn  1332 132 232 $np $GirdSecTag $IDGirdTransf;
# element nonlinearBeamColumn  1341 141 241 $np $GirdSecTag $IDGirdTransf;	# level 4
# element nonlinearBeamColumn  1342 142 242 $np $GirdSecTag $IDGirdTransf;


# # --------------------------------------------------------------------------------------------------------------------------------
# # Define GRAVITY LOADS, weight and masses
# # calculate dead load of frame, assume this to be an internal frame (do LL in a similar manner)
# # calculate distributed weight along the beam length
# set Tslab [expr 6*$in];			# 6-inch slab
# set Lslab [expr $LGird/2]; 			# slab extends a distance of $LGird/2 in/out of plane
# set DLfactor 1.0;				# scale dead load up a little
# set Qslab [expr $GammaConcrete*$Tslab*$Lslab*$DLfactor]; 
# set QdlBeam [expr $Qslab + $QBeam]; 	# dead load distributed along beam (one-way slab)
# set QdlGird $QGird; 			# dead load distributed along girder
# set WeightCol [expr $QdlCol*$LCol];  		# total Column weight
# set WeightBeam [expr $QdlBeam*$LBeam]; 	# total Beam weight
# set WeightGird [expr $QdlGird*$LGird]; 	# total Beam weight

# # assign masses to the nodes that the columns are connected to 
# # each connection takes the mass of 1/2 of each element framing into it (mass=weight/$g)
# set Mmid  [expr ($WeightCol/2 + $WeightCol/2 +$WeightBeam/2+$WeightGird/2)/$g];
# set Mtop  [expr ($WeightCol/2 + $WeightBeam/2+$WeightGird/2)/$g];

# # frame 1
# mass 121 $Mmid 0 $Mmid 0. 0. 0.;		# level 2
# mass 122 $Mmid 0 $Mmid 0. 0. 0.;
# mass 131 $Mmid 0 $Mmid 0. 0. 0.;		# level 3
# mass 132 $Mmid 0 $Mmid 0. 0. 0.;
# mass 141 $Mtop 0 $Mtop 0. 0. 0.;		# level 4
# mass 142 $Mtop 0 $Mtop 0. 0. 0.;

# # frame 2
# mass 221 $Mmid 0 $Mmid 0. 0. 0.;		# level 2
# mass 222 $Mmid 0 $Mmid 0. 0. 0.;
# mass 231 $Mmid 0 $Mmid 0. 0. 0.;		# level 3
# mass 232 $Mmid 0 $Mmid 0. 0. 0.;
# mass 241 $Mtop 0 $Mtop 0. 0. 0.;		# level 4
# mass 242 $Mtop 0 $Mtop 0. 0. 0.;

# set FloorWeight2 [expr 4*$WeightCol + 2*$WeightGird + 2*$WeightBeam]
# set FloorWeight3 [expr 4*$WeightCol + 2*$WeightGird + 2*$WeightBeam]
# set FloorWeight4 [expr 2*$WeightCol + 2*$WeightGird + 2*$WeightBeam]
# set WeightTotal [expr $FloorWeight2+$FloorWeight3+$FloorWeight4];			# total building weight
# set MassTotal [expr $WeightTotal/$g];							# total building mass

# # --------------------------------------------------------------------------------------------------------------------------------
# # LATERAL-LOAD distribution for static pushover analysis
# # calculate distribution of lateral load based on mass/weight distributions along building height
# # Fj = WjHj/sum(WiHi)  * Weight   at each floor j
# set sumWiHi [expr $FloorWeight2*$Y2+$FloorWeight3*$Y3+$FloorWeight4*$Y4]; 		# sum of storey weight times height, for lateral-load distribution
# set WiHi2 [expr $FloorWeight2*$Y2]; 		# storey weight times height, for lateral-load distribution
# set WiHi3 [expr $FloorWeight3*$Y3]; 		# storey weight times height, for lateral-load distribution
# set WiHi4 [expr $FloorWeight4*$Y4]; 		# storey weight times height, for lateral-load distribution
# set F2 [expr $WiHi2/$sumWiHi*$WeightTotal];	# lateral load at level
# set F3 [expr $WiHi3/$sumWiHi*$WeightTotal];	# lateral load at level
# set F4 [expr $WiHi4/$sumWiHi*$WeightTotal];	# lateral load at level


# # Define RECORDERS -------------------------------------------------------------
# recorder Node -file $dataDir/DFree.out -time -node 141 -dof 1 2 3 disp;			# displacements of free node
# recorder Node -file $dataDir/DBase.out -time -node 111 112 211 212   -dof 1 2 3 disp;		# displacements of support nodes
# recorder Node -file $dataDir/RBase.out -time -node 111 112 211 212   -dof 1 2 3 reaction;		# support reaction
# recorder Drift -file $dataDir/DrNode.out -time -iNode 111 -jNode 141 -dof 1 -perpDirn 2;		# lateral drift
# recorder Element -file $dataDir/Fel1.out -time -ele 1111 localForce;				# element forces in local coordinates
# recorder Element -xml $dataDir/PlasticRotation1.out -time -ele 1111 plasticRotation;				# element forces in local coordinates
# recorder Element -file $dataDir/ForceEle1sec1.out -time -ele 1111 section 1 force;			# section forces, axial and moment, node i
# recorder Element -file $dataDir/DefoEle1sec1.out -time -ele 11111 section 1 deformation;		# section deformations, axial and curvature, node i
# recorder Element -file $dataDir/ForceEle1sec$np.out -time -ele 111 section $np force;			# section forces, axial and moment, node j
# recorder Element -file $dataDir/DefoEle1sec$np.out -time -ele 1111 section $np deformation;		# section deformations, axial and curvature, node j
# set yFiber [expr $HCol/2-$cover];								# fiber location for stress-strain recorder, local coords
# set zFiber [expr $BCol/2-$cover];								# fiber location for stress-strain recorder, local coords
# recorder Element -file $dataDir/SSconcEle1sec1.out -time -ele 1111 section $np fiber $yFiber $zFiber $IDconcCore  stressStrain;	# steel fiber stress-strain, node i
# recorder Element -file $dataDir/SSreinfEle1sec1.out -time -ele 1111 section $np fiber $yFiber $zFiber $IDSteel  stressStrain;	# steel fiber stress-strain, node i
# puts "check1"
# # Define DISPLAY -------------------------------------------------------------
# set  xPixels 1200;	# height of graphical window in pixels
# set  yPixels 800;	# height of graphical window in pixels
# set  xLoc1 10;	# horizontal location of graphical window (0=upper left-most corner)
# set  yLoc1 10;	# vertical location of graphical window (0=upper left-most corner)
# set dAmp 2;	# scaling factor for viewing deformed shape, it depends on the dimensions of the model
# DisplayModel3D NodeNumbers $dAmp $xLoc1 $yLoc1  $xPixels $yPixels
# #DisplayModel3D nill $dAmp $xLoc1 $yLoc1  $xPixels $yPixels


# # define GRAVITY -------------------------------------------------------------
# # GRAVITY LOADS # define gravity load applied to beams and columns -- 	eleLoad applies loads in local coordinate axis
# pattern Plain 101 Linear {
# # Frame 1
# # columns
	# eleLoad -ele 1111 -type -beamUniform 0. 0. -$QdlCol;		# level 1-2
	# eleLoad -ele 1112 -type -beamUniform 0. 0. -$QdlCol
	# eleLoad -ele 1121 -type -beamUniform 0. 0. -$QdlCol;		# level 2-3
	# eleLoad -ele 1122 -type -beamUniform 0. 0. -$QdlCol
	# eleLoad -ele 1131 -type -beamUniform 0. 0. -$QdlCol;		# level 3-4
	# eleLoad -ele 1132 -type -beamUniform 0. 0. -$QdlCol
# # beams
	# eleLoad -ele 1221 -type -beamUniform -$QdlBeam 0.;		# level 2
	# eleLoad -ele 1231 -type -beamUniform -$QdlBeam 0.;		# level 3
	# eleLoad -ele 1241 -type -beamUniform -$QdlBeam 0.;		# level 4

# # Frame 2
# # columns
	# eleLoad -ele 2111 -type -beamUniform 0. 0. -$QdlCol;		# level 1-2
	# eleLoad -ele 2112 -type -beamUniform 0. 0. -$QdlCol
	# eleLoad -ele 2121 -type -beamUniform 0. 0. -$QdlCol;		# level 2-3
	# eleLoad -ele 2122 -type -beamUniform 0. 0. -$QdlCol
	# eleLoad -ele 2131 -type -beamUniform 0. 0. -$QdlCol;		# level 3-4
	# eleLoad -ele 2132 -type -beamUniform 0. 0. -$QdlCol
# # beams
	# eleLoad -ele 2221 -type -beamUniform -$QdlBeam 0.;		# level 2
	# eleLoad -ele 2231 -type -beamUniform -$QdlBeam 0.;		# level 3
	# eleLoad -ele 2241 -type -beamUniform -$QdlBeam 0.;		# level 4

# # girders connecting frames
# # Frame 1-2
	# eleLoad -ele 1321 -type -beamUniform -$QdlGird 0.;		# level 2
	# eleLoad -ele 1322 -type -beamUniform -$QdlGird 0.;
	# eleLoad -ele 1331 -type -beamUniform -$QdlGird 0.;		# level 3
	# eleLoad -ele 1332 -type -beamUniform -$QdlGird 0.;
	# eleLoad -ele 1341 -type -beamUniform -$QdlGird 0.;		# level 4
	# eleLoad -ele 1342 -type -beamUniform -$QdlGird 0.;
# }
# Gravity-analysis parameters -- load-controlled static analysis
# set Tol 1.0e-8;			# convergence tolerance for test
# constraints Transformation;     		# how it handles boundary conditions
# numberer RCM;			# renumber dof's to minimize band-width (optimization), if you want to
# system BandGeneral ;		# how to store and solve the system of equations in the analysis (large model: try UmfPack)
# test EnergyIncr $Tol 6 ; 		# determine if convergence has been achieved at the end of an iteration step
# algorithm Newton;			# use Newton's solution algorithm: updates tangent stiffness at every iteration
# set NstepGravity 10;  		# apply gravity in 10 steps
# set DGravity [expr 1./$NstepGravity]; 	# first load increment;
# integrator LoadControl $DGravity;	# determine the next time step for an analysis
# analysis Static;			# define type of analysis static or transient
# analyze $NstepGravity;		# apply gravity


# # ------------------------------------------------- maintain constant gravity loads and reset time to zero
# loadConst -time 0.0
# set Tol 1.0e-6;			# reduce tolerance after gravity loads
# puts "Model Built"


