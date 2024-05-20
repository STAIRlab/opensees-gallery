####################################################################################################
####################################################################################################
#                                        3-story CBF Building
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
set NStory  3;
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
puts "Composite Action is Considered"
set Composite 1;
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
set   X_CGP1  21.3016;  set   Y_CGP1  21.3016;
set   X_CGP2  22.7600;  set   Y_CGP2  22.7600;
set   X_CGP3  20.4177;  set   Y_CGP3  20.4177;
# Geometry of Mid-Span Gusset Plate
set   X_MGP1  15.6005;  set   Y_MGP1  15.6005;
set   X_MGP2  15.6005;  set   Y_MGP2  15.6005;
set   X_MGP3  21.3016;  set   Y_MGP3  21.3016;

# FRAME GRID LINES
set Floor4  540.00;
set Floor3  360.00;
set Floor2  180.00;
set Floor1 0.0;

set Axis1 0.0;
set Axis2 360.00;
set Axis3 720.00;
set Axis4 1080.00;

set HBuilding 540.00;
set WFrame 360.00;
variable HBuilding 540.00;

####################################################################################################
#                                                  NODES                                           #
####################################################################################################

# COMMAND SYNTAX 
# node $NodeID  $X-Coordinate  $Y-Coordinate;

#SUPPORT NODES
node 110   $Axis1  $Floor1; node 120   $Axis2  $Floor1; node 130   $Axis3  $Floor1; node 140   $Axis4  $Floor1; 

# EGF COLUMN GRID NODES
node 430   $Axis3  $Floor4; node 440   $Axis4  $Floor4; 
node 330   $Axis3  $Floor3; node 340   $Axis4  $Floor3; 
node 230   $Axis3  $Floor2; node 240   $Axis4  $Floor2; 

# EGF COLUMN NODES
node 431  $Axis3  $Floor4; node 441  $Axis4  $Floor4; 
node 333  $Axis3  $Floor3; node 343  $Axis4  $Floor3; 
node 331  $Axis3  $Floor3; node 341  $Axis4  $Floor3; 
node 233  $Axis3  $Floor2; node 243  $Axis4  $Floor2; 
node 231  $Axis3  $Floor2; node 241  $Axis4  $Floor2; 
node 133  $Axis3  $Floor1; node 143  $Axis4  $Floor1; 

# EGF BEAM NODES
node 434  $Axis3  $Floor4; node 442  $Axis4  $Floor4; 
node 334  $Axis3  $Floor3; node 342  $Axis4  $Floor3; 
node 234  $Axis3  $Floor2; node 242  $Axis4  $Floor2; 

# MF COLUMN NODES
node 411  $Axis1 [expr $Floor4 - 30.40/2]; node 421  $Axis2 [expr $Floor4 - 30.40/2]; 
node 313  $Axis1 [expr $Floor3 + 21.50/2]; node 323  $Axis2 [expr $Floor3 + 21.50/2]; 
node 311  $Axis1 [expr $Floor3 - 21.50/2]; node 321  $Axis2 [expr $Floor3 - 21.50/2]; 
node 213  $Axis1 [expr $Floor2 + 18.40/2]; node 223  $Axis2 [expr $Floor2 + 18.40/2]; 
node 211  $Axis1 [expr $Floor2 - 18.40/2]; node 221  $Axis2 [expr $Floor2 - 18.40/2]; 
node 113  $Axis1 $Floor1; node 123  $Axis2 $Floor1; 

# MF BEAM NODES
node 414   [expr $Axis1 + 13.10/2] $Floor4; node 422   [expr $Axis2 - 13.10/2] $Floor4; 
node 314   [expr $Axis1 + 13.10/2] $Floor3; node 322   [expr $Axis2 - 13.10/2] $Floor3; 
node 214   [expr $Axis1 + 13.10/2] $Floor2; node 222   [expr $Axis2 - 13.10/2] $Floor2; 

# COLUMN SPLICE NODES

# MID-SPAN GUSSET PLATE RIGID OFFSET NODES
node 204101   [expr ($Axis1 + $Axis2)/2] $Floor4;
node 204102   [expr ($Axis1 + $Axis2)/2 - 72.1250/2] $Floor4;
node 204112   [expr ($Axis1 + $Axis2)/2 - 72.1250/2] $Floor4;
node 204105   [expr ($Axis1 + $Axis2)/2 + 72.1250/2] $Floor4;
node 204115   [expr ($Axis1 + $Axis2)/2 + 72.1250/2] $Floor4;
node 204104   [expr ($Axis1 + $Axis2)/2 + $X_MGP3] [expr $Floor4 - $Y_MGP3];
node 204114   [expr ($Axis1 + $Axis2)/2 + $X_MGP3] [expr $Floor4 - $Y_MGP3];
node 204103   [expr ($Axis1 + $Axis2)/2 - $X_MGP3] [expr $Floor4 - $Y_MGP3];
node 204113   [expr ($Axis1 + $Axis2)/2 - $X_MGP3] [expr $Floor4 - $Y_MGP3];
node 202101   [expr ($Axis1 + $Axis2)/2] $Floor2;
node 202102   [expr ($Axis1 + $Axis2)/2 - 75.5000/2] $Floor2;
node 202112   [expr ($Axis1 + $Axis2)/2 - 75.5000/2] $Floor2;
node 202105   [expr ($Axis1 + $Axis2)/2 + 75.5000/2] $Floor2;
node 202115   [expr ($Axis1 + $Axis2)/2 + 75.5000/2] $Floor2;
node 202104   [expr ($Axis1 + $Axis2)/2 + $X_MGP1] [expr $Floor2 - $Y_MGP1];
node 202114   [expr ($Axis1 + $Axis2)/2 + $X_MGP1] [expr $Floor2 - $Y_MGP1];
node 202103   [expr ($Axis1 + $Axis2)/2 - $X_MGP1] [expr $Floor2 - $Y_MGP1];
node 202113   [expr ($Axis1 + $Axis2)/2 - $X_MGP1] [expr $Floor2 - $Y_MGP1];
node 202106   [expr ($Axis1 + $Axis2)/2 + $X_MGP2] [expr $Floor2 + $Y_MGP2];
node 202116   [expr ($Axis1 + $Axis2)/2 + $X_MGP2] [expr $Floor2 + $Y_MGP2];
node 202107   [expr ($Axis1 + $Axis2)/2 - $X_MGP2] [expr $Floor2 + $Y_MGP2];
node 202117   [expr ($Axis1 + $Axis2)/2 - $X_MGP2] [expr $Floor2 + $Y_MGP2];

# CORNER X-BRACING RIGID OFFSET NODES
node 103140   [expr $Axis1 + $X_CGP3] [expr $Floor3 + $Y_CGP3];
node 103141   [expr $Axis1 + $X_CGP3] [expr $Floor3 + $Y_CGP3];
node 103150   [expr $Axis1 + $X_CGP2] [expr $Floor3 - $Y_CGP2];
node 103151   [expr $Axis1 + $X_CGP2] [expr $Floor3 - $Y_CGP2];
node 103240   [expr $Axis2 - $X_CGP3] [expr $Floor3 + $Y_CGP3];
node 103241   [expr $Axis2 - $X_CGP3] [expr $Floor3 + $Y_CGP3];
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
ConstructPanel_Rectangle  1 4 $Axis1 $Floor4 $E $A_Stiff $I_Stiff 13.10 30.40 $trans_selected; ConstructPanel_Rectangle  2 4 $Axis2 $Floor4 $E $A_Stiff $I_Stiff 13.10 30.40 $trans_selected; 
ConstructPanel_Rectangle  1 3 $Axis1 $Floor3 $E $A_Stiff $I_Stiff 13.10 21.50 $trans_selected; ConstructPanel_Rectangle  2 3 $Axis2 $Floor3 $E $A_Stiff $I_Stiff 13.10 21.50 $trans_selected; 
ConstructPanel_Rectangle  1 2 $Axis1 $Floor2 $E $A_Stiff $I_Stiff 13.10 18.40 $trans_selected; ConstructPanel_Rectangle  2 2 $Axis2 $Floor2 $E $A_Stiff $I_Stiff 13.10 18.40 $trans_selected; 

####################################################################################################
#                                          PANEL ZONE SPRINGS                                      #
####################################################################################################

# COMMAND SYNTAX 
# Spring_PZ    Element_ID Node_i Node_j E mu fy tw_Col tdp d_Col d_Beam tf_Col bf_Col Ic trib ts Response_ID transfTag
Spring_PZ    904100 404109 404110 $E $mu [expr $fy *   1.0]  0.71   0.00 13.10 30.40  1.11 12.30 1070.00 3.500 4.000 2 1; Spring_PZ    904200 404209 404210 $E $mu [expr $fy *   1.0]  0.71   0.00 13.10 30.40  1.11 12.30 1070.00 3.500 4.000 2 1; 
Spring_PZ    903100 403109 403110 $E $mu [expr $fy *   1.0]  0.71   0.00 13.10 21.50  1.11 12.30 1070.00 3.500 4.000 2 1; Spring_PZ    903200 403209 403210 $E $mu [expr $fy *   1.0]  0.71   0.00 13.10 21.50  1.11 12.30 1070.00 3.500 4.000 2 1; 
Spring_PZ    902100 402109 402110 $E $mu [expr $fy *   1.0]  0.71   0.00 13.10 18.40  1.11 12.30 1070.00 3.500 4.000 2 1; Spring_PZ    902200 402209 402210 $E $mu [expr $fy *   1.0]  0.71   0.00 13.10 18.40  1.11 12.30 1070.00 3.500 4.000 2 1; 

####################################################################################################
#                                          RIGID BRACE LINKS                                       #
####################################################################################################

# COMMAND SYNTAX 
# element elasticBeamColumn $ElementID $NodeIDi $NodeIDj $Area $E $Inertia $transformation;

# MIDDLE RIGID LINKS
element elasticBeamColumn 704122 204101 204102 $A_Stiff $E $I_Stiff  $trans_selected;
element elasticBeamColumn 704133 204101 204103 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 704144 204101 204104 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 704155 204101 204105 $A_Stiff $E $I_Stiff  $trans_selected;


element elasticBeamColumn 702122 202101 202102 $A_Stiff $E $I_Stiff  $trans_selected;
element elasticBeamColumn 702133 202101 202103 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 702144 202101 202104 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 702155 202101 202105 $A_Stiff $E $I_Stiff  $trans_selected;
element elasticBeamColumn 702166 202101 202106 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 702177 202101 202107 $A_Stiff $E $I_Stiff  $trans_Corot;


# CORNER RIGID LINKS
element elasticBeamColumn 703111 403110 103140 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 703199 403199 103150 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 703211 403208 103240 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 703299 403206 103250 $A_Stiff $E $I_Stiff  $trans_Corot;

element elasticBeamColumn 701111 110 101140 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 701211 120 101240 $A_Stiff $E $I_Stiff  $trans_Corot;


####################################################################################################
#                                 			GUSSET PLATE SPRINGS   		                            #
####################################################################################################

# COMMAND SYNTAX 
# Spring_Gusset $SpringID $NodeIDi $NodeIDj $E $fy $L_buckling $t_plate $L_connection $d_brace $MatID;

# BEAM MID-SPAN GUSSET PLATE SPRING
Spring_Gusset 904133 204113 204103 $E $fyG 9.1220 0.5000 14.0000 8.6300  4000;
Spring_Gusset 904144 204114 204104 $E $fyG 9.1220 0.5000 14.0000 8.6300  4001;

Spring_Gusset 902133 202113 202103 $E $fyG 9.0551 0.5000 24.0000 9.6300  4002;
Spring_Gusset 902144 202114 202104 $E $fyG 9.0551 0.5000 24.0000 9.6300  4003;
Spring_Gusset 902166 202116 202106 $E $fyG 8.9712 0.5000 24.4375 8.6300  4004;
Spring_Gusset 902177 202117 202107 $E $fyG 8.9712 0.5000 24.4375 8.6300  4005;


# CORNER GUSSET PLATE SPRINGS
Spring_Gusset 903111 103140 103141 $E $fyG 7.3731 0.5000 14.0000 8.6300  4006;
Spring_Gusset 903199 103150 103151 $E $fyG 7.9925 0.5000 21.0000 8.6300  4007;
Spring_Gusset 903211 103240 103241 $E $fyG 7.3731 0.5000 14.0000 8.6300  4008;
Spring_Gusset 903299 103250 103251 $E $fyG 7.9925 0.5000 21.0000 8.6300  4009;

Spring_Gusset 901111 101140 101141 $E $fyG 10.2084 0.5000 24.0000 9.6300  4010;
Spring_Gusset 901211 101240 101241 $E $fyG 10.2084 0.5000 24.0000 9.6300  4011;


####################################################################################################
#                                 BRACE MEMBERS WITH FATIGUE MATERIAL                              #
####################################################################################################

# CREATE FATIGUE MATERIALS
# COMMAND SYNTAX 
# FatigueMat $MatID $BraceSecType $fy $E $L_brace $ry_brace $ht_brace $htw_brace $bftf_brace;
FatigueMat 100 2 $fyB $E 202.3709 3.2400 20.7000  0.0 0.0;
FatigueMat 102 2 $fyB $E 200.3084 2.8900 18.5000  0.0 0.0;
FatigueMat 104 2 $fyB $E 195.5584 2.9500 28.8000  0.0 0.0;

# CREATE THE BRACE SECTIONS
# COMMAND SYNTAX 
# FiberRHSS $BraceSecType $FatigueMatID $h_brace $t_brace $nFiber $nFiber $nFiber $nFiber;
FiberCHSS     1   101 9.6300 0.5000 12 4; 
FiberCHSS     2   103 8.6300 0.5000 12 4; 
FiberCHSS     3   105 8.6300 0.3220 12 4; 

# CONSTRUCT THE BRACE MEMBERS
# COMMAND SYNTAX 
# ConstructBrace $BraceID $NodeIDi $NodeIDj $nSegments $Imperfeection $nIntgeration $transformation;
ConstructBrace 8101100   101141   202113     1   $nSegments $initialGI $nIntegration  $trans_Corot;
ConstructBrace 8201100   101241   202114     1   $nSegments $initialGI $nIntegration  $trans_Corot;

ConstructBrace 8102100   103151   202117     2   $nSegments $initialGI $nIntegration  $trans_Corot;
ConstructBrace 8202100   103251   202116     2   $nSegments $initialGI $nIntegration  $trans_Corot;

ConstructBrace 8103100   103141   204113     3   $nSegments $initialGI $nIntegration  $trans_Corot;
ConstructBrace 8203100   103241   204114     3   $nSegments $initialGI $nIntegration  $trans_Corot;


# CONSTRUCT THE GHOST BRACES
uniaxialMaterial Elastic 1000 100.0
element corotTruss 4101100   101141   202113  0.05  1000;
element corotTruss 4201100   101241   202114  0.05  1000;
element corotTruss 4102100   103151   202117  0.05  1000;
element corotTruss 4202100   103251   202116  0.05  1000;
element corotTruss 4103100   103141   204113  0.05  1000;
element corotTruss 4203100   103241   204114  0.05  1000;

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
FiberWF    101 666 13.1000 12.3000 1.1100 0.7100 6 2 6 2; ConstructFiberColumn 603100     313    411   101 5 0.0010 5 $trans_selected 0;
FiberWF    102 666 13.1000 12.3000 1.1100 0.7100 6 2 6 2; ConstructFiberColumn 603200     323    421   102 5 0.0010 5 $trans_selected 0;

FiberWF    103 666 13.1000 12.3000 1.1100 0.7100 6 2 6 2; ConstructFiberColumn 602100     213    311   103 5 0.0010 5 $trans_selected 0;
FiberWF    104 666 13.1000 12.3000 1.1100 0.7100 6 2 6 2; ConstructFiberColumn 602200     223    321   104 5 0.0010 5 $trans_selected 0;

FiberWF    105 666 13.1000 12.3000 1.1100 0.7100 6 2 6 2; ConstructFiberColumn 601100     113    211   105 5 0.0010 5 $trans_selected 0;
FiberWF    106 666 13.1000 12.3000 1.1100 0.7100 6 2 6 2; ConstructFiberColumn 601200     123    221   106 5 0.0010 5 $trans_selected 0;


# BEAMS
element ModElasticBeam2d   504101      414   204112  51.0000 $E [expr ($n+1)/$n*0.90*$Comp_I*8230.0000] $K11_2 $K33_2 $K44_2 $trans_selected; element ModElasticBeam2d   504102      422   204115  51.0000 $E [expr ($n+1)/$n*0.90*$Comp_I*8230.0000] $K11_2 $K33_2 $K44_2 $trans_selected; 
element ModElasticBeam2d   503100      314      322  32.7000 $E [expr ($n+1)/$n*0.90*$Comp_I*2670.0000] $K11_2 $K33_2 $K44_2 $trans_selected; 
element ModElasticBeam2d   502101      214   202112  19.1000 $E [expr ($n+1)/$n*0.90*$Comp_I*1070.0000] $K11_2 $K33_2 $K44_2 $trans_selected; element ModElasticBeam2d   502102      222   202115  19.1000 $E [expr ($n+1)/$n*0.90*$Comp_I*1070.0000] $K11_2 $K33_2 $K44_2 $trans_selected; 

###################################################################################################
#                                           MF BEAM SPRINGS                                       #
###################################################################################################

# COMMAND SYNTAX 
# Spring_Pinching $SpringID $iNode $jNode $EffectivePlasticStrength $gap $CompositeFlag

set gap 0.08;
Spring_IMK 904104 404104 414 $E $fy [expr $Comp_I*8230.0000]  30.4000 40.8000 7.0400 3.4200 137.3875 68.6937 68.6937 36723.5000 0 $Composite 0 2; Spring_IMK 904202 422 404202 $E $fy [expr $Comp_I*8230.0000]  30.4000 40.8000 7.0400 3.4200 137.3875 68.6937 68.6937 36723.5000 0 $Composite 0 2; Spring_IMK 904122 204102 204112 $E $fy [expr $Comp_I*8230.0000] 30.4000 40.8000 7.0400 3.4200 137.3875 68.6937 68.6937 36723.5000 0 $Composite 0 2; Spring_IMK 904155 204105 204115 $E $fy [expr $Comp_I*8230.0000] 30.4000 40.8000 7.0400 3.4200 137.3875 68.6937 68.6937 36723.5000 0 $Composite 0 2; 
Spring_IMK 902104 402104 214 $E $fy [expr $Comp_I*1070.0000]  18.4000 35.7000 5.0600 1.6900 135.7000 67.8500 67.8500 8046.5000 0 $Composite 0 2; Spring_IMK 902202 222 402202 $E $fy [expr $Comp_I*1070.0000]  18.4000 35.7000 5.0600 1.6900 135.7000 67.8500 67.8500 8046.5000 0 $Composite 0 2; Spring_IMK 902122 202102 202112 $E $fy [expr $Comp_I*1070.0000] 18.4000 35.7000 5.0600 1.6900 135.7000 67.8500 67.8500 8046.5000 0 $Composite 0 2; Spring_IMK 902155 202105 202115 $E $fy [expr $Comp_I*1070.0000] 18.4000 35.7000 5.0600 1.6900 135.7000 67.8500 67.8500 8046.5000 0 $Composite 0 2; 

Spring_Pinching  903104  403104 314 16879.5000 $gap $Composite; Spring_Pinching  903202  322 403202 16879.5000 $gap $Composite; 

###################################################################################################
#                                           MF COLUMN SPRINGS                                     #
###################################################################################################

Spring_Rigid  904101  404101     411; Spring_Rigid  904201  404201     421; 
Spring_Rigid  903103  403103     313; Spring_Rigid  903203  403203     323; 
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
element truss 1004 404204 430 $A_Stiff 99;
element truss 1003 403204 330 $A_Stiff 99;
element truss 1002 402204 230 $A_Stiff 99;

####################################################################################################
#                                          EGF COLUMNS AND BEAMS                                   #
####################################################################################################

# GRAVITY COLUMNS
element elasticBeamColumn  603300     333     431 52.5000 $E [expr (317.6250  + 690.0000)] $trans_PDelta; element elasticBeamColumn  603400     343     441 52.5000 $E [expr (317.6250  + 690.0000)] $trans_PDelta; 
element elasticBeamColumn  602300     233     331 52.5000 $E [expr (317.6250  + 690.0000)] $trans_PDelta; element elasticBeamColumn  602400     243     341 52.5000 $E [expr (317.6250  + 690.0000)] $trans_PDelta; 
element elasticBeamColumn  601300     133     231 52.5000 $E [expr (317.6250  + 690.0000)] $trans_PDelta; element elasticBeamColumn  601400     143     241 52.5000 $E [expr (317.6250  + 690.0000)] $trans_PDelta; 

# GRAVITY BEAMS
element elasticBeamColumn  504200     434     442 193.9000 $E [expr $Comp_I_GC * 18900.0000] $trans_PDelta;
element elasticBeamColumn  503200     334     342 214.2000 $E [expr $Comp_I_GC * 21700.0000] $trans_PDelta;
element elasticBeamColumn  502200     234     242 214.2000 $E [expr $Comp_I_GC * 21700.0000] $trans_PDelta;

# GRAVITY COLUMNS SPRINGS
Spring_IMK   904301     430     431 $E $fy [expr (317.6250 + 690.0000)] 14.0000 27.5000 6.9700 2.4600 180.0000 90.0000 180.0000 16193.5813 0 $Composite 0 2; Spring_IMK   904401     440     441 $E $fy [expr (317.6250 + 690.0000)] 14.0000 27.5000 6.9700 2.4600 180.0000 90.0000 180.0000 16193.5813 0 $Composite 0 2; 
Spring_IMK   903303     330     333 $E $fy [expr (317.6250 + 690.0000)] 14.0000 27.5000 6.9700 2.4600 180.0000 90.0000 180.0000 16193.5813 0 $Composite 0 2; Spring_IMK   903403     340     343 $E $fy [expr (317.6250 + 690.0000)] 14.0000 27.5000 6.9700 2.4600 180.0000 90.0000 180.0000 16193.5813 0 $Composite 0 2; 
Spring_IMK   903301     330     331 $E $fy [expr (317.6250 + 690.0000)] 14.0000 27.5000 6.9700 2.4600 180.0000 90.0000 180.0000 16193.5813 0 $Composite 0 2; Spring_IMK   903401     340     341 $E $fy [expr (317.6250 + 690.0000)] 14.0000 27.5000 6.9700 2.4600 180.0000 90.0000 180.0000 16193.5813 0 $Composite 0 2; 
Spring_IMK   902303     230     233 $E $fy [expr (317.6250 + 690.0000)] 14.0000 27.5000 6.9700 2.4600 180.0000 90.0000 180.0000 16193.5813 0 $Composite 0 2; Spring_IMK   902403     240     243 $E $fy [expr (317.6250 + 690.0000)] 14.0000 27.5000 6.9700 2.4600 180.0000 90.0000 180.0000 16193.5813 0 $Composite 0 2; 
Spring_IMK   902301     230     231 $E $fy [expr (317.6250 + 690.0000)] 14.0000 27.5000 6.9700 2.4600 180.0000 90.0000 180.0000 16193.5813 0 $Composite 0 2; Spring_IMK   902401     240     241 $E $fy [expr (317.6250 + 690.0000)] 14.0000 27.5000 6.9700 2.4600 180.0000 90.0000 180.0000 16193.5813 0 $Composite 0 2; 
Spring_IMK   901303     130     133 $E $fy 690.0000 14.0000 27.5000 6.9700 2.4600 180.0000 90.0000 180.0000 10333.4000 0 $Composite 0 2; Spring_IMK   901403     140     143 $E $fy 690.0000 14.0000 27.5000 6.9700 2.4600 180.0000 90.0000 180.0000 10333.4000 0 $Composite 0 2; 

# GRAVITY BEAMS SPRINGS
set gap 0.08;
Spring_Pinching   904304     430     434 107569.0000 $gap 1; Spring_Pinching   904402     440     442 107569.0000 $gap 1; 
Spring_Pinching   903304     330     334 122391.5000 $gap 1; Spring_Pinching   903402     340     342 122391.5000 $gap 1; 
Spring_Pinching   902304     230     234 122391.5000 $gap 1; Spring_Pinching   902402     240     242 122391.5000 $gap 1; 

###################################################################################################
#                                       BOUNDARY CONDITIONS                                       #
###################################################################################################

# MF SUPPORTS
fix 110 1 1 1; 
fix 120 1 1 1; 

# EGF SUPPORTS
fix 130 1 1 0; fix 140 1 1 0; 

# MF FLOOR MOVEMENT
equalDOF 404104 404204 1; 
equalDOF 403104 403204 1; 
equalDOF 402104 402204 1; 

# BEAM MID-SPAN HORIZONTAL MOVEMENT CONSTRAINT
equalDOF 404104 204101 1; 
equalDOF 402104 202101 1; 

# EGF FLOOR MOVEMENT
equalDOF 430 440 1;
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
recorder Node -file $MainFolder/EigenAnalysis/EigenVectorsMode1.out -node 402104 403104 404104  -dof 1 "eigen  1";
recorder Node -file $MainFolder/EigenAnalysis/EigenVectorsMode2.out -node 402104 403104 404104  -dof 1 "eigen  2";
recorder Node -file $MainFolder/EigenAnalysis/EigenVectorsMode3.out -node 402104 403104 404104  -dof 1 "eigen  3";

# TIME
recorder Node -file $MainFolder/$SubFolder/Time.out  -time -node 110 -dof 1 disp;

# SUPPORT REACTIONS
recorder Node -file $MainFolder/$SubFolder/Support1.out -node     110 -dof 1 2 6 reaction; recorder Node -file $MainFolder/$SubFolder/Support2.out -node     120 -dof 1 2 6 reaction; recorder Node -file $MainFolder/$SubFolder/Support3.out -node     130 -dof 1 2 6 reaction; recorder Node -file $MainFolder/$SubFolder/Support4.out -node     140 -dof 1 2 6 reaction; 

# FLOOR LATERAL DISPLACEMENT
recorder Node -file $MainFolder/$SubFolder/Disp4_MF.out  -node  404104 -dof 1 disp; 
recorder Node -file $MainFolder/$SubFolder/Disp3_MF.out  -node  403104 -dof 1 disp; 
recorder Node -file $MainFolder/$SubFolder/Disp2_MF.out  -node  402104 -dof 1 disp; 

# STORY DRIFT RATIO
recorder Drift -file $MainFolder/$SubFolder/SDR3_MF.out -iNode  403104 -jNode  404104 -dof 1 -perpDirn 2; 
recorder Drift -file $MainFolder/$SubFolder/SDR2_MF.out -iNode  402104 -jNode  403104 -dof 1 -perpDirn 2; 
recorder Drift -file $MainFolder/$SubFolder/SDR1_MF.out -iNode     110 -jNode  402104 -dof 1 -perpDirn 2; 

# COLUMN ELASTIC ELEMENT FORCES
recorder Element -file $MainFolder/$SubFolder/Column31.out -ele  603100 force; recorder Element -file $MainFolder/$SubFolder/Column32.out -ele  603200 force; recorder Element -file $MainFolder/$SubFolder/Column33.out -ele  603300 force; recorder Element -file $MainFolder/$SubFolder/Column34.out -ele  603400 force; 
recorder Element -file $MainFolder/$SubFolder/Column21.out -ele  602100 force; recorder Element -file $MainFolder/$SubFolder/Column22.out -ele  602200 force; recorder Element -file $MainFolder/$SubFolder/Column23.out -ele  602300 force; recorder Element -file $MainFolder/$SubFolder/Column24.out -ele  602400 force; 
recorder Element -file $MainFolder/$SubFolder/Column11.out -ele  601100 force; recorder Element -file $MainFolder/$SubFolder/Column12.out -ele  601200 force; recorder Element -file $MainFolder/$SubFolder/Column13.out -ele  601300 force; recorder Element -file $MainFolder/$SubFolder/Column14.out -ele  601400 force; 

# BRACE CORNER RIGID LINKS FORCES
recorder Element -file $MainFolder/$SubFolder/CGP31.out -ele  703111 globalForce; recorder Element -file $MainFolder/$SubFolder/CGP32.out -ele  703211 globalForce; 
recorder Element -file $MainFolder/$SubFolder/CGP21.out -ele  703199 globalForce; recorder Element -file $MainFolder/$SubFolder/CGP22.out -ele  703299 globalForce; 
recorder Element -file $MainFolder/$SubFolder/CGP11.out -ele  701111 globalForce; recorder Element -file $MainFolder/$SubFolder/CGP12.out -ele  701211 globalForce; 

###################################################################################################
#                                              NODAL MASS                                         #
###################################################################################################

set g 386.10;
mass 404104 0.2506  1.e-9 1.e-9; mass 404204 0.2506  1.e-9 1.e-9; mass 430 1.0810  1.e-9 1.e-9; mass 440 1.0810  1.e-9 1.e-9; 
mass 403104 0.3963  1.e-9 1.e-9; mass 403204 0.3963  1.e-9 1.e-9; mass 330 1.0082  1.e-9 1.e-9; mass 340 1.0082  1.e-9 1.e-9; 
mass 402104 0.3963  1.e-9 1.e-9; mass 402204 0.3963  1.e-9 1.e-9; mass 230 1.0082  1.e-9 1.e-9; mass 240 1.0082  1.e-9 1.e-9; 

constraints Plain;

###################################################################################################
#                                        EIGEN VALUE ANALYSIS                                     #
###################################################################################################

set pi [expr 2.0*asin(1.0)];
set nEigen 3;
set lambdaN [eigen [expr $nEigen]];
set lambda1 [lindex $lambdaN 0];
set lambda2 [lindex $lambdaN 1];
set lambda3 [lindex $lambdaN 2];
set w1 [expr pow($lambda1,0.5)];
set w2 [expr pow($lambda2,0.5)];
set w3 [expr pow($lambda3,0.5)];
set T1 [expr round(2.0*$pi/$w1 *1000.)/1000.];
set T2 [expr round(2.0*$pi/$w2 *1000.)/1000.];
set T3 [expr round(2.0*$pi/$w3 *1000.)/1000.];
puts "T1 = $T1 s";
puts "T2 = $T2 s";
puts "T3 = $T3 s";
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
	load 404103 0. -50.681 0.; 	load 404203 0. -50.681 0.; 
	load 403103 0. -59.963 0.; 	load 403203 0. -59.963 0.; 
	load 402103 0. -59.963 0.; 	load 402203 0. -59.963 0.; 

	# EGF COLUMN LOADS
	load 430 0. -516.150000 0.; 	load 440 0. -516.150000 0.; 
	load 330 0. -576.900000 0.; 	load 340 0. -576.900000 0.; 
	load 230 0. -576.900000 0.; 	load 240 0. -576.900000 0.; 

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

puts "Seismic Weight= 3681.113 kip";
puts "Seismic Mass=  8.281 kip.sec2/in";

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
set a0 [expr $zeta*2.0*$w1*$w3/($w1 + $w3)];
set a1 [expr $zeta*2.0/($w1 + $w3)];
set a1_mod [expr $a1*(1.0+$n)/$n];
region 1 -ele  603100 603200 602100 602200 601100 601200 504101 504102 503100 502101 502102  -rayleigh 0.0 0.0 $a1_mod 0.0;
region 2 -node  402104 402204 230 240 403104 403204 330 340 404104 404204 430 440  -rayleigh $a0 0.0 0.0 0.0;
region 3 -eleRange  900000  999999 -rayleigh 0.0 0.0 [expr $a1_mod/10] 0.0;

# GROUND MOTION ACCELERATION FILE INPUT
set AccelSeries "Series -dt $GMdt -filePath $GMfile -factor  [expr $EqSF * $g]"
pattern UniformExcitation  200 1 -accel $AccelSeries

set MF_FloorNodes [list  402104 403104 404104 ];
set EGF_FloorNodes [list  230 330 430 ];
set GMduration [expr $GMdt*$GMpoints];
set FVduration 10.000000;
set NumSteps [expr round(($GMduration + $FVduration)/$GMdt)];	# number of steps in analysis
set totTime [expr $GMdt*$NumSteps];                            # Total time of analysis
set dtAnalysis [expr 0.500000*$GMdt];                             	# dt of Analysis

DynamicAnalysisCollapseSolverX  $GMdt	$dtAnalysis	$totTime $NStory	 0.15   $MF_FloorNodes	$EGF_FloorNodes	180.00 180.00 1 $StartTime $MaxRunTime;

###################################################################################################
###################################################################################################
							puts "Ground Motion Done. End Time: [getTime]"
###################################################################################################
###################################################################################################
}

wipe all;
