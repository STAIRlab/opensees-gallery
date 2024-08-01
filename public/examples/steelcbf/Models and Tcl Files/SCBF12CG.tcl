####################################################################################################
####################################################################################################
#                                        12-story CBF Building
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
set NStory 12;
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
set   X_CGP1  24.6710;  set   Y_CGP1  24.6710;
set   X_CGP2  24.1583;  set   Y_CGP2  24.1583;
set   X_CGP3  24.1583;  set   Y_CGP3  24.1583;
set   X_CGP4  24.5720;  set   Y_CGP4  24.5720;
set   X_CGP5  22.4004;  set   Y_CGP5  22.4004;
set   X_CGP6  21.3504;  set   Y_CGP6  21.3504;
set   X_CGP7  21.3504;  set   Y_CGP7  21.3504;
set   X_CGP8  21.3504;  set   Y_CGP8  21.3504;
set   X_CGP9  19.8860;  set   Y_CGP9  19.8860;
set   X_CGP10  19.7863;  set   Y_CGP10  19.7863;
set   X_CGP11  17.9075;  set   Y_CGP11  17.9075;
set   X_CGP12  14.8492;  set   Y_CGP12  14.8492;
# Geometry of Mid-Span Gusset Plate
set   X_MGP1  15.2530;  set   Y_MGP1  15.2530;
set   X_MGP2  15.2530;  set   Y_MGP2  15.2530;
set   X_MGP3  15.2530;  set   Y_MGP3  15.2530;
set   X_MGP4  15.2530;  set   Y_MGP4  15.2530;
set   X_MGP5  15.2580;  set   Y_MGP5  15.2580;
set   X_MGP6  15.2580;  set   Y_MGP6  15.2580;
set   X_MGP7  15.3852;  set   Y_MGP7  15.3852;
set   X_MGP8  15.3852;  set   Y_MGP8  15.3852;
set   X_MGP9  14.9440;  set   Y_MGP9  14.9440;
set   X_MGP10  14.9440;  set   Y_MGP10  14.9440;
set   X_MGP11  14.1923;  set   Y_MGP11  14.1923;
set   X_MGP12  14.1923;  set   Y_MGP12  14.1923;

# FRAME GRID LINES
set Floor13  2160.00;
set Floor12  1980.00;
set Floor11  1800.00;
set Floor10  1620.00;
set Floor9  1440.00;
set Floor8  1260.00;
set Floor7  1080.00;
set Floor6  900.00;
set Floor5  720.00;
set Floor4  540.00;
set Floor3  360.00;
set Floor2  180.00;
set Floor1 0.0;

set Axis1 0.0;
set Axis2 360.00;
set Axis3 720.00;
set Axis4 1080.00;

set HBuilding 2160.00;
set WFrame 360.00;
variable HBuilding 2160.00;

####################################################################################################
#                                                  NODES                                           #
####################################################################################################

# COMMAND SYNTAX 
# node $NodeID  $X-Coordinate  $Y-Coordinate;

#SUPPORT NODES
node 110   $Axis1  $Floor1; node 120   $Axis2  $Floor1; node 130   $Axis3  $Floor1; node 140   $Axis4  $Floor1; 

# EGF COLUMN GRID NODES
node 1330   $Axis3  $Floor13; node 1340   $Axis4  $Floor13; 
node 1230   $Axis3  $Floor12; node 1240   $Axis4  $Floor12; 
node 1130   $Axis3  $Floor11; node 1140   $Axis4  $Floor11; 
node 1030   $Axis3  $Floor10; node 1040   $Axis4  $Floor10; 
node 930   $Axis3  $Floor9; node 940   $Axis4  $Floor9; 
node 830   $Axis3  $Floor8; node 840   $Axis4  $Floor8; 
node 730   $Axis3  $Floor7; node 740   $Axis4  $Floor7; 
node 630   $Axis3  $Floor6; node 640   $Axis4  $Floor6; 
node 530   $Axis3  $Floor5; node 540   $Axis4  $Floor5; 
node 430   $Axis3  $Floor4; node 440   $Axis4  $Floor4; 
node 330   $Axis3  $Floor3; node 340   $Axis4  $Floor3; 
node 230   $Axis3  $Floor2; node 240   $Axis4  $Floor2; 

# EGF COLUMN NODES
node 1331  $Axis3  $Floor13; node 1341  $Axis4  $Floor13; 
node 1233  $Axis3  $Floor12; node 1243  $Axis4  $Floor12; 
node 1231  $Axis3  $Floor12; node 1241  $Axis4  $Floor12; 
node 1133  $Axis3  $Floor11; node 1143  $Axis4  $Floor11; 
node 1131  $Axis3  $Floor11; node 1141  $Axis4  $Floor11; 
node 1033  $Axis3  $Floor10; node 1043  $Axis4  $Floor10; 
node 1031  $Axis3  $Floor10; node 1041  $Axis4  $Floor10; 
node 933  $Axis3  $Floor9; node 943  $Axis4  $Floor9; 
node 931  $Axis3  $Floor9; node 941  $Axis4  $Floor9; 
node 833  $Axis3  $Floor8; node 843  $Axis4  $Floor8; 
node 831  $Axis3  $Floor8; node 841  $Axis4  $Floor8; 
node 733  $Axis3  $Floor7; node 743  $Axis4  $Floor7; 
node 731  $Axis3  $Floor7; node 741  $Axis4  $Floor7; 
node 633  $Axis3  $Floor6; node 643  $Axis4  $Floor6; 
node 631  $Axis3  $Floor6; node 641  $Axis4  $Floor6; 
node 533  $Axis3  $Floor5; node 543  $Axis4  $Floor5; 
node 531  $Axis3  $Floor5; node 541  $Axis4  $Floor5; 
node 433  $Axis3  $Floor4; node 443  $Axis4  $Floor4; 
node 431  $Axis3  $Floor4; node 441  $Axis4  $Floor4; 
node 333  $Axis3  $Floor3; node 343  $Axis4  $Floor3; 
node 331  $Axis3  $Floor3; node 341  $Axis4  $Floor3; 
node 233  $Axis3  $Floor2; node 243  $Axis4  $Floor2; 
node 231  $Axis3  $Floor2; node 241  $Axis4  $Floor2; 
node 133  $Axis3  $Floor1; node 143  $Axis4  $Floor1; 

# EGF BEAM NODES
node 1334  $Axis3  $Floor13; node 1342  $Axis4  $Floor13; 
node 1234  $Axis3  $Floor12; node 1242  $Axis4  $Floor12; 
node 1134  $Axis3  $Floor11; node 1142  $Axis4  $Floor11; 
node 1034  $Axis3  $Floor10; node 1042  $Axis4  $Floor10; 
node 934  $Axis3  $Floor9; node 942  $Axis4  $Floor9; 
node 834  $Axis3  $Floor8; node 842  $Axis4  $Floor8; 
node 734  $Axis3  $Floor7; node 742  $Axis4  $Floor7; 
node 634  $Axis3  $Floor6; node 642  $Axis4  $Floor6; 
node 534  $Axis3  $Floor5; node 542  $Axis4  $Floor5; 
node 434  $Axis3  $Floor4; node 442  $Axis4  $Floor4; 
node 334  $Axis3  $Floor3; node 342  $Axis4  $Floor3; 
node 234  $Axis3  $Floor2; node 242  $Axis4  $Floor2; 

# MF COLUMN NODES
node 1311  $Axis1 [expr $Floor13 - 18.10/2]; node 1321  $Axis2 [expr $Floor13 - 18.10/2]; 
node 1213  $Axis1 [expr $Floor12 + 17.70/2]; node 1223  $Axis2 [expr $Floor12 + 17.70/2]; 
node 1211  $Axis1 [expr $Floor12 - 17.70/2]; node 1221  $Axis2 [expr $Floor12 - 17.70/2]; 
node 1113  $Axis1 [expr $Floor11 + 18.20/2]; node 1123  $Axis2 [expr $Floor11 + 18.20/2]; 
node 1111  $Axis1 [expr $Floor11 - 18.20/2]; node 1121  $Axis2 [expr $Floor11 - 18.20/2]; 
node 1013  $Axis1 [expr $Floor10 + 17.70/2]; node 1023  $Axis2 [expr $Floor10 + 17.70/2]; 
node 1011  $Axis1 [expr $Floor10 - 17.70/2]; node 1021  $Axis2 [expr $Floor10 - 17.70/2]; 
node 913  $Axis1 [expr $Floor9 + 18.40/2]; node 923  $Axis2 [expr $Floor9 + 18.40/2]; 
node 911  $Axis1 [expr $Floor9 - 18.40/2]; node 921  $Axis2 [expr $Floor9 - 18.40/2]; 
node 813  $Axis1 [expr $Floor8 + 17.70/2]; node 823  $Axis2 [expr $Floor8 + 17.70/2]; 
node 811  $Axis1 [expr $Floor8 - 17.70/2]; node 821  $Axis2 [expr $Floor8 - 17.70/2]; 
node 713  $Axis1 [expr $Floor7 + 18.40/2]; node 723  $Axis2 [expr $Floor7 + 18.40/2]; 
node 711  $Axis1 [expr $Floor7 - 18.40/2]; node 721  $Axis2 [expr $Floor7 - 18.40/2]; 
node 613  $Axis1 [expr $Floor6 + 17.70/2]; node 623  $Axis2 [expr $Floor6 + 17.70/2]; 
node 611  $Axis1 [expr $Floor6 - 17.70/2]; node 621  $Axis2 [expr $Floor6 - 17.70/2]; 
node 513  $Axis1 [expr $Floor5 + 18.50/2]; node 523  $Axis2 [expr $Floor5 + 18.50/2]; 
node 511  $Axis1 [expr $Floor5 - 18.50/2]; node 521  $Axis2 [expr $Floor5 - 18.50/2]; 
node 413  $Axis1 [expr $Floor4 + 17.70/2]; node 423  $Axis2 [expr $Floor4 + 17.70/2]; 
node 411  $Axis1 [expr $Floor4 - 17.70/2]; node 421  $Axis2 [expr $Floor4 - 17.70/2]; 
node 313  $Axis1 [expr $Floor3 + 18.50/2]; node 323  $Axis2 [expr $Floor3 + 18.50/2]; 
node 311  $Axis1 [expr $Floor3 - 18.50/2]; node 321  $Axis2 [expr $Floor3 - 18.50/2]; 
node 213  $Axis1 [expr $Floor2 + 17.70/2]; node 223  $Axis2 [expr $Floor2 + 17.70/2]; 
node 211  $Axis1 [expr $Floor2 - 17.70/2]; node 221  $Axis2 [expr $Floor2 - 17.70/2]; 
node 113  $Axis1 $Floor1; node 123  $Axis2 $Floor1; 

# MF BEAM NODES
node 1314   [expr $Axis1 + 12.10/2] $Floor13; node 1322   [expr $Axis2 - 12.10/2] $Floor13; 
node 1214   [expr $Axis1 + 14.20/2] $Floor12; node 1222   [expr $Axis2 - 14.20/2] $Floor12; 
node 1114   [expr $Axis1 + 14.20/2] $Floor11; node 1122   [expr $Axis2 - 14.20/2] $Floor11; 
node 1014   [expr $Axis1 + 15.50/2] $Floor10; node 1022   [expr $Axis2 - 15.50/2] $Floor10; 
node 914   [expr $Axis1 + 15.50/2] $Floor9; node 922   [expr $Axis2 - 15.50/2] $Floor9; 
node 814   [expr $Axis1 + 16.70/2] $Floor8; node 822   [expr $Axis2 - 16.70/2] $Floor8; 
node 714   [expr $Axis1 + 16.70/2] $Floor7; node 722   [expr $Axis2 - 16.70/2] $Floor7; 
node 614   [expr $Axis1 + 18.30/2] $Floor6; node 622   [expr $Axis2 - 18.30/2] $Floor6; 
node 514   [expr $Axis1 + 18.30/2] $Floor5; node 522   [expr $Axis2 - 18.30/2] $Floor5; 
node 414   [expr $Axis1 + 20.20/2] $Floor4; node 422   [expr $Axis2 - 20.20/2] $Floor4; 
node 314   [expr $Axis1 + 20.20/2] $Floor3; node 322   [expr $Axis2 - 20.20/2] $Floor3; 
node 214   [expr $Axis1 + 20.20/2] $Floor2; node 222   [expr $Axis2 - 20.20/2] $Floor2; 

# COLUMN SPLICE NODES
node 111172 $Axis1 [expr ($Floor11 + 0.50 * 180)]; node 111272 $Axis2 [expr ($Floor11 + 0.50 * 180)]; node 111372 $Axis3 [expr ($Floor11 + 0.50 * 180)]; node 111472 $Axis4 [expr ($Floor11 + 0.50 * 180)]; 
node 111171 $Axis1 [expr ($Floor11 + 0.50 * 180)]; node 111271 $Axis2 [expr ($Floor11 + 0.50 * 180)]; node 111371 $Axis3 [expr ($Floor11 + 0.50 * 180)]; node 111471 $Axis4 [expr ($Floor11 + 0.50 * 180)]; 
node 109172 $Axis1 [expr ($Floor9 + 0.50 * 180)]; node 109272 $Axis2 [expr ($Floor9 + 0.50 * 180)]; node 109372 $Axis3 [expr ($Floor9 + 0.50 * 180)]; node 109472 $Axis4 [expr ($Floor9 + 0.50 * 180)]; 
node 109171 $Axis1 [expr ($Floor9 + 0.50 * 180)]; node 109271 $Axis2 [expr ($Floor9 + 0.50 * 180)]; node 109371 $Axis3 [expr ($Floor9 + 0.50 * 180)]; node 109471 $Axis4 [expr ($Floor9 + 0.50 * 180)]; 
node 107172 $Axis1 [expr ($Floor7 + 0.50 * 180)]; node 107272 $Axis2 [expr ($Floor7 + 0.50 * 180)]; node 107372 $Axis3 [expr ($Floor7 + 0.50 * 180)]; node 107472 $Axis4 [expr ($Floor7 + 0.50 * 180)]; 
node 107171 $Axis1 [expr ($Floor7 + 0.50 * 180)]; node 107271 $Axis2 [expr ($Floor7 + 0.50 * 180)]; node 107371 $Axis3 [expr ($Floor7 + 0.50 * 180)]; node 107471 $Axis4 [expr ($Floor7 + 0.50 * 180)]; 
node 105172 $Axis1 [expr ($Floor5 + 0.50 * 180)]; node 105272 $Axis2 [expr ($Floor5 + 0.50 * 180)]; node 105372 $Axis3 [expr ($Floor5 + 0.50 * 180)]; node 105472 $Axis4 [expr ($Floor5 + 0.50 * 180)]; 
node 105171 $Axis1 [expr ($Floor5 + 0.50 * 180)]; node 105271 $Axis2 [expr ($Floor5 + 0.50 * 180)]; node 105371 $Axis3 [expr ($Floor5 + 0.50 * 180)]; node 105471 $Axis4 [expr ($Floor5 + 0.50 * 180)]; 
node 103172 $Axis1 [expr ($Floor3 + 0.50 * 180)]; node 103272 $Axis2 [expr ($Floor3 + 0.50 * 180)]; node 103372 $Axis3 [expr ($Floor3 + 0.50 * 180)]; node 103472 $Axis4 [expr ($Floor3 + 0.50 * 180)]; 
node 103171 $Axis1 [expr ($Floor3 + 0.50 * 180)]; node 103271 $Axis2 [expr ($Floor3 + 0.50 * 180)]; node 103371 $Axis3 [expr ($Floor3 + 0.50 * 180)]; node 103471 $Axis4 [expr ($Floor3 + 0.50 * 180)]; 

# MID-SPAN GUSSET PLATE RIGID OFFSET NODES
node 212101   [expr ($Axis1 + $Axis2)/2] $Floor12;
node 212102   [expr ($Axis1 + $Axis2)/2 - 50.7468/2] $Floor12;
node 212112   [expr ($Axis1 + $Axis2)/2 - 50.7468/2] $Floor12;
node 212105   [expr ($Axis1 + $Axis2)/2 + 50.7468/2] $Floor12;
node 212115   [expr ($Axis1 + $Axis2)/2 + 50.7468/2] $Floor12;
node 212104   [expr ($Axis1 + $Axis2)/2 + $X_MGP11] [expr $Floor12 - $Y_MGP11];
node 212114   [expr ($Axis1 + $Axis2)/2 + $X_MGP11] [expr $Floor12 - $Y_MGP11];
node 212103   [expr ($Axis1 + $Axis2)/2 - $X_MGP11] [expr $Floor12 - $Y_MGP11];
node 212113   [expr ($Axis1 + $Axis2)/2 - $X_MGP11] [expr $Floor12 - $Y_MGP11];
node 212106   [expr ($Axis1 + $Axis2)/2 + $X_MGP12] [expr $Floor12 + $Y_MGP12];
node 212116   [expr ($Axis1 + $Axis2)/2 + $X_MGP12] [expr $Floor12 + $Y_MGP12];
node 212107   [expr ($Axis1 + $Axis2)/2 - $X_MGP12] [expr $Floor12 + $Y_MGP12];
node 212117   [expr ($Axis1 + $Axis2)/2 - $X_MGP12] [expr $Floor12 + $Y_MGP12];
node 210101   [expr ($Axis1 + $Axis2)/2] $Floor10;
node 210102   [expr ($Axis1 + $Axis2)/2 - 59.4089/2] $Floor10;
node 210112   [expr ($Axis1 + $Axis2)/2 - 59.4089/2] $Floor10;
node 210105   [expr ($Axis1 + $Axis2)/2 + 59.4089/2] $Floor10;
node 210115   [expr ($Axis1 + $Axis2)/2 + 59.4089/2] $Floor10;
node 210104   [expr ($Axis1 + $Axis2)/2 + $X_MGP9] [expr $Floor10 - $Y_MGP9];
node 210114   [expr ($Axis1 + $Axis2)/2 + $X_MGP9] [expr $Floor10 - $Y_MGP9];
node 210103   [expr ($Axis1 + $Axis2)/2 - $X_MGP9] [expr $Floor10 - $Y_MGP9];
node 210113   [expr ($Axis1 + $Axis2)/2 - $X_MGP9] [expr $Floor10 - $Y_MGP9];
node 210106   [expr ($Axis1 + $Axis2)/2 + $X_MGP10] [expr $Floor10 + $Y_MGP10];
node 210116   [expr ($Axis1 + $Axis2)/2 + $X_MGP10] [expr $Floor10 + $Y_MGP10];
node 210107   [expr ($Axis1 + $Axis2)/2 - $X_MGP10] [expr $Floor10 + $Y_MGP10];
node 210117   [expr ($Axis1 + $Axis2)/2 - $X_MGP10] [expr $Floor10 + $Y_MGP10];
node 208101   [expr ($Axis1 + $Axis2)/2] $Floor8;
node 208102   [expr ($Axis1 + $Axis2)/2 - 68.2477/2] $Floor8;
node 208112   [expr ($Axis1 + $Axis2)/2 - 68.2477/2] $Floor8;
node 208105   [expr ($Axis1 + $Axis2)/2 + 68.2477/2] $Floor8;
node 208115   [expr ($Axis1 + $Axis2)/2 + 68.2477/2] $Floor8;
node 208104   [expr ($Axis1 + $Axis2)/2 + $X_MGP7] [expr $Floor8 - $Y_MGP7];
node 208114   [expr ($Axis1 + $Axis2)/2 + $X_MGP7] [expr $Floor8 - $Y_MGP7];
node 208103   [expr ($Axis1 + $Axis2)/2 - $X_MGP7] [expr $Floor8 - $Y_MGP7];
node 208113   [expr ($Axis1 + $Axis2)/2 - $X_MGP7] [expr $Floor8 - $Y_MGP7];
node 208106   [expr ($Axis1 + $Axis2)/2 + $X_MGP8] [expr $Floor8 + $Y_MGP8];
node 208116   [expr ($Axis1 + $Axis2)/2 + $X_MGP8] [expr $Floor8 + $Y_MGP8];
node 208107   [expr ($Axis1 + $Axis2)/2 - $X_MGP8] [expr $Floor8 + $Y_MGP8];
node 208117   [expr ($Axis1 + $Axis2)/2 - $X_MGP8] [expr $Floor8 + $Y_MGP8];
node 206101   [expr ($Axis1 + $Axis2)/2] $Floor6;
node 206102   [expr ($Axis1 + $Axis2)/2 - 68.2477/2] $Floor6;
node 206112   [expr ($Axis1 + $Axis2)/2 - 68.2477/2] $Floor6;
node 206105   [expr ($Axis1 + $Axis2)/2 + 68.2477/2] $Floor6;
node 206115   [expr ($Axis1 + $Axis2)/2 + 68.2477/2] $Floor6;
node 206104   [expr ($Axis1 + $Axis2)/2 + $X_MGP5] [expr $Floor6 - $Y_MGP5];
node 206114   [expr ($Axis1 + $Axis2)/2 + $X_MGP5] [expr $Floor6 - $Y_MGP5];
node 206103   [expr ($Axis1 + $Axis2)/2 - $X_MGP5] [expr $Floor6 - $Y_MGP5];
node 206113   [expr ($Axis1 + $Axis2)/2 - $X_MGP5] [expr $Floor6 - $Y_MGP5];
node 206106   [expr ($Axis1 + $Axis2)/2 + $X_MGP6] [expr $Floor6 + $Y_MGP6];
node 206116   [expr ($Axis1 + $Axis2)/2 + $X_MGP6] [expr $Floor6 + $Y_MGP6];
node 206107   [expr ($Axis1 + $Axis2)/2 - $X_MGP6] [expr $Floor6 + $Y_MGP6];
node 206117   [expr ($Axis1 + $Axis2)/2 - $X_MGP6] [expr $Floor6 + $Y_MGP6];
node 204101   [expr ($Axis1 + $Axis2)/2] $Floor4;
node 204102   [expr ($Axis1 + $Axis2)/2 - 74.7885/2] $Floor4;
node 204112   [expr ($Axis1 + $Axis2)/2 - 74.7885/2] $Floor4;
node 204105   [expr ($Axis1 + $Axis2)/2 + 74.7885/2] $Floor4;
node 204115   [expr ($Axis1 + $Axis2)/2 + 74.7885/2] $Floor4;
node 204104   [expr ($Axis1 + $Axis2)/2 + $X_MGP3] [expr $Floor4 - $Y_MGP3];
node 204114   [expr ($Axis1 + $Axis2)/2 + $X_MGP3] [expr $Floor4 - $Y_MGP3];
node 204103   [expr ($Axis1 + $Axis2)/2 - $X_MGP3] [expr $Floor4 - $Y_MGP3];
node 204113   [expr ($Axis1 + $Axis2)/2 - $X_MGP3] [expr $Floor4 - $Y_MGP3];
node 204106   [expr ($Axis1 + $Axis2)/2 + $X_MGP4] [expr $Floor4 + $Y_MGP4];
node 204116   [expr ($Axis1 + $Axis2)/2 + $X_MGP4] [expr $Floor4 + $Y_MGP4];
node 204107   [expr ($Axis1 + $Axis2)/2 - $X_MGP4] [expr $Floor4 + $Y_MGP4];
node 204117   [expr ($Axis1 + $Axis2)/2 - $X_MGP4] [expr $Floor4 + $Y_MGP4];
node 202101   [expr ($Axis1 + $Axis2)/2] $Floor2;
node 202102   [expr ($Axis1 + $Axis2)/2 - 74.2086/2] $Floor2;
node 202112   [expr ($Axis1 + $Axis2)/2 - 74.2086/2] $Floor2;
node 202105   [expr ($Axis1 + $Axis2)/2 + 74.2086/2] $Floor2;
node 202115   [expr ($Axis1 + $Axis2)/2 + 74.2086/2] $Floor2;
node 202104   [expr ($Axis1 + $Axis2)/2 + $X_MGP1] [expr $Floor2 - $Y_MGP1];
node 202114   [expr ($Axis1 + $Axis2)/2 + $X_MGP1] [expr $Floor2 - $Y_MGP1];
node 202103   [expr ($Axis1 + $Axis2)/2 - $X_MGP1] [expr $Floor2 - $Y_MGP1];
node 202113   [expr ($Axis1 + $Axis2)/2 - $X_MGP1] [expr $Floor2 - $Y_MGP1];
node 202106   [expr ($Axis1 + $Axis2)/2 + $X_MGP2] [expr $Floor2 + $Y_MGP2];
node 202116   [expr ($Axis1 + $Axis2)/2 + $X_MGP2] [expr $Floor2 + $Y_MGP2];
node 202107   [expr ($Axis1 + $Axis2)/2 - $X_MGP2] [expr $Floor2 + $Y_MGP2];
node 202117   [expr ($Axis1 + $Axis2)/2 - $X_MGP2] [expr $Floor2 + $Y_MGP2];

# CORNER X-BRACING RIGID OFFSET NODES
node 113150   [expr $Axis1 + $X_CGP12] [expr $Floor13 - $Y_CGP12];
node 113151   [expr $Axis1 + $X_CGP12] [expr $Floor13 - $Y_CGP12];
node 113250   [expr $Axis2 - $X_CGP12] [expr $Floor13 - $Y_CGP12];
node 113251   [expr $Axis2 - $X_CGP12] [expr $Floor13 - $Y_CGP12];
node 111140   [expr $Axis1 + $X_CGP11] [expr $Floor11 + $Y_CGP11];
node 111141   [expr $Axis1 + $X_CGP11] [expr $Floor11 + $Y_CGP11];
node 111150   [expr $Axis1 + $X_CGP10] [expr $Floor11 - $Y_CGP10];
node 111151   [expr $Axis1 + $X_CGP10] [expr $Floor11 - $Y_CGP10];
node 111240   [expr $Axis2 - $X_CGP11] [expr $Floor11 + $Y_CGP11];
node 111241   [expr $Axis2 - $X_CGP11] [expr $Floor11 + $Y_CGP11];
node 111250   [expr $Axis2 - $X_CGP10] [expr $Floor11 - $Y_CGP10];
node 111251   [expr $Axis2 - $X_CGP10] [expr $Floor11 - $Y_CGP10];
node 109140   [expr $Axis1 + $X_CGP9] [expr $Floor9 + $Y_CGP9];
node 109141   [expr $Axis1 + $X_CGP9] [expr $Floor9 + $Y_CGP9];
node 109150   [expr $Axis1 + $X_CGP8] [expr $Floor9 - $Y_CGP8];
node 109151   [expr $Axis1 + $X_CGP8] [expr $Floor9 - $Y_CGP8];
node 109240   [expr $Axis2 - $X_CGP9] [expr $Floor9 + $Y_CGP9];
node 109241   [expr $Axis2 - $X_CGP9] [expr $Floor9 + $Y_CGP9];
node 109250   [expr $Axis2 - $X_CGP8] [expr $Floor9 - $Y_CGP8];
node 109251   [expr $Axis2 - $X_CGP8] [expr $Floor9 - $Y_CGP8];
node 107140   [expr $Axis1 + $X_CGP7] [expr $Floor7 + $Y_CGP7];
node 107141   [expr $Axis1 + $X_CGP7] [expr $Floor7 + $Y_CGP7];
node 107150   [expr $Axis1 + $X_CGP6] [expr $Floor7 - $Y_CGP6];
node 107151   [expr $Axis1 + $X_CGP6] [expr $Floor7 - $Y_CGP6];
node 107240   [expr $Axis2 - $X_CGP7] [expr $Floor7 + $Y_CGP7];
node 107241   [expr $Axis2 - $X_CGP7] [expr $Floor7 + $Y_CGP7];
node 107250   [expr $Axis2 - $X_CGP6] [expr $Floor7 - $Y_CGP6];
node 107251   [expr $Axis2 - $X_CGP6] [expr $Floor7 - $Y_CGP6];
node 105140   [expr $Axis1 + $X_CGP5] [expr $Floor5 + $Y_CGP5];
node 105141   [expr $Axis1 + $X_CGP5] [expr $Floor5 + $Y_CGP5];
node 105150   [expr $Axis1 + $X_CGP4] [expr $Floor5 - $Y_CGP4];
node 105151   [expr $Axis1 + $X_CGP4] [expr $Floor5 - $Y_CGP4];
node 105240   [expr $Axis2 - $X_CGP5] [expr $Floor5 + $Y_CGP5];
node 105241   [expr $Axis2 - $X_CGP5] [expr $Floor5 + $Y_CGP5];
node 105250   [expr $Axis2 - $X_CGP4] [expr $Floor5 - $Y_CGP4];
node 105251   [expr $Axis2 - $X_CGP4] [expr $Floor5 - $Y_CGP4];
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
ConstructPanel_Rectangle  1 13 $Axis1 $Floor13 $E $A_Stiff $I_Stiff 12.10 18.10 $trans_selected; ConstructPanel_Rectangle  2 13 $Axis2 $Floor13 $E $A_Stiff $I_Stiff 12.10 18.10 $trans_selected; 
ConstructPanel_Rectangle  1 12 $Axis1 $Floor12 $E $A_Stiff $I_Stiff 14.20 17.70 $trans_selected; ConstructPanel_Rectangle  2 12 $Axis2 $Floor12 $E $A_Stiff $I_Stiff 14.20 17.70 $trans_selected; 
ConstructPanel_Rectangle  1 11 $Axis1 $Floor11 $E $A_Stiff $I_Stiff 14.20 18.20 $trans_selected; ConstructPanel_Rectangle  2 11 $Axis2 $Floor11 $E $A_Stiff $I_Stiff 14.20 18.20 $trans_selected; 
ConstructPanel_Rectangle  1 10 $Axis1 $Floor10 $E $A_Stiff $I_Stiff 15.50 17.70 $trans_selected; ConstructPanel_Rectangle  2 10 $Axis2 $Floor10 $E $A_Stiff $I_Stiff 15.50 17.70 $trans_selected; 
ConstructPanel_Rectangle  1 9 $Axis1 $Floor9 $E $A_Stiff $I_Stiff 15.50 18.40 $trans_selected; ConstructPanel_Rectangle  2 9 $Axis2 $Floor9 $E $A_Stiff $I_Stiff 15.50 18.40 $trans_selected; 
ConstructPanel_Rectangle  1 8 $Axis1 $Floor8 $E $A_Stiff $I_Stiff 16.70 17.70 $trans_selected; ConstructPanel_Rectangle  2 8 $Axis2 $Floor8 $E $A_Stiff $I_Stiff 16.70 17.70 $trans_selected; 
ConstructPanel_Rectangle  1 7 $Axis1 $Floor7 $E $A_Stiff $I_Stiff 16.70 18.40 $trans_selected; ConstructPanel_Rectangle  2 7 $Axis2 $Floor7 $E $A_Stiff $I_Stiff 16.70 18.40 $trans_selected; 
ConstructPanel_Rectangle  1 6 $Axis1 $Floor6 $E $A_Stiff $I_Stiff 18.30 17.70 $trans_selected; ConstructPanel_Rectangle  2 6 $Axis2 $Floor6 $E $A_Stiff $I_Stiff 18.30 17.70 $trans_selected; 
ConstructPanel_Rectangle  1 5 $Axis1 $Floor5 $E $A_Stiff $I_Stiff 18.30 18.50 $trans_selected; ConstructPanel_Rectangle  2 5 $Axis2 $Floor5 $E $A_Stiff $I_Stiff 18.30 18.50 $trans_selected; 
ConstructPanel_Rectangle  1 4 $Axis1 $Floor4 $E $A_Stiff $I_Stiff 20.20 17.70 $trans_selected; ConstructPanel_Rectangle  2 4 $Axis2 $Floor4 $E $A_Stiff $I_Stiff 20.20 17.70 $trans_selected; 
ConstructPanel_Rectangle  1 3 $Axis1 $Floor3 $E $A_Stiff $I_Stiff 20.20 18.50 $trans_selected; ConstructPanel_Rectangle  2 3 $Axis2 $Floor3 $E $A_Stiff $I_Stiff 20.20 18.50 $trans_selected; 
ConstructPanel_Rectangle  1 2 $Axis1 $Floor2 $E $A_Stiff $I_Stiff 20.20 17.70 $trans_selected; ConstructPanel_Rectangle  2 2 $Axis2 $Floor2 $E $A_Stiff $I_Stiff 20.20 17.70 $trans_selected; 

####################################################################################################
#                                          PANEL ZONE SPRINGS                                      #
####################################################################################################

# COMMAND SYNTAX 
# Spring_PZ    Element_ID Node_i Node_j E mu fy tw_Col tdp d_Col d_Beam tf_Col bf_Col Ic trib ts Response_ID transfTag
Spring_PZ    913100 413109 413110 $E $mu [expr $fy *   1.0]  0.34   0.00 12.10 18.10  0.57  8.05 348.00 3.500 4.000 2 1; Spring_PZ    913200 413209 413210 $E $mu [expr $fy *   1.0]  0.34   0.00 12.10 18.10  0.57  8.05 348.00 3.500 4.000 2 1; 
Spring_PZ    912100 412109 412110 $E $mu [expr $fy *   1.0]  0.34   0.00 12.10 17.70  0.57  8.05 348.00 3.500 4.000 2 1; Spring_PZ    912200 412209 412210 $E $mu [expr $fy *   1.0]  0.34   0.00 12.10 17.70  0.57  8.05 348.00 3.500 4.000 2 1; 
Spring_PZ    911100 411109 411110 $E $mu [expr $fy *   1.0]  0.48   0.00 14.20 18.20  0.78 14.60 1110.00 3.500 4.000 2 1; Spring_PZ    911200 411209 411210 $E $mu [expr $fy *   1.0]  0.48   0.00 14.20 18.20  0.78 14.60 1110.00 3.500 4.000 2 1; 
Spring_PZ    910100 410109 410110 $E $mu [expr $fy *   1.0]  0.48   0.00 14.20 17.70  0.78 14.60 1110.00 3.500 4.000 2 1; Spring_PZ    910200 410209 410210 $E $mu [expr $fy *   1.0]  0.48   0.00 14.20 17.70  0.78 14.60 1110.00 3.500 4.000 2 1; 
Spring_PZ    909100 409109 409110 $E $mu [expr $fy *   1.0]  0.89   0.00 15.50 18.40  1.44 15.70 2400.00 3.500 4.000 2 1; Spring_PZ    909200 409209 409210 $E $mu [expr $fy *   1.0]  0.89   0.00 15.50 18.40  1.44 15.70 2400.00 3.500 4.000 2 1; 
Spring_PZ    908100 408109 408110 $E $mu [expr $fy *   1.0]  0.89   0.00 15.50 17.70  1.44 15.70 2400.00 3.500 4.000 2 1; Spring_PZ    908200 408209 408210 $E $mu [expr $fy *   1.0]  0.89   0.00 15.50 17.70  1.44 15.70 2400.00 3.500 4.000 2 1; 
Spring_PZ    907100 407109 407110 $E $mu [expr $fy *   1.0]  1.29   0.00 16.70 18.40  2.07 16.10 3840.00 3.500 4.000 2 1; Spring_PZ    907200 407209 407210 $E $mu [expr $fy *   1.0]  1.29   0.00 16.70 18.40  2.07 16.10 3840.00 3.500 4.000 2 1; 
Spring_PZ    906100 406109 406110 $E $mu [expr $fy *   1.0]  1.29   0.00 16.70 17.70  2.07 16.10 3840.00 3.500 4.000 2 1; Spring_PZ    906200 406209 406210 $E $mu [expr $fy *   1.0]  1.29   0.00 16.70 17.70  2.07 16.10 3840.00 3.500 4.000 2 1; 
Spring_PZ    905100 405109 405110 $E $mu [expr $fy *   1.0]  1.77   0.00 18.30 18.50  2.85 16.60 6000.00 3.500 4.000 2 1; Spring_PZ    905200 405209 405210 $E $mu [expr $fy *   1.0]  1.77   0.00 18.30 18.50  2.85 16.60 6000.00 3.500 4.000 2 1; 
Spring_PZ    904100 404109 404110 $E $mu [expr $fy *   1.0]  1.77   0.00 18.30 17.70  2.85 16.60 6000.00 3.500 4.000 2 1; Spring_PZ    904200 404209 404210 $E $mu [expr $fy *   1.0]  1.77   0.00 18.30 17.70  2.85 16.60 6000.00 3.500 4.000 2 1; 
Spring_PZ    903100 403109 403110 $E $mu [expr $fy *   1.0]  2.38   0.00 20.20 18.50  3.82 17.20 9430.00 3.500 4.000 2 1; Spring_PZ    903200 403209 403210 $E $mu [expr $fy *   1.0]  2.38   0.00 20.20 18.50  3.82 17.20 9430.00 3.500 4.000 2 1; 
Spring_PZ    902100 402109 402110 $E $mu [expr $fy *   1.0]  2.38   0.00 20.20 17.70  3.82 17.20 9430.00 3.500 4.000 2 1; Spring_PZ    902200 402209 402210 $E $mu [expr $fy *   1.0]  2.38   0.00 20.20 17.70  3.82 17.20 9430.00 3.500 4.000 2 1; 

####################################################################################################
#                                          RIGID BRACE LINKS                                       #
####################################################################################################

# COMMAND SYNTAX 
# element elasticBeamColumn $ElementID $NodeIDi $NodeIDj $Area $E $Inertia $transformation;

# MIDDLE RIGID LINKS

element elasticBeamColumn 712122 212101 212102 $A_Stiff $E $I_Stiff  $trans_selected;
element elasticBeamColumn 712133 212101 212103 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 712144 212101 212104 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 712155 212101 212105 $A_Stiff $E $I_Stiff  $trans_selected;
element elasticBeamColumn 712166 212101 212106 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 712177 212101 212107 $A_Stiff $E $I_Stiff  $trans_Corot;


element elasticBeamColumn 710122 210101 210102 $A_Stiff $E $I_Stiff  $trans_selected;
element elasticBeamColumn 710133 210101 210103 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 710144 210101 210104 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 710155 210101 210105 $A_Stiff $E $I_Stiff  $trans_selected;
element elasticBeamColumn 710166 210101 210106 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 710177 210101 210107 $A_Stiff $E $I_Stiff  $trans_Corot;


element elasticBeamColumn 708122 208101 208102 $A_Stiff $E $I_Stiff  $trans_selected;
element elasticBeamColumn 708133 208101 208103 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 708144 208101 208104 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 708155 208101 208105 $A_Stiff $E $I_Stiff  $trans_selected;
element elasticBeamColumn 708166 208101 208106 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 708177 208101 208107 $A_Stiff $E $I_Stiff  $trans_Corot;


element elasticBeamColumn 706122 206101 206102 $A_Stiff $E $I_Stiff  $trans_selected;
element elasticBeamColumn 706133 206101 206103 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 706144 206101 206104 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 706155 206101 206105 $A_Stiff $E $I_Stiff  $trans_selected;
element elasticBeamColumn 706166 206101 206106 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 706177 206101 206107 $A_Stiff $E $I_Stiff  $trans_Corot;


element elasticBeamColumn 704122 204101 204102 $A_Stiff $E $I_Stiff  $trans_selected;
element elasticBeamColumn 704133 204101 204103 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 704144 204101 204104 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 704155 204101 204105 $A_Stiff $E $I_Stiff  $trans_selected;
element elasticBeamColumn 704166 204101 204106 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 704177 204101 204107 $A_Stiff $E $I_Stiff  $trans_Corot;


element elasticBeamColumn 702122 202101 202102 $A_Stiff $E $I_Stiff  $trans_selected;
element elasticBeamColumn 702133 202101 202103 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 702144 202101 202104 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 702155 202101 202105 $A_Stiff $E $I_Stiff  $trans_selected;
element elasticBeamColumn 702166 202101 202106 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 702177 202101 202107 $A_Stiff $E $I_Stiff  $trans_Corot;


# CORNER RIGID LINKS
element elasticBeamColumn 713199 413199 113150 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 713299 413206 113250 $A_Stiff $E $I_Stiff  $trans_Corot;

element elasticBeamColumn 711111 411110 111140 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 711199 411199 111150 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 711211 411208 111240 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 711299 411206 111250 $A_Stiff $E $I_Stiff  $trans_Corot;

element elasticBeamColumn 709111 409110 109140 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 709199 409199 109150 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 709211 409208 109240 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 709299 409206 109250 $A_Stiff $E $I_Stiff  $trans_Corot;

element elasticBeamColumn 707111 407110 107140 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 707199 407199 107150 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 707211 407208 107240 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 707299 407206 107250 $A_Stiff $E $I_Stiff  $trans_Corot;

element elasticBeamColumn 705111 405110 105140 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 705199 405199 105150 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 705211 405208 105240 $A_Stiff $E $I_Stiff  $trans_Corot;
element elasticBeamColumn 705299 405206 105250 $A_Stiff $E $I_Stiff  $trans_Corot;

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
Spring_Gusset 912133 212113 212103 $E $fyG 7.7555 0.5000 10.0000 6.6300  4000;
Spring_Gusset 912144 212114 212104 $E $fyG 7.7555 0.5000 10.0000 6.6300  4001;
Spring_Gusset 912166 212116 212106 $E $fyG 7.7555 0.5000 10.0000 6.6300  4002;
Spring_Gusset 912177 212117 212107 $E $fyG 7.7555 0.5000 10.0000 6.6300  4003;

Spring_Gusset 910133 210113 210103 $E $fyG 8.8180 0.5000 14.0000 8.7500  4004;
Spring_Gusset 910144 210114 210104 $E $fyG 8.8180 0.5000 14.0000 8.7500  4005;
Spring_Gusset 910166 210116 210106 $E $fyG 8.8180 0.5000 14.0000 8.7500  4006;
Spring_Gusset 910177 210117 210107 $E $fyG 8.8180 0.5000 14.0000 8.7500  4007;

Spring_Gusset 908133 208113 208103 $E $fyG 9.4430 0.5000 19.0000 10.0000  4008;
Spring_Gusset 908144 208114 208104 $E $fyG 9.4430 0.5000 19.0000 10.0000  4009;
Spring_Gusset 908166 208116 208106 $E $fyG 9.4430 0.5000 19.0000 10.0000  4010;
Spring_Gusset 908177 208117 208107 $E $fyG 9.4430 0.5000 19.0000 10.0000  4011;

Spring_Gusset 906133 206113 206103 $E $fyG 9.4430 0.5000 19.0000 10.0000  4012;
Spring_Gusset 906144 206114 206104 $E $fyG 9.4430 0.5000 19.0000 10.0000  4013;
Spring_Gusset 906166 206116 206106 $E $fyG 9.4430 0.5000 19.0000 10.0000  4014;
Spring_Gusset 906177 206117 206107 $E $fyG 9.4430 0.5000 19.0000 10.0000  4015;

Spring_Gusset 904133 204113 204103 $E $fyG 9.2555 0.5000 24.0000 9.6300  4016;
Spring_Gusset 904144 204114 204104 $E $fyG 9.2555 0.5000 24.0000 9.6300  4017;
Spring_Gusset 904166 204116 204106 $E $fyG 9.2555 0.5000 24.0000 9.6300  4018;
Spring_Gusset 904177 204117 204107 $E $fyG 9.2555 0.5000 24.0000 9.6300  4019;

Spring_Gusset 902133 202113 202103 $E $fyG 9.2555 0.5000 23.5900 9.6300  4020;
Spring_Gusset 902144 202114 202104 $E $fyG 9.2555 0.5000 23.5900 9.6300  4021;
Spring_Gusset 902166 202116 202106 $E $fyG 9.2555 0.5000 23.5900 9.6300  4022;
Spring_Gusset 902177 202117 202107 $E $fyG 9.2555 0.5000 23.5900 9.6300  4023;


# CORNER GUSSET PLATE SPRINGS
Spring_Gusset 913199 113150 113151 $E $fyG 3.8610 0.5000 10.0000 6.6300  4024;
Spring_Gusset 913299 113250 113251 $E $fyG 3.8610 0.5000 10.0000 6.6300  4025;

Spring_Gusset 911111 111140 111141 $E $fyG 7.3413 0.5000 10.0000 6.6300  4026;
Spring_Gusset 911199 111150 111151 $E $fyG 7.7502 0.5000 14.0000 8.7500  4027;
Spring_Gusset 911211 111240 111241 $E $fyG 7.3413 0.5000 10.0000 6.6300  4028;
Spring_Gusset 911299 111250 111251 $E $fyG 7.7502 0.5000 14.0000 8.7500  4029;

Spring_Gusset 909111 109140 109141 $E $fyG 7.4910 0.5000 14.0000 8.7500  4030;
Spring_Gusset 909199 109150 109151 $E $fyG 7.2209 0.5000 19.0000 10.0000  4031;
Spring_Gusset 909211 109240 109241 $E $fyG 7.4910 0.5000 14.0000 8.7500  4032;
Spring_Gusset 909299 109250 109251 $E $fyG 7.2209 0.5000 19.0000 10.0000  4033;

Spring_Gusset 907111 107140 107141 $E $fyG 6.9380 0.5000 19.0000 10.0000  4034;
Spring_Gusset 907199 107150 107151 $E $fyG 6.9380 0.5000 19.0000 10.0000  4035;
Spring_Gusset 907211 107240 107241 $E $fyG 6.9380 0.5000 19.0000 10.0000  4036;
Spring_Gusset 907299 107250 107251 $E $fyG 6.9380 0.5000 19.0000 10.0000  4037;

Spring_Gusset 905111 105140 105141 $E $fyG 7.9987 0.5000 19.0000 10.0000  4038;
Spring_Gusset 905199 105150 105151 $E $fyG 9.2715 0.5000 24.0000 9.6300  4039;
Spring_Gusset 905211 105240 105241 $E $fyG 7.9987 0.5000 19.0000 10.0000  4040;
Spring_Gusset 905299 105250 105251 $E $fyG 9.2715 0.5000 24.0000 9.6300  4041;

Spring_Gusset 903111 103140 103141 $E $fyG 7.8360 0.5000 24.0000 9.6300  4042;
Spring_Gusset 903199 103150 103151 $E $fyG 7.8360 0.5000 24.0000 9.6300  4043;
Spring_Gusset 903211 103240 103241 $E $fyG 7.8360 0.5000 24.0000 9.6300  4044;
Spring_Gusset 903299 103250 103251 $E $fyG 7.8360 0.5000 24.0000 9.6300  4045;

Spring_Gusset 901111 101140 101141 $E $fyG 11.6650 0.5000 23.5900 9.6300  4046;
Spring_Gusset 901211 101240 101241 $E $fyG 11.6650 0.5000 23.5900 9.6300  4047;


####################################################################################################
#                                 BRACE MEMBERS WITH FATIGUE MATERIAL                              #
####################################################################################################

# CREATE FATIGUE MATERIALS
# COMMAND SYNTAX 
# FatigueMat $MatID $BraceSecType $fy $E $L_brace $ry_brace $ht_brace $htw_brace $bftf_brace;
FatigueMat 100 2 $fyB $E 198.0977 3.2400 20.7000  0.0 0.0;
FatigueMat 102 2 $fyB $E 198.8228 3.2400 20.7000  0.0 0.0;
FatigueMat 104 2 $fyB $E 198.8228 3.2400 20.7000  0.0 0.0;
FatigueMat 106 2 $fyB $E 198.2370 3.2400 20.7000  0.0 0.0;
FatigueMat 108 2 $fyB $E 201.1206 3.4100 28.7000  0.0 0.0;
FatigueMat 110 2 $fyB $E 202.6055 3.4100 28.7000  0.0 0.0;
FatigueMat 112 2 $fyB $E 202.6055 3.4100 28.7000  0.0 0.0;
FatigueMat 114 2 $fyB $E 202.6055 3.4100 28.7000  0.0 0.0;
FatigueMat 116 2 $fyB $E 205.3015 2.9900 30.1000  0.0 0.0;
FatigueMat 118 2 $fyB $E 205.4430 2.9900 30.1000  0.0 0.0;
FatigueMat 120 2 $fyB $E 209.1623 2.2400 22.8000  0.0 0.0;
FatigueMat 122 2 $fyB $E 213.4757 2.2400 22.8000  0.0 0.0;

# CREATE THE BRACE SECTIONS
# COMMAND SYNTAX 
# FiberRHSS $BraceSecType $FatigueMatID $h_brace $t_brace $nFiber $nFiber $nFiber $nFiber;
FiberCHSS     1   101 9.6300 0.5000 12 4; 
FiberCHSS     2   103 9.6300 0.5000 12 4; 
FiberCHSS     3   105 9.6300 0.5000 12 4; 
FiberCHSS     4   107 9.6300 0.5000 12 4; 
FiberCHSS     5   109 10.0000 0.3750 12 4; 
FiberCHSS     6   111 10.0000 0.3750 12 4; 
FiberCHSS     7   113 10.0000 0.3750 12 4; 
FiberCHSS     8   115 10.0000 0.3750 12 4; 
FiberCHSS     9   117 8.7500 0.3120 12 4; 
FiberCHSS    10   119 8.7500 0.3120 12 4; 
FiberCHSS    11   121 6.6300 0.3120 12 4; 
FiberCHSS    12   123 6.6300 0.3120 12 4; 

# CONSTRUCT THE BRACE MEMBERS
# COMMAND SYNTAX 
# ConstructBrace $BraceID $NodeIDi $NodeIDj $nSegments $Imperfeection $nIntgeration $transformation;
ConstructBrace 8101100   101141   202113     1   $nSegments $initialGI $nIntegration  $trans_Corot;
ConstructBrace 8201100   101241   202114     1   $nSegments $initialGI $nIntegration  $trans_Corot;

ConstructBrace 8102100   103151   202117     2   $nSegments $initialGI $nIntegration  $trans_Corot;
ConstructBrace 8202100   103251   202116     2   $nSegments $initialGI $nIntegration  $trans_Corot;

ConstructBrace 8103100   103141   204113     3   $nSegments $initialGI $nIntegration  $trans_Corot;
ConstructBrace 8203100   103241   204114     3   $nSegments $initialGI $nIntegration  $trans_Corot;

ConstructBrace 8104100   105151   204117     4   $nSegments $initialGI $nIntegration  $trans_Corot;
ConstructBrace 8204100   105251   204116     4   $nSegments $initialGI $nIntegration  $trans_Corot;

ConstructBrace 8105100   105141   206113     5   $nSegments $initialGI $nIntegration  $trans_Corot;
ConstructBrace 8205100   105241   206114     5   $nSegments $initialGI $nIntegration  $trans_Corot;

ConstructBrace 8106100   107151   206117     6   $nSegments $initialGI $nIntegration  $trans_Corot;
ConstructBrace 8206100   107251   206116     6   $nSegments $initialGI $nIntegration  $trans_Corot;

ConstructBrace 8107100   107141   208113     7   $nSegments $initialGI $nIntegration  $trans_Corot;
ConstructBrace 8207100   107241   208114     7   $nSegments $initialGI $nIntegration  $trans_Corot;

ConstructBrace 8108100   109151   208117     8   $nSegments $initialGI $nIntegration  $trans_Corot;
ConstructBrace 8208100   109251   208116     8   $nSegments $initialGI $nIntegration  $trans_Corot;

ConstructBrace 8109100   109141   210113     9   $nSegments $initialGI $nIntegration  $trans_Corot;
ConstructBrace 8209100   109241   210114     9   $nSegments $initialGI $nIntegration  $trans_Corot;

ConstructBrace 8110100   111151   210117    10   $nSegments $initialGI $nIntegration  $trans_Corot;
ConstructBrace 8210100   111251   210116    10   $nSegments $initialGI $nIntegration  $trans_Corot;

ConstructBrace 8111100   111141   212113    11   $nSegments $initialGI $nIntegration  $trans_Corot;
ConstructBrace 8211100   111241   212114    11   $nSegments $initialGI $nIntegration  $trans_Corot;

ConstructBrace 8112100   113151   212117    12   $nSegments $initialGI $nIntegration  $trans_Corot;
ConstructBrace 8212100   113251   212116    12   $nSegments $initialGI $nIntegration  $trans_Corot;


# CONSTRUCT THE GHOST BRACES
uniaxialMaterial Elastic 1000 100.0
element corotTruss 4101100   101141   202113  0.05  1000;
element corotTruss 4201100   101241   202114  0.05  1000;
element corotTruss 4102100   103151   202117  0.05  1000;
element corotTruss 4202100   103251   202116  0.05  1000;
element corotTruss 4103100   103141   204113  0.05  1000;
element corotTruss 4203100   103241   204114  0.05  1000;
element corotTruss 4104100   105151   204117  0.05  1000;
element corotTruss 4204100   105251   204116  0.05  1000;
element corotTruss 4105100   105141   206113  0.05  1000;
element corotTruss 4205100   105241   206114  0.05  1000;
element corotTruss 4106100   107151   206117  0.05  1000;
element corotTruss 4206100   107251   206116  0.05  1000;
element corotTruss 4107100   107141   208113  0.05  1000;
element corotTruss 4207100   107241   208114  0.05  1000;
element corotTruss 4108100   109151   208117  0.05  1000;
element corotTruss 4208100   109251   208116  0.05  1000;
element corotTruss 4109100   109141   210113  0.05  1000;
element corotTruss 4209100   109241   210114  0.05  1000;
element corotTruss 4110100   111151   210117  0.05  1000;
element corotTruss 4210100   111251   210116  0.05  1000;
element corotTruss 4111100   111141   212113  0.05  1000;
element corotTruss 4211100   111241   212114  0.05  1000;
element corotTruss 4112100   113151   212117  0.05  1000;
element corotTruss 4212100   113251   212116  0.05  1000;

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
FiberWF    101 666 12.1000 8.0500 0.5750 0.3350 6 2 6 2; ConstructFiberColumn 612100    1213   1311   101 5 0.0010 5 $trans_selected 0;
FiberWF    102 666 12.1000 8.0500 0.5750 0.3350 6 2 6 2; ConstructFiberColumn 612200    1223   1321   102 5 0.0010 5 $trans_selected 0;

FiberWF    103 666 12.1000 8.0500 0.5750 0.3350 6 2 6 2; ConstructFiberColumn 611102  111172   1211   103 2 0.0010 5 $trans_selected 2;
FiberWF    104 666 12.1000 8.0500 0.5750 0.3350 6 2 6 2; ConstructFiberColumn 611202  111272   1221   104 2 0.0010 5 $trans_selected 2;

FiberWF    105 666 14.2000 14.6000 0.7800 0.4850 6 2 6 2; ConstructFiberColumn  611101     1113  111171   105 2 0.0010 5 $trans_selected 1;
FiberWF    106 666 14.2000 14.6000 0.7800 0.4850 6 2 6 2; ConstructFiberColumn  611201     1123  111271   106 2 0.0010 5 $trans_selected 1;

FiberWF    107 666 14.2000 14.6000 0.7800 0.4850 6 2 6 2; ConstructFiberColumn 610100    1013   1111   107 5 0.0010 5 $trans_selected 0;
FiberWF    108 666 14.2000 14.6000 0.7800 0.4850 6 2 6 2; ConstructFiberColumn 610200    1023   1121   108 5 0.0010 5 $trans_selected 0;

FiberWF    109 666 14.2000 14.6000 0.7800 0.4850 6 2 6 2; ConstructFiberColumn 609102  109172   1011   109 2 0.0010 5 $trans_selected 2;
FiberWF    110 666 14.2000 14.6000 0.7800 0.4850 6 2 6 2; ConstructFiberColumn 609202  109272   1021   110 2 0.0010 5 $trans_selected 2;

FiberWF    111 666 15.5000 15.7000 1.4400 0.8900 6 2 6 2; ConstructFiberColumn  609101      913  109171   111 2 0.0010 5 $trans_selected 1;
FiberWF    112 666 15.5000 15.7000 1.4400 0.8900 6 2 6 2; ConstructFiberColumn  609201      923  109271   112 2 0.0010 5 $trans_selected 1;

FiberWF    113 666 15.5000 15.7000 1.4400 0.8900 6 2 6 2; ConstructFiberColumn 608100     813    911   113 5 0.0010 5 $trans_selected 0;
FiberWF    114 666 15.5000 15.7000 1.4400 0.8900 6 2 6 2; ConstructFiberColumn 608200     823    921   114 5 0.0010 5 $trans_selected 0;

FiberWF    115 666 15.5000 15.7000 1.4400 0.8900 6 2 6 2; ConstructFiberColumn 607102  107172    811   115 2 0.0010 5 $trans_selected 2;
FiberWF    116 666 15.5000 15.7000 1.4400 0.8900 6 2 6 2; ConstructFiberColumn 607202  107272    821   116 2 0.0010 5 $trans_selected 2;

FiberWF    117 666 16.7000 16.1000 2.0700 1.2900 6 2 6 2; ConstructFiberColumn  607101      713  107171   117 2 0.0010 5 $trans_selected 1;
FiberWF    118 666 16.7000 16.1000 2.0700 1.2900 6 2 6 2; ConstructFiberColumn  607201      723  107271   118 2 0.0010 5 $trans_selected 1;

FiberWF    119 666 16.7000 16.1000 2.0700 1.2900 6 2 6 2; ConstructFiberColumn 606100     613    711   119 5 0.0010 5 $trans_selected 0;
FiberWF    120 666 16.7000 16.1000 2.0700 1.2900 6 2 6 2; ConstructFiberColumn 606200     623    721   120 5 0.0010 5 $trans_selected 0;

FiberWF    121 666 16.7000 16.1000 2.0700 1.2900 6 2 6 2; ConstructFiberColumn 605102  105172    611   121 2 0.0010 5 $trans_selected 2;
FiberWF    122 666 16.7000 16.1000 2.0700 1.2900 6 2 6 2; ConstructFiberColumn 605202  105272    621   122 2 0.0010 5 $trans_selected 2;

FiberWF    123 666 18.3000 16.6000 2.8500 1.7700 6 2 6 2; ConstructFiberColumn  605101      513  105171   123 2 0.0010 5 $trans_selected 1;
FiberWF    124 666 18.3000 16.6000 2.8500 1.7700 6 2 6 2; ConstructFiberColumn  605201      523  105271   124 2 0.0010 5 $trans_selected 1;

FiberWF    125 666 18.3000 16.6000 2.8500 1.7700 6 2 6 2; ConstructFiberColumn 604100     413    511   125 5 0.0010 5 $trans_selected 0;
FiberWF    126 666 18.3000 16.6000 2.8500 1.7700 6 2 6 2; ConstructFiberColumn 604200     423    521   126 5 0.0010 5 $trans_selected 0;

FiberWF    127 666 18.3000 16.6000 2.8500 1.7700 6 2 6 2; ConstructFiberColumn 603102  103172    411   127 2 0.0010 5 $trans_selected 2;
FiberWF    128 666 18.3000 16.6000 2.8500 1.7700 6 2 6 2; ConstructFiberColumn 603202  103272    421   128 2 0.0010 5 $trans_selected 2;

FiberWF    129 666 20.2000 17.2000 3.8200 2.3800 6 2 6 2; ConstructFiberColumn  603101      313  103171   129 2 0.0010 5 $trans_selected 1;
FiberWF    130 666 20.2000 17.2000 3.8200 2.3800 6 2 6 2; ConstructFiberColumn  603201      323  103271   130 2 0.0010 5 $trans_selected 1;

FiberWF    131 666 20.2000 17.2000 3.8200 2.3800 6 2 6 2; ConstructFiberColumn 602100     213    311   131 5 0.0010 5 $trans_selected 0;
FiberWF    132 666 20.2000 17.2000 3.8200 2.3800 6 2 6 2; ConstructFiberColumn 602200     223    321   132 5 0.0010 5 $trans_selected 0;

FiberWF    133 666 20.2000 17.2000 3.8200 2.3800 6 2 6 2; ConstructFiberColumn 601100     113    211   133 5 0.0010 5 $trans_selected 0;
FiberWF    134 666 20.2000 17.2000 3.8200 2.3800 6 2 6 2; ConstructFiberColumn 601200     123    221   134 5 0.0010 5 $trans_selected 0;


# BEAMS
element ModElasticBeam2d   513100     1314     1322  16.2000 $E [expr ($n+1)/$n*0.90*$Comp_I*890.0000] $K11_2 $K33_2 $K44_2 $trans_selected; 
element ModElasticBeam2d   512101     1214   212112  10.3000 $E [expr ($n+1)/$n*0.90*$Comp_I*510.0000] $K11_2 $K33_2 $K44_2 $trans_selected; element ModElasticBeam2d   512102     1222   212115  10.3000 $E [expr ($n+1)/$n*0.90*$Comp_I*510.0000] $K11_2 $K33_2 $K44_2 $trans_selected; 
element ModElasticBeam2d   511100     1114     1122  17.6000 $E [expr ($n+1)/$n*0.90*$Comp_I*984.0000] $K11_2 $K33_2 $K44_2 $trans_selected; 
element ModElasticBeam2d   510101     1014   210112  10.3000 $E [expr ($n+1)/$n*0.90*$Comp_I*510.0000] $K11_2 $K33_2 $K44_2 $trans_selected; element ModElasticBeam2d   510102     1022   210115  10.3000 $E [expr ($n+1)/$n*0.90*$Comp_I*510.0000] $K11_2 $K33_2 $K44_2 $trans_selected; 
element ModElasticBeam2d   509100      914      922  19.1000 $E [expr ($n+1)/$n*0.90*$Comp_I*1070.0000] $K11_2 $K33_2 $K44_2 $trans_selected; 
element ModElasticBeam2d   508101      814   208112  10.3000 $E [expr ($n+1)/$n*0.90*$Comp_I*510.0000] $K11_2 $K33_2 $K44_2 $trans_selected; element ModElasticBeam2d   508102      822   208115  10.3000 $E [expr ($n+1)/$n*0.90*$Comp_I*510.0000] $K11_2 $K33_2 $K44_2 $trans_selected; 
element ModElasticBeam2d   507100      714      722  19.1000 $E [expr ($n+1)/$n*0.90*$Comp_I*1070.0000] $K11_2 $K33_2 $K44_2 $trans_selected; 
element ModElasticBeam2d   506101      614   206112  10.3000 $E [expr ($n+1)/$n*0.90*$Comp_I*510.0000] $K11_2 $K33_2 $K44_2 $trans_selected; element ModElasticBeam2d   506102      622   206115  10.3000 $E [expr ($n+1)/$n*0.90*$Comp_I*510.0000] $K11_2 $K33_2 $K44_2 $trans_selected; 
element ModElasticBeam2d   505100      514      522  20.8000 $E [expr ($n+1)/$n*0.90*$Comp_I*1170.0000] $K11_2 $K33_2 $K44_2 $trans_selected; 
element ModElasticBeam2d   504101      414   204112  10.3000 $E [expr ($n+1)/$n*0.90*$Comp_I*510.0000] $K11_2 $K33_2 $K44_2 $trans_selected; element ModElasticBeam2d   504102      422   204115  10.3000 $E [expr ($n+1)/$n*0.90*$Comp_I*510.0000] $K11_2 $K33_2 $K44_2 $trans_selected; 
element ModElasticBeam2d   503100      314      322  20.8000 $E [expr ($n+1)/$n*0.90*$Comp_I*1170.0000] $K11_2 $K33_2 $K44_2 $trans_selected; 
element ModElasticBeam2d   502101      214   202112  10.3000 $E [expr ($n+1)/$n*0.90*$Comp_I*510.0000] $K11_2 $K33_2 $K44_2 $trans_selected; element ModElasticBeam2d   502102      222   202115  10.3000 $E [expr ($n+1)/$n*0.90*$Comp_I*510.0000] $K11_2 $K33_2 $K44_2 $trans_selected; 

###################################################################################################
#                                           MF BEAM SPRINGS                                       #
###################################################################################################

# COMMAND SYNTAX 
# Spring_Pinching $SpringID $iNode $jNode $EffectivePlasticStrength $gap $CompositeFlag

set gap 0.08;
Spring_IMK 912104 412104 1214 $E $fy [expr $Comp_I*510.0000]  17.7000 53.5000 7.0600 1.2200 147.5266 73.7633 73.7633 4023.2500 0 $Composite 0 2; Spring_IMK 912202 1222 412202 $E $fy [expr $Comp_I*510.0000]  17.7000 53.5000 7.0600 1.2200 147.5266 73.7633 73.7633 4023.2500 0 $Composite 0 2; Spring_IMK 912122 212102 212112 $E $fy [expr $Comp_I*510.0000] 17.7000 53.5000 7.0600 1.2200 147.5266 73.7633 73.7633 4023.2500 0 $Composite 0 2; Spring_IMK 912155 212105 212115 $E $fy [expr $Comp_I*510.0000] 17.7000 53.5000 7.0600 1.2200 147.5266 73.7633 73.7633 4023.2500 0 $Composite 0 2; 
Spring_IMK 910104 410104 1014 $E $fy [expr $Comp_I*510.0000]  17.7000 53.5000 7.0600 1.2200 142.5455 71.2728 71.2728 4023.2500 0 $Composite 0 2; Spring_IMK 910202 1022 410202 $E $fy [expr $Comp_I*510.0000]  17.7000 53.5000 7.0600 1.2200 142.5455 71.2728 71.2728 4023.2500 0 $Composite 0 2; Spring_IMK 910122 210102 210112 $E $fy [expr $Comp_I*510.0000] 17.7000 53.5000 7.0600 1.2200 142.5455 71.2728 71.2728 4023.2500 0 $Composite 0 2; Spring_IMK 910155 210105 210115 $E $fy [expr $Comp_I*510.0000] 17.7000 53.5000 7.0600 1.2200 142.5455 71.2728 71.2728 4023.2500 0 $Composite 0 2; 
Spring_IMK 908104 408104 814 $E $fy [expr $Comp_I*510.0000]  17.7000 53.5000 7.0600 1.2200 137.5262 68.7631 68.7631 4023.2500 0 $Composite 0 2; Spring_IMK 908202 822 408202 $E $fy [expr $Comp_I*510.0000]  17.7000 53.5000 7.0600 1.2200 137.5262 68.7631 68.7631 4023.2500 0 $Composite 0 2; Spring_IMK 908122 208102 208112 $E $fy [expr $Comp_I*510.0000] 17.7000 53.5000 7.0600 1.2200 137.5262 68.7631 68.7631 4023.2500 0 $Composite 0 2; Spring_IMK 908155 208105 208115 $E $fy [expr $Comp_I*510.0000] 17.7000 53.5000 7.0600 1.2200 137.5262 68.7631 68.7631 4023.2500 0 $Composite 0 2; 
Spring_IMK 906104 406104 614 $E $fy [expr $Comp_I*510.0000]  17.7000 53.5000 7.0600 1.2200 136.7261 68.3631 68.3631 4023.2500 0 $Composite 0 2; Spring_IMK 906202 622 406202 $E $fy [expr $Comp_I*510.0000]  17.7000 53.5000 7.0600 1.2200 136.7261 68.3631 68.3631 4023.2500 0 $Composite 0 2; Spring_IMK 906122 206102 206112 $E $fy [expr $Comp_I*510.0000] 17.7000 53.5000 7.0600 1.2200 136.7261 68.3631 68.3631 4023.2500 0 $Composite 0 2; Spring_IMK 906155 206105 206115 $E $fy [expr $Comp_I*510.0000] 17.7000 53.5000 7.0600 1.2200 136.7261 68.3631 68.3631 4023.2500 0 $Composite 0 2; 
Spring_IMK 904104 404104 414 $E $fy [expr $Comp_I*510.0000]  17.7000 53.5000 7.0600 1.2200 132.5058 66.2529 66.2529 4023.2500 0 $Composite 0 2; Spring_IMK 904202 422 404202 $E $fy [expr $Comp_I*510.0000]  17.7000 53.5000 7.0600 1.2200 132.5058 66.2529 66.2529 4023.2500 0 $Composite 0 2; Spring_IMK 904122 204102 204112 $E $fy [expr $Comp_I*510.0000] 17.7000 53.5000 7.0600 1.2200 132.5058 66.2529 66.2529 4023.2500 0 $Composite 0 2; Spring_IMK 904155 204105 204115 $E $fy [expr $Comp_I*510.0000] 17.7000 53.5000 7.0600 1.2200 132.5058 66.2529 66.2529 4023.2500 0 $Composite 0 2; 
Spring_IMK 902104 402104 214 $E $fy [expr $Comp_I*510.0000]  17.7000 53.5000 7.0600 1.2200 132.7957 66.3979 66.3979 4023.2500 0 $Composite 0 2; Spring_IMK 902202 222 402202 $E $fy [expr $Comp_I*510.0000]  17.7000 53.5000 7.0600 1.2200 132.7957 66.3979 66.3979 4023.2500 0 $Composite 0 2; Spring_IMK 902122 202102 202112 $E $fy [expr $Comp_I*510.0000] 17.7000 53.5000 7.0600 1.2200 132.7957 66.3979 66.3979 4023.2500 0 $Composite 0 2; Spring_IMK 902155 202105 202115 $E $fy [expr $Comp_I*510.0000] 17.7000 53.5000 7.0600 1.2200 132.7957 66.3979 66.3979 4023.2500 0 $Composite 0 2; 

Spring_Pinching  913104  413104 1314 6776.0000 $gap $Composite; Spring_Pinching  913202  1322 413202 6776.0000 $gap $Composite; 
Spring_Pinching  911104  411104 1114 7441.5000 $gap $Composite; Spring_Pinching  911202  1122 411202 7441.5000 $gap $Composite; 
Spring_Pinching  909104  409104 914 8046.5000 $gap $Composite; Spring_Pinching  909202  922 409202 8046.5000 $gap $Composite; 
Spring_Pinching  907104  407104 714 8046.5000 $gap $Composite; Spring_Pinching  907202  722 407202 8046.5000 $gap $Composite; 
Spring_Pinching  905104  405104 514 8833.0000 $gap $Composite; Spring_Pinching  905202  522 405202 8833.0000 $gap $Composite; 
Spring_Pinching  903104  403104 314 8833.0000 $gap $Composite; Spring_Pinching  903202  322 403202 8833.0000 $gap $Composite; 

###################################################################################################
#                                           MF COLUMN SPRINGS                                     #
###################################################################################################

Spring_Rigid  913101  413101    1311; Spring_Rigid  913201  413201    1321; 
Spring_Rigid  912103  412103    1213; Spring_Rigid  912203  412203    1223; 
Spring_Rigid  912101  412101    1211; Spring_Rigid  912201  412201    1221; 
Spring_Rigid  911103  411103    1113; Spring_Rigid  911203  411203    1123; 
Spring_Rigid  911101  411101    1111; Spring_Rigid  911201  411201    1121; 
Spring_Rigid  910103  410103    1013; Spring_Rigid  910203  410203    1023; 
Spring_Rigid  910101  410101    1011; Spring_Rigid  910201  410201    1021; 
Spring_Rigid  909103  409103     913; Spring_Rigid  909203  409203     923; 
Spring_Rigid  909101  409101     911; Spring_Rigid  909201  409201     921; 
Spring_Rigid  908103  408103     813; Spring_Rigid  908203  408203     823; 
Spring_Rigid  908101  408101     811; Spring_Rigid  908201  408201     821; 
Spring_Rigid  907103  407103     713; Spring_Rigid  907203  407203     723; 
Spring_Rigid  907101  407101     711; Spring_Rigid  907201  407201     721; 
Spring_Rigid  906103  406103     613; Spring_Rigid  906203  406203     623; 
Spring_Rigid  906101  406101     611; Spring_Rigid  906201  406201     621; 
Spring_Rigid  905103  405103     513; Spring_Rigid  905203  405203     523; 
Spring_Rigid  905101  405101     511; Spring_Rigid  905201  405201     521; 
Spring_Rigid  904103  404103     413; Spring_Rigid  904203  404203     423; 
Spring_Rigid  904101  404101     411; Spring_Rigid  904201  404201     421; 
Spring_Rigid  903103  403103     313; Spring_Rigid  903203  403203     323; 
Spring_Rigid  903101  403101     311; Spring_Rigid  903201  403201     321; 
Spring_Rigid  902103  402103     213; Spring_Rigid  902203  402203     223; 
Spring_Rigid  902101  402101     211; Spring_Rigid  902201  402201     221; 
Spring_Rigid  901103     110     113; Spring_Rigid  901203     120     123; 

###################################################################################################
#                                          COLUMN SPLICE SPRINGS                                  #
###################################################################################################

Spring_Zero 911107 111171 111172; 
Spring_Zero 911207 111271 111272; 
Spring_Zero 911307 111371 111372; 
Spring_Zero 911407 111471 111472; 
Spring_Zero 909107 109171 109172; 
Spring_Zero 909207 109271 109272; 
Spring_Zero 909307 109371 109372; 
Spring_Zero 909407 109471 109472; 
Spring_Zero 907107 107171 107172; 
Spring_Zero 907207 107271 107272; 
Spring_Zero 907307 107371 107372; 
Spring_Zero 907407 107471 107472; 
Spring_Zero 905107 105171 105172; 
Spring_Zero 905207 105271 105272; 
Spring_Zero 905307 105371 105372; 
Spring_Zero 905407 105471 105472; 
Spring_Zero 903107 103171 103172; 
Spring_Zero 903207 103271 103272; 
Spring_Zero 903307 103371 103372; 
Spring_Zero 903407 103471 103472; 

####################################################################################################
#                                              FLOOR LINKS                                         #
####################################################################################################

# Command Syntax 
# element truss $ElementID $iNode $jNode $Area $matID
element truss 1013 413204 1330 $A_Stiff 99;
element truss 1012 412204 1230 $A_Stiff 99;
element truss 1011 411204 1130 $A_Stiff 99;
element truss 1010 410204 1030 $A_Stiff 99;
element truss 1009 409204 930 $A_Stiff 99;
element truss 1008 408204 830 $A_Stiff 99;
element truss 1007 407204 730 $A_Stiff 99;
element truss 1006 406204 630 $A_Stiff 99;
element truss 1005 405204 530 $A_Stiff 99;
element truss 1004 404204 430 $A_Stiff 99;
element truss 1003 403204 330 $A_Stiff 99;
element truss 1002 402204 230 $A_Stiff 99;

####################################################################################################
#                                          EGF COLUMNS AND BEAMS                                   #
####################################################################################################

# GRAVITY COLUMNS
element elasticBeamColumn  612300    1233    1331 11.8750 $E [expr (71.8438  + 100.0000)] $trans_PDelta; element elasticBeamColumn  612400    1243    1341 11.8750 $E [expr (71.8438  + 100.0000)] $trans_PDelta; 
element elasticBeamColumn  611302  111372    1231 11.8750 $E [expr (71.8438  + 100.0000)] $trans_PDelta; element elasticBeamColumn  611402  111472    1241 11.8750 $E [expr (71.8438  + 100.0000)] $trans_PDelta; 
element elasticBeamColumn  611301    1133  111371 11.8750 $E [expr (71.8438  + 804.0000)] $trans_PDelta; element elasticBeamColumn  611401    1143  111471 11.8750 $E [expr (71.8438  + 804.0000)] $trans_PDelta; 
element elasticBeamColumn  610300    1033    1131 12.9437 $E [expr (79.5625  + 804.0000)] $trans_PDelta; element elasticBeamColumn  610400    1043    1141 12.9437 $E [expr (79.5625  + 804.0000)] $trans_PDelta; 
element elasticBeamColumn  609302  109372    1031 12.9437 $E [expr (79.5625  + 804.0000)] $trans_PDelta; element elasticBeamColumn  609402  109472    1041 12.9437 $E [expr (79.5625  + 804.0000)] $trans_PDelta; 
element elasticBeamColumn  609301     933  109371 12.9437 $E [expr (79.5625  + 1862.0000)] $trans_PDelta; element elasticBeamColumn  609401     943  109471 12.9437 $E [expr (79.5625  + 1862.0000)] $trans_PDelta; 
element elasticBeamColumn  608300     833     931 15.7344 $E [expr (214.9375  + 1862.0000)] $trans_PDelta; element elasticBeamColumn  608400     843     941 15.7344 $E [expr (214.9375  + 1862.0000)] $trans_PDelta; 
element elasticBeamColumn  607302  107372     831 15.7344 $E [expr (214.9375  + 1862.0000)] $trans_PDelta; element elasticBeamColumn  607402  107472     841 15.7344 $E [expr (214.9375  + 1862.0000)] $trans_PDelta; 
element elasticBeamColumn  607301     733  107371 15.7344 $E [expr (214.9375  + 2880.0000)] $trans_PDelta; element elasticBeamColumn  607401     743  107471 15.7344 $E [expr (214.9375  + 2880.0000)] $trans_PDelta; 
element elasticBeamColumn  606300     633     731 20.9594 $E [expr (293.9063  + 2880.0000)] $trans_PDelta; element elasticBeamColumn  606400     643     741 20.9594 $E [expr (293.9063  + 2880.0000)] $trans_PDelta; 
element elasticBeamColumn  605302  105372     631 20.9594 $E [expr (293.9063  + 2880.0000)] $trans_PDelta; element elasticBeamColumn  605402  105472     641 20.9594 $E [expr (293.9063  + 2880.0000)] $trans_PDelta; 
element elasticBeamColumn  605301     533  105371 20.9594 $E [expr (293.9063  + 4340.0000)] $trans_PDelta; element elasticBeamColumn  605401     543  105471 20.9594 $E [expr (293.9063  + 4340.0000)] $trans_PDelta; 
element elasticBeamColumn  604300     433     531 25.3531 $E [expr (401.9688  + 4340.0000)] $trans_PDelta; element elasticBeamColumn  604400     443     541 25.3531 $E [expr (401.9688  + 4340.0000)] $trans_PDelta; 
element elasticBeamColumn  603302  103372     431 25.3531 $E [expr (401.9688  + 4340.0000)] $trans_PDelta; element elasticBeamColumn  603402  103472     441 25.3531 $E [expr (401.9688  + 4340.0000)] $trans_PDelta; 
element elasticBeamColumn  603301     333  103371 25.3531 $E [expr (401.9688  + 6500.0000)] $trans_PDelta; element elasticBeamColumn  603401     343  103471 25.3531 $E [expr (401.9688  + 6500.0000)] $trans_PDelta; 
element elasticBeamColumn  602300     233     331 30.7562 $E [expr (497.5625  + 6500.0000)] $trans_PDelta; element elasticBeamColumn  602400     243     341 30.7562 $E [expr (497.5625  + 6500.0000)] $trans_PDelta; 
element elasticBeamColumn  601300     133     231 30.7562 $E [expr (497.5625  + 6500.0000)] $trans_PDelta; element elasticBeamColumn  601400     143     241 30.7562 $E [expr (497.5625  + 6500.0000)] $trans_PDelta; 

# GRAVITY BEAMS
element elasticBeamColumn  513200    1334    1342 45.0125 $E [expr $Comp_I_GC * 4387.5000] $trans_PDelta;
element elasticBeamColumn  512200    1234    1242 49.7250 $E [expr $Comp_I_GC * 5037.5000] $trans_PDelta;
element elasticBeamColumn  511200    1134    1142 49.7250 $E [expr $Comp_I_GC * 5037.5000] $trans_PDelta;
element elasticBeamColumn  510200    1034    1042 49.7250 $E [expr $Comp_I_GC * 5037.5000] $trans_PDelta;
element elasticBeamColumn  509200     934     942 49.7250 $E [expr $Comp_I_GC * 5037.5000] $trans_PDelta;
element elasticBeamColumn  508200     834     842 49.7250 $E [expr $Comp_I_GC * 5037.5000] $trans_PDelta;
element elasticBeamColumn  507200     734     742 49.7250 $E [expr $Comp_I_GC * 5037.5000] $trans_PDelta;
element elasticBeamColumn  506200     634     642 49.7250 $E [expr $Comp_I_GC * 5037.5000] $trans_PDelta;
element elasticBeamColumn  505200     534     542 49.7250 $E [expr $Comp_I_GC * 5037.5000] $trans_PDelta;
element elasticBeamColumn  504200     434     442 49.7250 $E [expr $Comp_I_GC * 5037.5000] $trans_PDelta;
element elasticBeamColumn  503200     334     342 49.7250 $E [expr $Comp_I_GC * 5037.5000] $trans_PDelta;
element elasticBeamColumn  502200     234     242 49.7250 $E [expr $Comp_I_GC * 5037.5000] $trans_PDelta;

# GRAVITY COLUMNS SPRINGS
Spring_IMK   913301    1330    1331 $E $fy [expr (71.8438 + 100.0000)] 14.0000 27.5000 6.9700 2.4600 180.0000 90.0000 180.0000 3624.5172 0 $Composite 0 2; Spring_IMK   913401    1340    1341 $E $fy [expr (71.8438 + 100.0000)] 14.0000 27.5000 6.9700 2.4600 180.0000 90.0000 180.0000 3624.5172 0 $Composite 0 2; 
Spring_IMK   912303    1230    1233 $E $fy [expr (71.8438 + 100.0000)] 14.0000 27.5000 6.9700 2.4600 180.0000 90.0000 180.0000 3624.5172 0 $Composite 0 2; Spring_IMK   912403    1240    1243 $E $fy [expr (71.8438 + 100.0000)] 14.0000 27.5000 6.9700 2.4600 180.0000 90.0000 180.0000 3624.5172 0 $Composite 0 2; 
Spring_IMK   912301    1230    1231 $E $fy [expr (71.8438 + 100.0000)] 14.0000 27.5000 6.9700 2.4600 180.0000 90.0000 180.0000 3624.5172 0 $Composite 0 2; Spring_IMK   912401    1240    1241 $E $fy [expr (71.8438 + 100.0000)] 14.0000 27.5000 6.9700 2.4600 180.0000 90.0000 180.0000 3624.5172 0 $Composite 0 2; 
Spring_IMK   911303    1130    1133 $E $fy [expr (79.5625 + 804.0000)] 14.2000 25.4000 6.4100 2.4800 180.0000 90.0000 180.0000 11570.4359 0 $Composite 0 2; Spring_IMK   911403    1140    1143 $E $fy [expr (79.5625 + 804.0000)] 14.2000 25.4000 6.4100 2.4800 180.0000 90.0000 180.0000 11570.4359 0 $Composite 0 2; 
Spring_IMK   911301    1130    1131 $E $fy [expr (79.5625 + 804.0000)] 14.2000 25.4000 6.4100 2.4800 180.0000 90.0000 180.0000 11570.4359 0 $Composite 0 2; Spring_IMK   911401    1140    1141 $E $fy [expr (79.5625 + 804.0000)] 14.2000 25.4000 6.4100 2.4800 180.0000 90.0000 180.0000 11570.4359 0 $Composite 0 2; 
Spring_IMK   910303    1030    1033 $E $fy [expr (79.5625 + 804.0000)] 14.2000 25.4000 6.4100 2.4800 180.0000 90.0000 180.0000 11570.4359 0 $Composite 0 2; Spring_IMK   910403    1040    1043 $E $fy [expr (79.5625 + 804.0000)] 14.2000 25.4000 6.4100 2.4800 180.0000 90.0000 180.0000 11570.4359 0 $Composite 0 2; 
Spring_IMK   910301    1030    1031 $E $fy [expr (79.5625 + 804.0000)] 14.2000 25.4000 6.4100 2.4800 180.0000 90.0000 180.0000 11570.4359 0 $Composite 0 2; Spring_IMK   910401    1040    1041 $E $fy [expr (79.5625 + 804.0000)] 14.2000 25.4000 6.4100 2.4800 180.0000 90.0000 180.0000 11570.4359 0 $Composite 0 2; 
Spring_IMK   909303     930     933 $E $fy [expr (214.9375 + 1862.0000)] 14.0000 25.9000 10.2000 3.7000 180.0000 90.0000 180.0000 24495.6938 0 $Composite 0 2; Spring_IMK   909403     940     943 $E $fy [expr (214.9375 + 1862.0000)] 14.0000 25.9000 10.2000 3.7000 180.0000 90.0000 180.0000 24495.6938 0 $Composite 0 2; 
Spring_IMK   909301     930     931 $E $fy [expr (214.9375 + 1862.0000)] 14.0000 25.9000 10.2000 3.7000 180.0000 90.0000 180.0000 24495.6938 0 $Composite 0 2; Spring_IMK   909401     940     941 $E $fy [expr (214.9375 + 1862.0000)] 14.0000 25.9000 10.2000 3.7000 180.0000 90.0000 180.0000 24495.6938 0 $Composite 0 2; 
Spring_IMK   908303     830     833 $E $fy [expr (214.9375 + 1862.0000)] 14.0000 25.9000 10.2000 3.7000 180.0000 90.0000 180.0000 24495.6938 0 $Composite 0 2; Spring_IMK   908403     840     843 $E $fy [expr (214.9375 + 1862.0000)] 14.0000 25.9000 10.2000 3.7000 180.0000 90.0000 180.0000 24495.6938 0 $Composite 0 2; 
Spring_IMK   908301     830     831 $E $fy [expr (214.9375 + 1862.0000)] 14.0000 25.9000 10.2000 3.7000 180.0000 90.0000 180.0000 24495.6938 0 $Composite 0 2; Spring_IMK   908401     840     841 $E $fy [expr (214.9375 + 1862.0000)] 14.0000 25.9000 10.2000 3.7000 180.0000 90.0000 180.0000 24495.6938 0 $Composite 0 2; 
Spring_IMK   907303     730     733 $E $fy [expr (293.9063 + 2880.0000)] 14.5000 19.3000 7.8000 3.7400 180.0000 90.0000 180.0000 36818.0313 0 $Composite 0 2; Spring_IMK   907403     740     743 $E $fy [expr (293.9063 + 2880.0000)] 14.5000 19.3000 7.8000 3.7400 180.0000 90.0000 180.0000 36818.0313 0 $Composite 0 2; 
Spring_IMK   907301     730     731 $E $fy [expr (293.9063 + 2880.0000)] 14.5000 19.3000 7.8000 3.7400 180.0000 90.0000 180.0000 36818.0313 0 $Composite 0 2; Spring_IMK   907401     740     741 $E $fy [expr (293.9063 + 2880.0000)] 14.5000 19.3000 7.8000 3.7400 180.0000 90.0000 180.0000 36818.0313 0 $Composite 0 2; 
Spring_IMK   906303     630     633 $E $fy [expr (293.9063 + 2880.0000)] 14.5000 19.3000 7.8000 3.7400 180.0000 90.0000 180.0000 36818.0313 0 $Composite 0 2; Spring_IMK   906403     640     643 $E $fy [expr (293.9063 + 2880.0000)] 14.5000 19.3000 7.8000 3.7400 180.0000 90.0000 180.0000 36818.0313 0 $Composite 0 2; 
Spring_IMK   906301     630     631 $E $fy [expr (293.9063 + 2880.0000)] 14.5000 19.3000 7.8000 3.7400 180.0000 90.0000 180.0000 36818.0313 0 $Composite 0 2; Spring_IMK   906401     640     641 $E $fy [expr (293.9063 + 2880.0000)] 14.5000 19.3000 7.8000 3.7400 180.0000 90.0000 180.0000 36818.0313 0 $Composite 0 2; 
Spring_IMK   905303     530     533 $E $fy [expr (401.9688 + 4340.0000)] 14.8000 16.8000 7.1100 3.9800 180.0000 90.0000 180.0000 53419.6094 0 $Composite 0 2; Spring_IMK   905403     540     543 $E $fy [expr (401.9688 + 4340.0000)] 14.8000 16.8000 7.1100 3.9800 180.0000 90.0000 180.0000 53419.6094 0 $Composite 0 2; 
Spring_IMK   905301     530     531 $E $fy [expr (401.9688 + 4340.0000)] 14.8000 16.8000 7.1100 3.9800 180.0000 90.0000 180.0000 53419.6094 0 $Composite 0 2; Spring_IMK   905401     540     541 $E $fy [expr (401.9688 + 4340.0000)] 14.8000 16.8000 7.1100 3.9800 180.0000 90.0000 180.0000 53419.6094 0 $Composite 0 2; 
Spring_IMK   904303     430     433 $E $fy [expr (401.9688 + 4340.0000)] 14.8000 16.8000 7.1100 3.9800 180.0000 90.0000 180.0000 53419.6094 0 $Composite 0 2; Spring_IMK   904403     440     443 $E $fy [expr (401.9688 + 4340.0000)] 14.8000 16.8000 7.1100 3.9800 180.0000 90.0000 180.0000 53419.6094 0 $Composite 0 2; 
Spring_IMK   904301     430     431 $E $fy [expr (401.9688 + 4340.0000)] 14.8000 16.8000 7.1100 3.9800 180.0000 90.0000 180.0000 53419.6094 0 $Composite 0 2; Spring_IMK   904401     440     441 $E $fy [expr (401.9688 + 4340.0000)] 14.8000 16.8000 7.1100 3.9800 180.0000 90.0000 180.0000 53419.6094 0 $Composite 0 2; 
Spring_IMK   903303     330     333 $E $fy [expr (497.5625 + 6500.0000)] 15.2000 13.7000 5.9700 4.0200 180.0000 90.0000 180.0000 76398.2656 0 $Composite 0 2; Spring_IMK   903403     340     343 $E $fy [expr (497.5625 + 6500.0000)] 15.2000 13.7000 5.9700 4.0200 180.0000 90.0000 180.0000 76398.2656 0 $Composite 0 2; 
Spring_IMK   903301     330     331 $E $fy [expr (497.5625 + 6500.0000)] 15.2000 13.7000 5.9700 4.0200 180.0000 90.0000 180.0000 76398.2656 0 $Composite 0 2; Spring_IMK   903401     340     341 $E $fy [expr (497.5625 + 6500.0000)] 15.2000 13.7000 5.9700 4.0200 180.0000 90.0000 180.0000 76398.2656 0 $Composite 0 2; 
Spring_IMK   902303     230     233 $E $fy [expr (497.5625 + 6500.0000)] 15.2000 13.7000 5.9700 4.0200 180.0000 90.0000 180.0000 76398.2656 0 $Composite 0 2; Spring_IMK   902403     240     243 $E $fy [expr (497.5625 + 6500.0000)] 15.2000 13.7000 5.9700 4.0200 180.0000 90.0000 180.0000 76398.2656 0 $Composite 0 2; 
Spring_IMK   902301     230     231 $E $fy [expr (497.5625 + 6500.0000)] 15.2000 13.7000 5.9700 4.0200 180.0000 90.0000 180.0000 76398.2656 0 $Composite 0 2; Spring_IMK   902401     240     241 $E $fy [expr (497.5625 + 6500.0000)] 15.2000 13.7000 5.9700 4.0200 180.0000 90.0000 180.0000 76398.2656 0 $Composite 0 2; 
Spring_IMK   901303     130     133 $E $fy 6500.0000 15.2000 13.7000 5.9700 4.0200 180.0000 90.0000 180.0000 70543.0000 0 $Composite 0 2; Spring_IMK   901403     140     143 $E $fy 6500.0000 15.2000 13.7000 5.9700 4.0200 180.0000 90.0000 180.0000 70543.0000 0 $Composite 0 2; 

# GRAVITY BEAMS SPRINGS
set gap 0.08;
Spring_Pinching   913304    1330    1334 24971.3750 $gap 1; Spring_Pinching   913402    1340    1342 24971.3750 $gap 1; 
Spring_Pinching   912304    1230    1234 28412.3125 $gap 1; Spring_Pinching   912402    1240    1242 28412.3125 $gap 1; 
Spring_Pinching   911304    1130    1134 28412.3125 $gap 1; Spring_Pinching   911402    1140    1142 28412.3125 $gap 1; 
Spring_Pinching   910304    1030    1034 28412.3125 $gap 1; Spring_Pinching   910402    1040    1042 28412.3125 $gap 1; 
Spring_Pinching   909304     930     934 28412.3125 $gap 1; Spring_Pinching   909402     940     942 28412.3125 $gap 1; 
Spring_Pinching   908304     830     834 28412.3125 $gap 1; Spring_Pinching   908402     840     842 28412.3125 $gap 1; 
Spring_Pinching   907304     730     734 28412.3125 $gap 1; Spring_Pinching   907402     740     742 28412.3125 $gap 1; 
Spring_Pinching   906304     630     634 28412.3125 $gap 1; Spring_Pinching   906402     640     642 28412.3125 $gap 1; 
Spring_Pinching   905304     530     534 28412.3125 $gap 1; Spring_Pinching   905402     540     542 28412.3125 $gap 1; 
Spring_Pinching   904304     430     434 28412.3125 $gap 1; Spring_Pinching   904402     440     442 28412.3125 $gap 1; 
Spring_Pinching   903304     330     334 28412.3125 $gap 1; Spring_Pinching   903402     340     342 28412.3125 $gap 1; 
Spring_Pinching   902304     230     234 28412.3125 $gap 1; Spring_Pinching   902402     240     242 28412.3125 $gap 1; 

###################################################################################################
#                                       BOUNDARY CONDITIONS                                       #
###################################################################################################

# MF SUPPORTS
fix 110 1 1 1; 
fix 120 1 1 1; 

# EGF SUPPORTS
fix 130 1 1 0; fix 140 1 1 0; 

# MF FLOOR MOVEMENT
equalDOF 413104 413204 1; 
equalDOF 412104 412204 1; 
equalDOF 411104 411204 1; 
equalDOF 410104 410204 1; 
equalDOF 409104 409204 1; 
equalDOF 408104 408204 1; 
equalDOF 407104 407204 1; 
equalDOF 406104 406204 1; 
equalDOF 405104 405204 1; 
equalDOF 404104 404204 1; 
equalDOF 403104 403204 1; 
equalDOF 402104 402204 1; 

# BEAM MID-SPAN HORIZONTAL MOVEMENT CONSTRAINT
equalDOF 412104 212101 1; 
equalDOF 410104 210101 1; 
equalDOF 408104 208101 1; 
equalDOF 406104 206101 1; 
equalDOF 404104 204101 1; 
equalDOF 402104 202101 1; 

# EGF FLOOR MOVEMENT
equalDOF 1330 1340 1;
equalDOF 1230 1240 1;
equalDOF 1130 1140 1;
equalDOF 1030 1040 1;
equalDOF 930 940 1;
equalDOF 830 840 1;
equalDOF 730 740 1;
equalDOF 630 640 1;
equalDOF 530 540 1;
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
recorder Node -file $MainFolder/EigenAnalysis/EigenVectorsMode1.out -node 402104 403104 404104 405104 406104 407104 408104 409104 410104 411104 412104 413104  -dof 1 "eigen  1";
recorder Node -file $MainFolder/EigenAnalysis/EigenVectorsMode2.out -node 402104 403104 404104 405104 406104 407104 408104 409104 410104 411104 412104 413104  -dof 1 "eigen  2";
recorder Node -file $MainFolder/EigenAnalysis/EigenVectorsMode3.out -node 402104 403104 404104 405104 406104 407104 408104 409104 410104 411104 412104 413104  -dof 1 "eigen  3";
recorder Node -file $MainFolder/EigenAnalysis/EigenVectorsMode4.out -node 402104 403104 404104 405104 406104 407104 408104 409104 410104 411104 412104 413104  -dof 1 "eigen  4";
recorder Node -file $MainFolder/EigenAnalysis/EigenVectorsMode5.out -node 402104 403104 404104 405104 406104 407104 408104 409104 410104 411104 412104 413104  -dof 1 "eigen  5";
recorder Node -file $MainFolder/EigenAnalysis/EigenVectorsMode6.out -node 402104 403104 404104 405104 406104 407104 408104 409104 410104 411104 412104 413104  -dof 1 "eigen  6";
recorder Node -file $MainFolder/EigenAnalysis/EigenVectorsMode7.out -node 402104 403104 404104 405104 406104 407104 408104 409104 410104 411104 412104 413104  -dof 1 "eigen  7";
recorder Node -file $MainFolder/EigenAnalysis/EigenVectorsMode8.out -node 402104 403104 404104 405104 406104 407104 408104 409104 410104 411104 412104 413104  -dof 1 "eigen  8";
recorder Node -file $MainFolder/EigenAnalysis/EigenVectorsMode9.out -node 402104 403104 404104 405104 406104 407104 408104 409104 410104 411104 412104 413104  -dof 1 "eigen  9";
recorder Node -file $MainFolder/EigenAnalysis/EigenVectorsMode10.out -node 402104 403104 404104 405104 406104 407104 408104 409104 410104 411104 412104 413104  -dof 1 "eigen  10";
recorder Node -file $MainFolder/EigenAnalysis/EigenVectorsMode11.out -node 402104 403104 404104 405104 406104 407104 408104 409104 410104 411104 412104 413104  -dof 1 "eigen  11";
recorder Node -file $MainFolder/EigenAnalysis/EigenVectorsMode12.out -node 402104 403104 404104 405104 406104 407104 408104 409104 410104 411104 412104 413104  -dof 1 "eigen  12";

# TIME
recorder Node -file $MainFolder/$SubFolder/Time.out  -time -node 110 -dof 1 disp;

# SUPPORT REACTIONS
recorder Node -file $MainFolder/$SubFolder/Support1.out -node     110 -dof 1 2 6 reaction; recorder Node -file $MainFolder/$SubFolder/Support2.out -node     120 -dof 1 2 6 reaction; recorder Node -file $MainFolder/$SubFolder/Support3.out -node     130 -dof 1 2 6 reaction; recorder Node -file $MainFolder/$SubFolder/Support4.out -node     140 -dof 1 2 6 reaction; 

# FLOOR LATERAL DISPLACEMENT
recorder Node -file $MainFolder/$SubFolder/Disp13_MF.out  -node  413104 -dof 1 disp; 
recorder Node -file $MainFolder/$SubFolder/Disp12_MF.out  -node  412104 -dof 1 disp; 
recorder Node -file $MainFolder/$SubFolder/Disp11_MF.out  -node  411104 -dof 1 disp; 
recorder Node -file $MainFolder/$SubFolder/Disp10_MF.out  -node  410104 -dof 1 disp; 
recorder Node -file $MainFolder/$SubFolder/Disp9_MF.out  -node  409104 -dof 1 disp; 
recorder Node -file $MainFolder/$SubFolder/Disp8_MF.out  -node  408104 -dof 1 disp; 
recorder Node -file $MainFolder/$SubFolder/Disp7_MF.out  -node  407104 -dof 1 disp; 
recorder Node -file $MainFolder/$SubFolder/Disp6_MF.out  -node  406104 -dof 1 disp; 
recorder Node -file $MainFolder/$SubFolder/Disp5_MF.out  -node  405104 -dof 1 disp; 
recorder Node -file $MainFolder/$SubFolder/Disp4_MF.out  -node  404104 -dof 1 disp; 
recorder Node -file $MainFolder/$SubFolder/Disp3_MF.out  -node  403104 -dof 1 disp; 
recorder Node -file $MainFolder/$SubFolder/Disp2_MF.out  -node  402104 -dof 1 disp; 

# STORY DRIFT RATIO
recorder Drift -file $MainFolder/$SubFolder/SDR12_MF.out -iNode  412104 -jNode  413104 -dof 1 -perpDirn 2; 
recorder Drift -file $MainFolder/$SubFolder/SDR11_MF.out -iNode  411104 -jNode  412104 -dof 1 -perpDirn 2; 
recorder Drift -file $MainFolder/$SubFolder/SDR10_MF.out -iNode  410104 -jNode  411104 -dof 1 -perpDirn 2; 
recorder Drift -file $MainFolder/$SubFolder/SDR9_MF.out -iNode  409104 -jNode  410104 -dof 1 -perpDirn 2; 
recorder Drift -file $MainFolder/$SubFolder/SDR8_MF.out -iNode  408104 -jNode  409104 -dof 1 -perpDirn 2; 
recorder Drift -file $MainFolder/$SubFolder/SDR7_MF.out -iNode  407104 -jNode  408104 -dof 1 -perpDirn 2; 
recorder Drift -file $MainFolder/$SubFolder/SDR6_MF.out -iNode  406104 -jNode  407104 -dof 1 -perpDirn 2; 
recorder Drift -file $MainFolder/$SubFolder/SDR5_MF.out -iNode  405104 -jNode  406104 -dof 1 -perpDirn 2; 
recorder Drift -file $MainFolder/$SubFolder/SDR4_MF.out -iNode  404104 -jNode  405104 -dof 1 -perpDirn 2; 
recorder Drift -file $MainFolder/$SubFolder/SDR3_MF.out -iNode  403104 -jNode  404104 -dof 1 -perpDirn 2; 
recorder Drift -file $MainFolder/$SubFolder/SDR2_MF.out -iNode  402104 -jNode  403104 -dof 1 -perpDirn 2; 
recorder Drift -file $MainFolder/$SubFolder/SDR1_MF.out -iNode     110 -jNode  402104 -dof 1 -perpDirn 2; 

# COLUMN ELASTIC ELEMENT FORCES
recorder Element -file $MainFolder/$SubFolder/Column121.out -ele  612100 force; recorder Element -file $MainFolder/$SubFolder/Column122.out -ele  612200 force; recorder Element -file $MainFolder/$SubFolder/Column123.out -ele  612300 force; recorder Element -file $MainFolder/$SubFolder/Column124.out -ele  612400 force; 
recorder Element -file $MainFolder/$SubFolder/Column111.out -ele  611101 force; recorder Element -file $MainFolder/$SubFolder/Column112.out -ele  611201 force; recorder Element -file $MainFolder/$SubFolder/Column113.out -ele  611301 force; recorder Element -file $MainFolder/$SubFolder/Column114.out -ele  611401 force; 
recorder Element -file $MainFolder/$SubFolder/Column101.out -ele  610100 force; recorder Element -file $MainFolder/$SubFolder/Column102.out -ele  610200 force; recorder Element -file $MainFolder/$SubFolder/Column103.out -ele  610300 force; recorder Element -file $MainFolder/$SubFolder/Column104.out -ele  610400 force; 
recorder Element -file $MainFolder/$SubFolder/Column91.out -ele  609101 force; recorder Element -file $MainFolder/$SubFolder/Column92.out -ele  609201 force; recorder Element -file $MainFolder/$SubFolder/Column93.out -ele  609301 force; recorder Element -file $MainFolder/$SubFolder/Column94.out -ele  609401 force; 
recorder Element -file $MainFolder/$SubFolder/Column81.out -ele  608100 force; recorder Element -file $MainFolder/$SubFolder/Column82.out -ele  608200 force; recorder Element -file $MainFolder/$SubFolder/Column83.out -ele  608300 force; recorder Element -file $MainFolder/$SubFolder/Column84.out -ele  608400 force; 
recorder Element -file $MainFolder/$SubFolder/Column71.out -ele  607101 force; recorder Element -file $MainFolder/$SubFolder/Column72.out -ele  607201 force; recorder Element -file $MainFolder/$SubFolder/Column73.out -ele  607301 force; recorder Element -file $MainFolder/$SubFolder/Column74.out -ele  607401 force; 
recorder Element -file $MainFolder/$SubFolder/Column61.out -ele  606100 force; recorder Element -file $MainFolder/$SubFolder/Column62.out -ele  606200 force; recorder Element -file $MainFolder/$SubFolder/Column63.out -ele  606300 force; recorder Element -file $MainFolder/$SubFolder/Column64.out -ele  606400 force; 
recorder Element -file $MainFolder/$SubFolder/Column51.out -ele  605101 force; recorder Element -file $MainFolder/$SubFolder/Column52.out -ele  605201 force; recorder Element -file $MainFolder/$SubFolder/Column53.out -ele  605301 force; recorder Element -file $MainFolder/$SubFolder/Column54.out -ele  605401 force; 
recorder Element -file $MainFolder/$SubFolder/Column41.out -ele  604100 force; recorder Element -file $MainFolder/$SubFolder/Column42.out -ele  604200 force; recorder Element -file $MainFolder/$SubFolder/Column43.out -ele  604300 force; recorder Element -file $MainFolder/$SubFolder/Column44.out -ele  604400 force; 
recorder Element -file $MainFolder/$SubFolder/Column31.out -ele  603101 force; recorder Element -file $MainFolder/$SubFolder/Column32.out -ele  603201 force; recorder Element -file $MainFolder/$SubFolder/Column33.out -ele  603301 force; recorder Element -file $MainFolder/$SubFolder/Column34.out -ele  603401 force; 
recorder Element -file $MainFolder/$SubFolder/Column21.out -ele  602100 force; recorder Element -file $MainFolder/$SubFolder/Column22.out -ele  602200 force; recorder Element -file $MainFolder/$SubFolder/Column23.out -ele  602300 force; recorder Element -file $MainFolder/$SubFolder/Column24.out -ele  602400 force; 
recorder Element -file $MainFolder/$SubFolder/Column11.out -ele  601100 force; recorder Element -file $MainFolder/$SubFolder/Column12.out -ele  601200 force; recorder Element -file $MainFolder/$SubFolder/Column13.out -ele  601300 force; recorder Element -file $MainFolder/$SubFolder/Column14.out -ele  601400 force; 

# BRACE CORNER RIGID LINKS FORCES
recorder Element -file $MainFolder/$SubFolder/CGP121.out -ele  713199 globalForce; recorder Element -file $MainFolder/$SubFolder/CGP122.out -ele  713299 globalForce; 
recorder Element -file $MainFolder/$SubFolder/CGP111.out -ele  711111 globalForce; recorder Element -file $MainFolder/$SubFolder/CGP112.out -ele  711211 globalForce; 
recorder Element -file $MainFolder/$SubFolder/CGP101.out -ele  711199 globalForce; recorder Element -file $MainFolder/$SubFolder/CGP102.out -ele  711299 globalForce; 
recorder Element -file $MainFolder/$SubFolder/CGP91.out -ele  709111 globalForce; recorder Element -file $MainFolder/$SubFolder/CGP92.out -ele  709211 globalForce; 
recorder Element -file $MainFolder/$SubFolder/CGP81.out -ele  709199 globalForce; recorder Element -file $MainFolder/$SubFolder/CGP82.out -ele  709299 globalForce; 
recorder Element -file $MainFolder/$SubFolder/CGP71.out -ele  707111 globalForce; recorder Element -file $MainFolder/$SubFolder/CGP72.out -ele  707211 globalForce; 
recorder Element -file $MainFolder/$SubFolder/CGP61.out -ele  707199 globalForce; recorder Element -file $MainFolder/$SubFolder/CGP62.out -ele  707299 globalForce; 
recorder Element -file $MainFolder/$SubFolder/CGP51.out -ele  705111 globalForce; recorder Element -file $MainFolder/$SubFolder/CGP52.out -ele  705211 globalForce; 
recorder Element -file $MainFolder/$SubFolder/CGP41.out -ele  705199 globalForce; recorder Element -file $MainFolder/$SubFolder/CGP42.out -ele  705299 globalForce; 
recorder Element -file $MainFolder/$SubFolder/CGP31.out -ele  703111 globalForce; recorder Element -file $MainFolder/$SubFolder/CGP32.out -ele  703211 globalForce; 
recorder Element -file $MainFolder/$SubFolder/CGP21.out -ele  703199 globalForce; recorder Element -file $MainFolder/$SubFolder/CGP22.out -ele  703299 globalForce; 
recorder Element -file $MainFolder/$SubFolder/CGP11.out -ele  701111 globalForce; recorder Element -file $MainFolder/$SubFolder/CGP12.out -ele  701211 globalForce; 

###################################################################################################
#                                              NODAL MASS                                         #
###################################################################################################

set g 386.10;
mass 413104 0.1777  1.e-9 1.e-9; mass 413204 0.1777  1.e-9 1.e-9; mass 1330 0.4881  1.e-9 1.e-9; mass 1340 0.4881  1.e-9 1.e-9; 
mass 412104 0.2506  1.e-9 1.e-9; mass 412204 0.2506  1.e-9 1.e-9; mass 1230 0.4516  1.e-9 1.e-9; mass 1240 0.4516  1.e-9 1.e-9; 
mass 411104 0.2506  1.e-9 1.e-9; mass 411204 0.2506  1.e-9 1.e-9; mass 1130 0.4516  1.e-9 1.e-9; mass 1140 0.4516  1.e-9 1.e-9; 
mass 410104 0.2506  1.e-9 1.e-9; mass 410204 0.2506  1.e-9 1.e-9; mass 1030 0.4516  1.e-9 1.e-9; mass 1040 0.4516  1.e-9 1.e-9; 
mass 409104 0.2506  1.e-9 1.e-9; mass 409204 0.2506  1.e-9 1.e-9; mass 930 0.4516  1.e-9 1.e-9; mass 940 0.4516  1.e-9 1.e-9; 
mass 408104 0.2506  1.e-9 1.e-9; mass 408204 0.2506  1.e-9 1.e-9; mass 830 0.4516  1.e-9 1.e-9; mass 840 0.4516  1.e-9 1.e-9; 
mass 407104 0.2506  1.e-9 1.e-9; mass 407204 0.2506  1.e-9 1.e-9; mass 730 0.4516  1.e-9 1.e-9; mass 740 0.4516  1.e-9 1.e-9; 
mass 406104 0.2506  1.e-9 1.e-9; mass 406204 0.2506  1.e-9 1.e-9; mass 630 0.4516  1.e-9 1.e-9; mass 640 0.4516  1.e-9 1.e-9; 
mass 405104 0.2506  1.e-9 1.e-9; mass 405204 0.2506  1.e-9 1.e-9; mass 530 0.4516  1.e-9 1.e-9; mass 540 0.4516  1.e-9 1.e-9; 
mass 404104 0.2506  1.e-9 1.e-9; mass 404204 0.2506  1.e-9 1.e-9; mass 430 0.4516  1.e-9 1.e-9; mass 440 0.4516  1.e-9 1.e-9; 
mass 403104 0.2506  1.e-9 1.e-9; mass 403204 0.2506  1.e-9 1.e-9; mass 330 0.4516  1.e-9 1.e-9; mass 340 0.4516  1.e-9 1.e-9; 
mass 402104 0.2506  1.e-9 1.e-9; mass 402204 0.2506  1.e-9 1.e-9; mass 230 0.4516  1.e-9 1.e-9; mass 240 0.4516  1.e-9 1.e-9; 

constraints Plain;

###################################################################################################
#                                        EIGEN VALUE ANALYSIS                                     #
###################################################################################################

set pi [expr 2.0*asin(1.0)];
set nEigen 12;
set lambdaN [eigen [expr $nEigen]];
set lambda1 [lindex $lambdaN 0];
set lambda2 [lindex $lambdaN 1];
set lambda3 [lindex $lambdaN 2];
set lambda4 [lindex $lambdaN 3];
set lambda5 [lindex $lambdaN 4];
set lambda6 [lindex $lambdaN 5];
set lambda7 [lindex $lambdaN 6];
set lambda8 [lindex $lambdaN 7];
set lambda9 [lindex $lambdaN 8];
set lambda10 [lindex $lambdaN 9];
set lambda11 [lindex $lambdaN 10];
set lambda12 [lindex $lambdaN 11];
set w1 [expr pow($lambda1,0.5)];
set w2 [expr pow($lambda2,0.5)];
set w3 [expr pow($lambda3,0.5)];
set w4 [expr pow($lambda4,0.5)];
set w5 [expr pow($lambda5,0.5)];
set w6 [expr pow($lambda6,0.5)];
set w7 [expr pow($lambda7,0.5)];
set w8 [expr pow($lambda8,0.5)];
set w9 [expr pow($lambda9,0.5)];
set w10 [expr pow($lambda10,0.5)];
set w11 [expr pow($lambda11,0.5)];
set w12 [expr pow($lambda12,0.5)];
set T1 [expr round(2.0*$pi/$w1 *1000.)/1000.];
set T2 [expr round(2.0*$pi/$w2 *1000.)/1000.];
set T3 [expr round(2.0*$pi/$w3 *1000.)/1000.];
set T4 [expr round(2.0*$pi/$w4 *1000.)/1000.];
set T5 [expr round(2.0*$pi/$w5 *1000.)/1000.];
set T6 [expr round(2.0*$pi/$w6 *1000.)/1000.];
set T7 [expr round(2.0*$pi/$w7 *1000.)/1000.];
set T8 [expr round(2.0*$pi/$w8 *1000.)/1000.];
set T9 [expr round(2.0*$pi/$w9 *1000.)/1000.];
set T10 [expr round(2.0*$pi/$w10 *1000.)/1000.];
set T11 [expr round(2.0*$pi/$w11 *1000.)/1000.];
set T12 [expr round(2.0*$pi/$w12 *1000.)/1000.];
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
	load 413103 0. -50.681 0.; 	load 413203 0. -50.681 0.; 
	load 412103 0. -59.963 0.; 	load 412203 0. -59.963 0.; 
	load 411103 0. -59.963 0.; 	load 411203 0. -59.963 0.; 
	load 410103 0. -59.963 0.; 	load 410203 0. -59.963 0.; 
	load 409103 0. -59.963 0.; 	load 409203 0. -59.963 0.; 
	load 408103 0. -59.963 0.; 	load 408203 0. -59.963 0.; 
	load 407103 0. -59.963 0.; 	load 407203 0. -59.963 0.; 
	load 406103 0. -59.963 0.; 	load 406203 0. -59.963 0.; 
	load 405103 0. -59.963 0.; 	load 405203 0. -59.963 0.; 
	load 404103 0. -59.963 0.; 	load 404203 0. -59.963 0.; 
	load 403103 0. -59.963 0.; 	load 403203 0. -59.963 0.; 
	load 402103 0. -59.963 0.; 	load 402203 0. -59.963 0.; 

	# EGF COLUMN LOADS
	load 1330 0. -232.734375 0.; 	load 1340 0. -232.734375 0.; 
	load 1230 0. -258.468750 0.; 	load 1240 0. -258.468750 0.; 
	load 1130 0. -258.468750 0.; 	load 1140 0. -258.468750 0.; 
	load 1030 0. -258.468750 0.; 	load 1040 0. -258.468750 0.; 
	load 930 0. -258.468750 0.; 	load 940 0. -258.468750 0.; 
	load 830 0. -258.468750 0.; 	load 840 0. -258.468750 0.; 
	load 730 0. -258.468750 0.; 	load 740 0. -258.468750 0.; 
	load 630 0. -258.468750 0.; 	load 640 0. -258.468750 0.; 
	load 530 0. -258.468750 0.; 	load 540 0. -258.468750 0.; 
	load 430 0. -258.468750 0.; 	load 440 0. -258.468750 0.; 
	load 330 0. -258.468750 0.; 	load 340 0. -258.468750 0.; 
	load 230 0. -258.468750 0.; 	load 240 0. -258.468750 0.; 

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

puts "Seismic Weight= 7572.319 kip";
puts "Seismic Mass=  16.780 kip.sec2/in";

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
region 2 -node  402104 402204 230 240 403104 403204 330 340 404104 404204 430 440 405104 405204 530 540 406104 406204 630 640 407104 407204 730 740 408104 408204 830 840 409104 409204 930 940 410104 410204 1030 1040 411104 411204 1130 1140 412104 412204 1230 1240 413104 413204 1330 1340  -rayleigh $a0 0.0 0.0 0.0;
region 3 -eleRange  900000  999999 -rayleigh 0.0 0.0 [expr $a1_mod/10] 0.0;

# GROUND MOTION ACCELERATION FILE INPUT
set AccelSeries "Series -dt $GMdt -filePath $GMfile -factor  [expr $EqSF * $g]"
pattern UniformExcitation  200 1 -accel $AccelSeries

set MF_FloorNodes [list  402104 403104 404104 405104 406104 407104 408104 409104 410104 411104 412104 413104 ];
set EGF_FloorNodes [list  230 330 430 530 630 730 830 930 1030 1130 1230 1330 ];
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
