####################################################################################################
####################################################################################################
#                                        2-story CBF Building
####################################################################################################
####################################################################################################

# CLEAR ALL;
wipe all;

# BUILD MODEL (2D - 3 DOF/node)
model basic -ndm 2 -ndf 3

####################################################################################################
#                                        BASIC MODEL VARIABLES                                     #
####################################################################################################

set  global RunTime;
set  global StartTime;
set  global MaxRunTime;
set  MaxRunTime [expr 10.0000 * 60.];
set  StartTime [clock seconds];
set  RunTime 0.0;
set  EQ 1;
set  PO 0;
set  ELF 0;
set  Composite 0;
set  ShowAnimation 1;
set  ModePO 1;
set  DriftPO 0.100000;
set  DampModeI 1;
set  DampModeJ 3;
set  zeta 0.020000;

####################################################################################################
#                                       SOURCING SUBROUTINES                                       #
####################################################################################################

source DisplayModel3D.tcl;
source DisplayPlane.tcl;
source Spring_PZ.tcl;
source Spring_IMK.tcl;
source Spring_Zero.tcl;
source Spring_Rigid.tcl;
source Spring_Pinching.tcl;
source ConstructPanel_Rectangle.tcl;
source ConstructBrace.tcl;
source Spring_Gusset.tcl;
source FatigueMat.tcl;
source ConstructFiberColumn.tcl;
source FiberRHSS.tcl;
source FiberCHSS.tcl;
source FiberWF.tcl;
source DynamicAnalysisCollapseSolverX.tcl;
source Generate_lognrmrand.tcl;

####################################################################################################
#                                          Create Results Folders                                  #
####################################################################################################

# RESULT FOLDER
set MainFolder "ResultsMainFolder";
set SubFolder  "ResultsSubFolder";
file mkdir $MainFolder;
cd $MainFolder
file mkdir $SubFolder;
cd ..

####################################################################################################
#                                              INPUT                                               #
####################################################################################################

# FRAME CENTERLINE DIMENSIONS
set NStory  2;
set NBay  1;

# MATERIAL PROPERTIES
set E  29000.0; 
set mu    0.3; 
set fy  [expr  55.0 *   1.0];
set fyB [expr  45.0 *   1.0];
set fyG [expr  55.0 *   1.0];

# BASIC MATERIALS
uniaxialMaterial Elastic  9  1.e-9; 		#Flexible Material 
uniaxialMaterial Elastic  99 1000000000.;  #Rigid Material 
uniaxialMaterial UVCuniaxial  666 29000.0000 55.0000 18.0000 10.0000 0.0000 1.0000 2 3500.0000 180.0000 345.0000 10.0000; #Voce-Chaboche Material

# GEOMETRIC TRANSFORMATIONS IDs
geomTransf Linear 		 1;
geomTransf PDelta 		 2;
geomTransf Corotational 3;
set trans_Linear 	1;
set trans_PDelta 	2;
set trans_Corot  	3;
set trans_selected  2;

# STIFF ELEMENTS PROPERTY
set A_Stiff 1000.0;
set I_Stiff 100000.0;

# COMPOSITE BEAM FACTOR
set Composite 0;
set Comp_I    1.400;
set Comp_I_GC 1.400;

# FIBER ELEMENT PROPERTIES
set nSegments    8;
set initialGI    0.00100;
set nIntegration 5;

# LOGARITHMIC STANDARD DEVIATIONS (FOR UNCERTAINTY CONSIDERATION)
global Sigma_IMKcol Sigma_IMKbeam Sigma_Pinching4 Sigma_PZ; 
set Sigma_IMKcol [list  1.e-9 1.e-9 1.e-9 1.e-9 1.e-9 1.e-9 1.e-9 1.e-9 1.e-9 ];
set Sigma_IMKbeam   [list  1.e-9 1.e-9 1.e-9 1.e-9 1.e-9 1.e-9 1.e-9 1.e-9 1.e-9 ];
set Sigma_Pinching4 [list  1.e-9 1.e-9 1.e-9 1.e-9 1.e-9 1.e-9 1.e-9 1.e-9 ];
set Sigma_PZ        [list  1.e-9 1.e-9 1.e-9 1.e-9 ];
set Sigma_fy     1.e-9;
set Sigma_fyB    1.e-9;
set Sigma_fyG    1.e-9;
set Sigma_GI     1.e-9;
set Sigma_zeta   1.e-9;
global Sigma_fy Sigma_fyB Sigma_fyG Sigma_GI; global xRandom;
set SigmaX $Sigma_fy;  Generate_lognrmrand $fy 	$SigmaX; 	set fy      $xRandom;
set SigmaX $Sigma_fyB; Generate_lognrmrand $fyB 	$SigmaX; 	set fyB 	$xRandom;
set SigmaX $Sigma_fyG; Generate_lognrmrand $fyG 	$SigmaX; 	set fyG 	$xRandom;
set SigmaX $Sigma_GI;  Generate_lognrmrand 0.001000 	    $SigmaX; 	set initialGI 	$xRandom;

####################################################################################################
#                                          PRE-CALCULATIONS                                        #
####################################################################################################

set pi [expr 2.0*asin(1.0)];

# Geometry of Corner Gusset Plate
set   X_CGP1  15.6447;  set   Y_CGP1  15.6447;
set   X_CGP2  20.8155;  set   Y_CGP2  20.8155;
# Geometry of Mid-Span Gusset Plate
set   X_MGP1  17.2799;  set   Y_MGP1  17.2799;
set   X_MGP2  17.2799;  set   Y_MGP2  17.2799;

# FRAME GRID LINES
set Floor3  240.00;
set Floor2  120.00;
set Floor1 0.0;

set Axis1 0.0;
set Axis2 240.00;
set Axis3 480.00;
set Axis4 720.00;

set HBuilding 240.00;
set WFrame 240.00;
variable HBuilding 240.00;

####################################################################################################
#                                                  NODES                                           #
####################################################################################################

# COMMAND SYNTAX 
# node $NodeID  $X-Coordinate  $Y-Coordinate;

#SUPPORT NODES
node 110   $Axis1  $Floor1; node 120   $Axis2  $Floor1; node 130   $Axis3  $Floor1; node 140   $Axis4  $Floor1; 

# EGF COLUMN GRID NODES
node 330   $Axis3  $Floor3; node 340   $Axis4  $Floor3; 
node 230   $Axis3  $Floor2; node 240   $Axis4  $Floor2; 

# EGF COLUMN NODES
node 331  $Axis3  $Floor3; node 341  $Axis4  $Floor3; 
node 233  $Axis3  $Floor2; node 243  $Axis4  $Floor2; 
node 231  $Axis3  $Floor2; node 241  $Axis4  $Floor2; 
node 133  $Axis3  $Floor1; node 143  $Axis4  $Floor1; 

# EGF BEAM NODES
node 334  $Axis3  $Floor3; node 342  $Axis4  $Floor3; 
node 234  $Axis3  $Floor2; node 242  $Axis4  $Floor2; 

# MF COLUMN NODES
node 311  $Axis1 [expr $Floor3 - 24.30/2]; node 321  $Axis2 [expr $Floor3 - 24.30/2]; 
node 213  $Axis1 [expr $Floor2 + 24.30/2]; node 223  $Axis2 [expr $Floor2 + 24.30/2]; 
node 211  $Axis1 [expr $Floor2 - 24.30/2]; node 221  $Axis2 [expr $Floor2 - 24.30/2]; 
node 113  $Axis1 $Floor1; node 123  $Axis2 $Floor1; 

# MF BEAM NODES
node 314   [expr $Axis1 + 10.10/2] $Floor3; node 322   [expr $Axis2 - 10.10/2] $Floor3; 
node 214   [expr $Axis1 + 10.10/2] $Floor2; node 222   [expr $Axis2 - 10.10/2] $Floor2; 

# COLUMN SPLICE NODES

# MID-SPAN GUSSET PLATE RIGID OFFSET NODES
node 202101   [expr ($Axis1 + $Axis2)/2] $Floor2;
node 202102   [expr ($Axis1 + $Axis2)/2 - 60.7056/2] $Floor2;
node 202112   [expr ($Axis1 + $Axis2)/2 - 60.7056/2] $Floor2;
node 202105   [expr ($Axis1 + $Axis2)/2 + 60.7056/2] $Floor2;
node 202115   [expr ($Axis1 + $Axis2)/2 + 60.7056/2] $Floor2;
node 202104   [expr ($Axis1 + $Axis2)/2 + $X_MGP1] [expr $Floor2 - $Y_MGP1];
node 202114   [expr ($Axis1 + $Axis2)/2 + $X_MGP1] [expr $Floor2 - $Y_MGP1];
node 202103   [expr ($Axis1 + $Axis2)/2 - $X_MGP1] [expr $Floor2 - $Y_MGP1];
node 202113   [expr ($Axis1 + $Axis2)/2 - $X_MGP1] [expr $Floor2 - $Y_MGP1];
node 202106   [expr ($Axis1 + $Axis2)/2 + $X_MGP2] [expr $Floor2 + $Y_MGP2];
node 202116   [expr ($Axis1 + $Axis2)/2 + $X_MGP2] [expr $Floor2 + $Y_MGP2];
node 202107   [expr ($Axis1 + $Axis2)/2 - $X_MGP2] [expr $Floor2 + $Y_MGP2];
node 202117   [expr ($Axis1 + $Axis2)/2 - $X_MGP2] [expr $Floor2 + $Y_MGP2];

# CORNER X-BRACING RIGID OFFSET NODES
node 103150   [expr $Axis1 + $X_CGP2] [expr $Floor3 - $Y_CGP2];
node 103151   [expr $Axis1 + $X_CGP2] [expr $Floor3 - $Y_CGP2];
node 103250   [expr $Axis2 - $X_CGP2] [expr $Floor3 - $Y_CGP2];
node 103251   [expr $Axis2 - $X_CGP2] [expr $Floor3 - $Y_CGP2];
node 101140   [expr $Axis1 + $X_CGP1] [expr $Floor1 + $Y_CGP1];
node 101141   [expr $Axis1 + $X_CGP1] [expr $Floor1 + $Y_CGP1];
node 101240   [expr $Axis2 - $X_CGP1] [expr $Floor1 + $Y_CGP1];
node 101241   [expr $Axis2 - $X_CGP1] [expr $Floor1 + $Y_CGP1];

###################################################################################################
#                                  PANEL ZONE NODES & ELEMENTS                                    #
###################################################################################################

# PANEL ZONE NODES AND ELASTIC ELEMENTS
# Command Syntax; 
# ConstructPanel_Rectangle Axis Floor X_Axis Y_Floor E A_Panel I_Panel d_Col d_Beam transfTag 
ConstructPanel_Rectangle  1 3 $Axis1 $Floor3 $E $A_Stiff $I_Stiff 10.10 24.30 $trans_selected; ConstructPanel_Rectangle  2 3 $Axis2 $Floor3 $E $A_Stiff $I_Stiff 10.10 24.30 $trans_selected; 
ConstructPanel_Rectangle  1 2 $Axis1 $Floor2 $E $A_Stiff $I_Stiff 10.10 24.30 $trans_selected; ConstructPanel_Rectangle  2 2 $Axis2 $Floor2 $E $A_Stiff $I_Stiff 10.10 24.30 $trans_selected; 

####################################################################################################
#                                          PANEL ZONE SPRINGS                                      #
####################################################################################################

# COMMAND SYNTAX 
# Spring_PZ    Element_ID Node_i Node_j E mu fy tw_Col tdp d_Col d_Beam tf_Col bf_Col Ic trib ts Response_ID transfTag
Spring_PZ    903100 403109 403110 $E $mu [expr $fy *   1.0]  0.35   0.00 10.10 24.30  0.62  8.02 248.00 3.500 4.000 2 1; Spring_PZ    903200 403209 403210 $E $mu [expr $fy *   1.0]  0.35   0.00 10.10 24.30  0.62  8.02 248.00 3.500 4.000 2 1; 
Spring_PZ    902100 402109 402110 $E $mu [expr $fy *   1.0]  0.35   0.00 10.10 24.30  0.62  8.02 248.00 3.500 4.000 2 1; Spring_PZ    902200 402209 402210 $E $mu [expr $fy *   1.0]  0.35   0.00 10.10 24.30  0.62  8.02 248.00 3.500 4.000 2 1; 

####################################################################################################
#                                          RIGID BRACE LINKS                                       #
####################################################################################################

# COMMAND SYNTAX 
# element elasticBeamColumn $ElementID $NodeIDi $NodeIDj $Area $E $Inertia $transformation;

# MIDDLE RIGID LINKS

element elasticBeamColumn 702122 202101 202102 $A_Stiff $E $I_Stiff  $trans_selected;
element elasticBeamColumn 702133 202101 202103 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 702144 202101 202104 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 702155 202101 202105 $A_Stiff $E $I_Stiff  $trans_selected;
element elasticBeamColumn 702166 202101 202106 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 702177 202101 202107 $A_Stiff $E $I_Stiff  $trans_Corot;


# CORNER RIGID LINKS
element elasticBeamColumn 703199 403199 103150 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 703299 403206 103250 $A_Stiff $E $I_Stiff  $trans_Corot;

element elasticBeamColumn 701111 110 101140 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 701211 120 101240 $A_Stiff $E $I_Stiff  $trans_Corot;


####################################################################################################
#                                 			GUSSET PLATE SPRINGS   		                            #
####################################################################################################

# COMMAND SYNTAX 
# Spring_Gusset $SpringID $NodeIDi $NodeIDj $E $fy $L_buckling $t_plate $L_connection $d_brace $MatID;

# BEAM MID-SPAN GUSSET PLATE SPRING
Spring_Gusset 902133 202113 202103 $E $fyG 3.9866 0.5000 13.0000 6.0000  4000;
Spring_Gusset 902144 202114 202104 $E $fyG 3.9866 0.5000 13.0000 6.0000  4001;
Spring_Gusset 902166 202116 202106 $E $fyG 3.9866 0.5000 13.0000 6.0000  4002;
Spring_Gusset 902177 202117 202107 $E $fyG 3.9866 0.5000 13.0000 6.0000  4003;


# CORNER GUSSET PLATE SPRINGS
Spring_Gusset 903199 103150 103151 $E $fyG 8.6275 0.5000 13.0000 6.0000  4004;
Spring_Gusset 903299 103250 103251 $E $fyG 8.6275 0.5000 13.0000 6.0000  4005;

Spring_Gusset 901111 101140 101141 $E $fyG 9.6520 0.5000 13.0000 6.0000  4006;
Spring_Gusset 901211 101240 101241 $E $fyG 9.6520 0.5000 13.0000 6.0000  4007;


####################################################################################################
#                                 BRACE MEMBERS WITH FATIGUE MATERIAL                              #
####################################################################################################

# CREATE FATIGUE MATERIALS
# COMMAND SYNTAX 
# FatigueMat $MatID $BraceSecType $fy $E $L_brace $ry_brace $ht_brace $htw_brace $bftf_brace;
FatigueMat 100 1 $fyB $E 123.1250 2.2800 14.2000  0.0 0.0;
FatigueMat 102 1 $fyB $E 115.8125 2.2800 14.2000  0.0 0.0;

# CREATE THE BRACE SECTIONS
# COMMAND SYNTAX 
# FiberRHSS $BraceSecType $FatigueMatID $h_brace $t_brace $nFiber $nFiber $nFiber $nFiber;
FiberRHSS     1   101 6.0000 0.3750 10 4 10 4; 
FiberRHSS     2   103 6.0000 0.3750 10 4 10 4; 

# CONSTRUCT THE BRACE MEMBERS
# COMMAND SYNTAX 
# ConstructBrace $BraceID $NodeIDi $NodeIDj $nSegments $Imperfeection $nIntgeration $transformation;
ConstructBrace 8101100   101141   202113     1   $nSegments $initialGI $nIntegration  $trans_Corot;
ConstructBrace 8201100   101241   202114     1   $nSegments $initialGI $nIntegration  $trans_Corot;

ConstructBrace 8102100   103151   202117     2   $nSegments $initialGI $nIntegration  $trans_Corot;
ConstructBrace 8202100   103251   202116     2   $nSegments $initialGI $nIntegration  $trans_Corot;


# CONSTRUCT THE GHOST BRACES
uniaxialMaterial Elastic 1000 100.0
element corotTruss 4101100   101141   202113  0.05  1000;
element corotTruss 4201100   101241   202114  0.05  1000;
element corotTruss 4102100   103151   202117  0.05  1000;
element corotTruss 4202100   103251   202116  0.05  1000;

####################################################################################################
#                                     ELASTIC COLUMNS AND BEAMS                                    #
####################################################################################################

# COMMAND SYNTAX 
# element ModElasticBeam2d $ElementID $iNode $jNode $Area $E $Ix $K11 $K33 $K44 $transformation 

# STIFFNESS MODIFIERS
set n 10.;
set K44_2 [expr 6*(1+$n)/(2+3*$n)];
set K11_2 [expr (1+2*$n)*$K44_2/(1+$n)];
set K33_2 [expr (1+2*$n)*$K44_2/(1+$n)];
set K44_1 [expr 6*$n/(1+3*$n)];
set K11_1 [expr (1+2*$n)*$K44_1/(1+$n)];
set K33_1 [expr 2*$K44_1];

# COLUMNS
FiberWF    101 666 10.1000 8.0200 0.6200 0.3500 6 2 6 2; ConstructFiberColumn 602100     213    311   101 5 0.0010 5 $trans_selected 0;
FiberWF    102 666 10.1000 8.0200 0.6200 0.3500 6 2 6 2; ConstructFiberColumn 602200     223    321   102 5 0.0010 5 $trans_selected 0;

FiberWF    103 666 10.1000 8.0200 0.6200 0.3500 6 2 6 2; ConstructFiberColumn 601100     113    211   103 5 0.0010 5 $trans_selected 0;
FiberWF    104 666 10.1000 8.0200 0.6200 0.3500 6 2 6 2; ConstructFiberColumn 601200     123    221   104 5 0.0010 5 $trans_selected 0;


# BEAMS
element ModElasticBeam2d   503100      314      322  34.4000 $E [expr ($n+1)/$n*0.90*$Comp_I*3540.0000] $K11_2 $K33_2 $K44_2 $trans_selected; 
element ModElasticBeam2d   502101      214   202112  34.4000 $E [expr ($n+1)/$n*0.90*$Comp_I*3540.0000] $K11_2 $K33_2 $K44_2 $trans_selected; element ModElasticBeam2d   502102      222   202115  34.4000 $E [expr ($n+1)/$n*0.90*$Comp_I*3540.0000] $K11_2 $K33_2 $K44_2 $trans_selected; 

###################################################################################################
#                                           MF BEAM SPRINGS                                       #
###################################################################################################

# COMMAND SYNTAX 
# Spring_Pinching $SpringID $iNode $jNode $EffectivePlasticStrength $gap $CompositeFlag

set gap 0.08;
Spring_IMK 902104 402104 214 $E $fy [expr $Comp_I*3540.0000]  24.3000 39.2000 7.5300 2.9400 84.5972 42.2986 42.2986 19783.5000 0 $Composite 0 2; Spring_IMK 902202 222 402202 $E $fy [expr $Comp_I*3540.0000]  24.3000 39.2000 7.5300 2.9400 84.5972 42.2986 42.2986 19783.5000 0 $Composite 0 2; Spring_IMK 902122 202102 202112 $E $fy [expr $Comp_I*3540.0000] 24.3000 39.2000 7.5300 2.9400 84.5972 42.2986 42.2986 19783.5000 0 $Composite 0 2; Spring_IMK 902155 202105 202115 $E $fy [expr $Comp_I*3540.0000] 24.3000 39.2000 7.5300 2.9400 84.5972 42.2986 42.2986 19783.5000 0 $Composite 0 2; 

Spring_Pinching  903104  403104 314 19783.5000 $gap $Composite; Spring_Pinching  903202  322 403202 19783.5000 $gap $Composite; 

###################################################################################################
#                                           MF COLUMN SPRINGS                                     #
###################################################################################################

Spring_Rigid  903101  403101     311; Spring_Rigid  903201  403201     321; 
Spring_Rigid  902103  402103     213; Spring_Rigid  902203  402203     223; 
Spring_Rigid  902101  402101     211; Spring_Rigid  902201  402201     221; 
Spring_Rigid  901103     110     113; Spring_Rigid  901203     120     123; 

###################################################################################################
#                                          COLUMN SPLICE SPRINGS                                  #
###################################################################################################


####################################################################################################
#                                              FLOOR LINKS                                         #
####################################################################################################

# Command Syntax 
# element truss $ElementID $iNode $jNode $Area $matID
element truss 1003 403204 330 $A_Stiff 99;
element truss 1002 402204 230 $A_Stiff 99;

####################################################################################################
#                                          EGF COLUMNS AND BEAMS                                   #
####################################################################################################

# GRAVITY COLUMNS
element elasticBeamColumn  602300     233     331 100000.0000 $E 100000000.0000 $trans_PDelta; element elasticBeamColumn  602400     243     341 100000.0000 $E 100000000.0000 $trans_PDelta; 
element elasticBeamColumn  601300     133     231 100000.0000 $E 100000000.0000 $trans_PDelta; element elasticBeamColumn  601400     143     241 100000.0000 $E 100000000.0000 $trans_PDelta; 

# GRAVITY BEAMS
element elasticBeamColumn  503200     334     342 100000.0000 $E 100000000.0000 $trans_PDelta;
element elasticBeamColumn  502200     234     242 100000.0000 $E 100000000.0000 $trans_PDelta;

# GRAVITY COLUMNS SPRINGS
Spring_Zero  903301     330     331; Spring_Zero  903401     340     341; 
Spring_Zero  902303     230     233; Spring_Zero  902403     240     243; 
Spring_Zero  902301     230     231; Spring_Zero  902401     240     241; 
Spring_Zero  901303     130     133; Spring_Zero  901403     140     143; 

# GRAVITY BEAMS SPRINGS
Spring_Rigid  903304     330     334; Spring_Rigid  903402     340     342; 
Spring_Rigid  902304     230     234; Spring_Rigid  902402     240     242; 

###################################################################################################
#                                       BOUNDARY CONDITIONS                                       #
###################################################################################################

# MF SUPPORTS
fix 110 1 1 1; 
fix 120 1 1 1; 

# EGF SUPPORTS
fix 130 1 1 0; fix 140 1 1 0; 

# MF FLOOR MOVEMENT
equalDOF 403104 403204 1; 
equalDOF 402104 402204 1; 

# BEAM MID-SPAN HORIZONTAL MOVEMENT CONSTRAINT
equalDOF 402104 202101 1; 

# EGF FLOOR MOVEMENT
equalDOF 330 340 1;
equalDOF 230 240 1;


##################################################################################################
##################################################################################################
                                       puts "Model Built"
##################################################################################################
##################################################################################################

###################################################################################################
#                                             RECORDERS                                           #
###################################################################################################

# EIGEN VECTORS
recorder Node -file $MainFolder/EigenAnalysis/EigenVectorsMode1.out -node 402104 403104  -dof 1 "eigen  1";
recorder Node -file $MainFolder/EigenAnalysis/EigenVectorsMode2.out -node 402104 403104  -dof 1 "eigen  2";

# TIME
recorder Node -file $MainFolder/$SubFolder/Time.out  -time -node 110 -dof 1 disp;

# SUPPORT REACTIONS
recorder Node -file $MainFolder/$SubFolder/Support1.out -node     110 -dof 1 2 6 reaction; recorder Node -file $MainFolder/$SubFolder/Support2.out -node     120 -dof 1 2 6 reaction; recorder Node -file $MainFolder/$SubFolder/Support3.out -node     130 -dof 1 2 6 reaction; recorder Node -file $MainFolder/$SubFolder/Support4.out -node     140 -dof 1 2 6 reaction; 

# FLOOR LATERAL DISPLACEMENT
recorder Node -file $MainFolder/$SubFolder/Disp3_MF.out  -node  403104 -dof 1 disp; 
recorder Node -file $MainFolder/$SubFolder/Disp2_MF.out  -node  402104 -dof 1 disp; 

# STORY DRIFT RATIO
recorder Drift -file $MainFolder/$SubFolder/SDR2_MF.out -iNode  402104 -jNode  403104 -dof 1 -perpDirn 2; 
recorder Drift -file $MainFolder/$SubFolder/SDR1_MF.out -iNode     110 -jNode  402104 -dof 1 -perpDirn 2; 

# COLUMN ELASTIC ELEMENT FORCES
recorder Element -file $MainFolder/$SubFolder/Column21.out -ele  602100 force; recorder Element -file $MainFolder/$SubFolder/Column22.out -ele  602200 force; recorder Element -file $MainFolder/$SubFolder/Column23.out -ele  602300 force; recorder Element -file $MainFolder/$SubFolder/Column24.out -ele  602400 force; 
recorder Element -file $MainFolder/$SubFolder/Column11.out -ele  601100 force; recorder Element -file $MainFolder/$SubFolder/Column12.out -ele  601200 force; recorder Element -file $MainFolder/$SubFolder/Column13.out -ele  601300 force; recorder Element -file $MainFolder/$SubFolder/Column14.out -ele  601400 force; 

# BRACE CORNER RIGID LINKS FORCES
recorder Element -file $MainFolder/$SubFolder/CGP21.out -ele  703199 globalForce; recorder Element -file $MainFolder/$SubFolder/CGP22.out -ele  703299 globalForce; 
recorder Element -file $MainFolder/$SubFolder/CGP11.out -ele  701111 globalForce; recorder Element -file $MainFolder/$SubFolder/CGP12.out -ele  701211 globalForce; 

###################################################################################################
#                                              NODAL MASS                                         #
###################################################################################################

set g 386.10;
mass 403104 0.1437  1.e-9 1.e-9; mass 403204 0.1437  1.e-9 1.e-9; mass 330 1.1636  1.e-9 1.e-9; mass 340 1.1636  1.e-9 1.e-9; 
mass 402104 0.2409  1.e-9 1.e-9; mass 402204 0.2409  1.e-9 1.e-9; mass 230 1.1150  1.e-9 1.e-9; mass 240 1.1150  1.e-9 1.e-9; 

constraints Plain;

###################################################################################################
#                                        EIGEN VALUE ANALYSIS                                     #
###################################################################################################

set pi [expr 2.0*asin(1.0)];
set nEigen 2;
set lambdaN [eigen [expr $nEigen]];
set lambda1 [lindex $lambdaN 0];
set lambda2 [lindex $lambdaN 1];
set w1 [expr pow($lambda1,0.5)];
set w2 [expr pow($lambda2,0.5)];
set T1 [expr round(2.0*$pi/$w1 *1000.)/1000.];
set T2 [expr round(2.0*$pi/$w2 *1000.)/1000.];
puts "T1 = $T1 s";
puts "T2 = $T2 s";
set fileX [open "EigenPeriod.out" w];
puts $fileX $T1;puts $fileX $T2;close $fileX;

constraints Plain;
algorithm Newton;
integrator LoadControl 1;
analysis Static;
analyze 1;

###################################################################################################
###################################################################################################
									puts "Eigen Analysis Done"
###################################################################################################
###################################################################################################

###################################################################################################
#                                      STATIC GRAVITY ANALYSIS                                    #
###################################################################################################

pattern Plain 100 Linear {

	# MF COLUMNS LOADS
	load 403103 0. -22.525 0.; 	load 403203 0. -22.525 0.; 
	load 402103 0. -26.650 0.; 	load 402203 0. -26.650 0.; 

	# EGF COLUMN LOADS
	load 330 0. -534.462500 0.; 	load 340 0. -534.462500 0.; 
	load 230 0. -590.525000 0.; 	load 240 0. -590.525000 0.; 

}

# Conversion Parameters
constraints Plain;
numberer RCM;
system BandGeneral;
test NormDispIncr 1.0e-5 60 ;
algorithm Newton;
integrator LoadControl 0.1;
analysis Static;
analyze 10;

loadConst -time 0.0;

###################################################################################################
###################################################################################################
										puts "Gravity Done"
###################################################################################################
###################################################################################################

puts "Seismic Weight= 2348.325 kip";
puts "Seismic Mass=  5.326 kip.sec2/in";

if {$ShowAnimation == 1} {
	DisplayModel3D DeformedShape 5.00 100 100  1000 750;
}

###################################################################################################
#                                   DYNAMIC EARTHQUAKE ANALYSIS                                   #
###################################################################################################

if {$EQ==1} {

set GMfile "NR94cnp.txt";				# ground motion filename
set GMdt 0.01;							# timestep of input GM file
set EqSF 1.0;							# ground motion scaling factor
set GMpoints 2495;						# number of steps in ground motion
	
# Rayleigh Damping
global Sigma_zeta; global xRandom;
set zeta 0.020;
set SigmaX $Sigma_zeta; Generate_lognrmrand $zeta 		$SigmaX; 		set zeta 	$xRandom;
set a0 [expr $zeta*2.0*$w1*$w2/($w1 + $w2)];
set a1 [expr $zeta*2.0/($w1 + $w2)];
set a1_mod [expr $a1*(1.0+$n)/$n];
region 1 -ele  603100 603200 602100 602200 601100 601200 504101 504102 503100 502101 502102  -rayleigh 0.0 0.0 $a1_mod 0.0;
region 2 -node  402104 402204 230 240 403104 403204 330 340  -rayleigh $a0 0.0 0.0 0.0;
region 3 -eleRange  900000  999999 -rayleigh 0.0 0.0 [expr $a1_mod/10] 0.0;

# GROUND MOTION ACCELERATION FILE INPUT
set AccelSeries "Series -dt $GMdt -filePath $GMfile -factor  [expr $EqSF * $g]"
pattern UniformExcitation  200 1 -accel $AccelSeries

set MF_FloorNodes [list  402104 403104 ];
set EGF_FloorNodes [list  230 330 ];
set GMduration [expr $GMdt*$GMpoints];
set FVduration 10.000000;
set NumSteps [expr round(($GMduration + $FVduration)/$GMdt)];	# number of steps in analysis
set totTime [expr $GMdt*$NumSteps];                            # Total time of analysis
set dtAnalysis [expr 0.500000*$GMdt];                             	# dt of Analysis

DynamicAnalysisCollapseSolverX  $GMdt	$dtAnalysis	$totTime $NStory	 0.15   $MF_FloorNodes	$EGF_FloorNodes	120.00 120.00 1 $StartTime $MaxRunTime;

###################################################################################################
###################################################################################################
							puts "Ground Motion Done. End Time: [getTime]"
###################################################################################################
###################################################################################################
}

wipe all;
