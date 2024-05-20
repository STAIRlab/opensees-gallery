#----------Create Model (2-D 3dof problem)-----------
#----------SAC 3 Storied Building, LA Down Town--------

wipe;

model BasicBuilder -ndm 2 -ndf 3;


#Unit kN,mm,Gpa (kN/mm2) [1Gpa =  1000 mpa]

# Create nodes
node 1 0.0 0.0;
node 2 9150 0.0;
node 3 18300 0.0;
node 4 27450 0.0;
node 5 36600 0.0;
node 6 45750 0.0;
node 7 0.0 3960 -mass 0.05973 0.0 0.0;
node 8 9150 3960 -mass 0.11947 0.0 0.0;
node 9 18300 3960 -mass 0.11947 0.0 0.0;
node 10 27450 3960 -mass 0.11947 0.0 0.0;
node 11 36600 3960 -mass 0.05973 0.0 0.0;
node 12 45750 3960;
node 13 0.0 7920 -mass 0.05973 0.0 0.0;
node 14 9150 7920 -mass 0.11947 0.0 0.0;
node 15 18300 7920 -mass 0.11947 0.0 0.0;
node 16 27450 7920 -mass 0.11947 0.0 0.0;
node 17 36600 7920 -mass 0.05973 0.0 0.0;
node 18 45750 7920;
node 19 0.0 11880 -mass 0.06462 0.0 0.0;
node 20 9150 11880 -mass 0.12923 0.0 0.0;
node 21 18300 11880 -mass 0.12923 0.0 0.0;
node 22 27450 11880 -mass 0.12923 0.0 0.0;
node 23 36600 11880 -mass 0.06462 0.0 0.0;
node 24 45750 11880;

#Intermediate nodes for YSPDs
node 25 13725 3960;
node 26 13725 7920;
node 27 13725 11880;

node 28 4575 3960;
node 29 4575 7920;
node 30 4575 11880;


node 31 22875 3960;
node 32 22875 7920;
node 33 22875 11880;




#Nodes for rotational hinge
node 101 27450 3960;
node 111 36600 3960;
node 161 27450 7920;
node 171 36600 7920;
node 221 27450 11880;
node 231 36600 11880;
node 123 45750 3960;
node 124 45750 3960;
node 183 45750 7920;
node 184 45750 7920;
node 243 45750 11880;



# Fix supports at node
fix 1 1 1 1;
fix 2 1 1 1;
fix 3 1 1 1;
fix 4 1 1 1;
fix 5 1 1 1;
fix 6 1 1 0;

#Beam Column Property (epsyp=fy/E)
set E 200.0;
set fy 0.345;

#Uniaxial materials
uniaxialMaterial Elastic 1 $E;
uniaxialMaterial Hardening 2 $E $fy 0.0 2.0;
uniaxialMaterial Elastic 3 1.0e-20;


#Column W14X257
set A_Col_1FB 48774;
set I_Col_1FB 1415186847;

#Column W14X311
set A_Col_2FB 58968;
set I_Col_2FB 1802282073;

#Column W14X68 (weak axis)
set A_Col_oth 12039;
set I_Col_oth 50364002;

#Trus Beam W21X44
set A_Beam_trs 8387;
set I_Beam_trs 350883092;

#Beam W33X118
set A_Beam_S1 22387;
set I_Beam_S1 2455765411;

#Beam W30X116
set A_Beam_S2 22064;
set I_Beam_S2 2052020928;

#Beam W24X68
set A_Beam_S3 12968;
set I_Beam_S3 761703509;

#Rigit Trus column
set A_Col_RT 1000000.0;
set I_Col_RT 1000000000000.0;

source Wsection.tcl;


# Beam hinge section
Wsection 1 2 835.66 13.97 292.10 18.80 10 1 1 2;
Wsection 2 2 762.00 14.35 266.70 21.59 10 1 1 2;
Wsection 3 2 601.98 10.54 227.84 14.86 10 1 1 2;

# Coordinate transformation
geomTransf PDelta 1;
#geomTransf Linear 1;


#Column Elements

element elasticBeamColumn 1 1 7 $A_Col_1FB $E $I_Col_1FB 1;
element elasticBeamColumn 2 7 13 $A_Col_1FB $E $I_Col_1FB 1;
element elasticBeamColumn 3 13 19 $A_Col_1FB $E $I_Col_1FB 1;

element elasticBeamColumn 4 2 8 $A_Col_2FB $E $I_Col_2FB 1;
element elasticBeamColumn 5 8 14 $A_Col_2FB $E $I_Col_2FB 1;
element elasticBeamColumn 6 14 20 $A_Col_2FB $E $I_Col_2FB 1;

element elasticBeamColumn 7 3 9 $A_Col_2FB $E $I_Col_2FB 1;
element elasticBeamColumn 8 9 15 $A_Col_2FB $E $I_Col_2FB 1;
element elasticBeamColumn 9 15 21 $A_Col_2FB $E $I_Col_2FB 1;
 
element elasticBeamColumn 10 4 10 $A_Col_1FB $E $I_Col_1FB 1;
element elasticBeamColumn 11 10 16 $A_Col_1FB $E $I_Col_1FB 1;
element elasticBeamColumn 12 16 22 $A_Col_1FB $E $I_Col_1FB 1;

element elasticBeamColumn 13 5 11 $A_Col_oth $E $I_Col_oth 1;
element elasticBeamColumn 14 11 17 $A_Col_oth $E $I_Col_oth 1;
element elasticBeamColumn 15 17 23 $A_Col_oth $E $I_Col_oth 1;


#Beam Elements

element beamWithHinges 16 7 28 1 915 1 0 $E $A_Beam_S1 $I_Beam_S1 1;
element beamWithHinges 161 28 8 1 0 1 915 $E $A_Beam_S1 $I_Beam_S1 1;
element beamWithHinges 17 8 25 1 915 1 0 $E $A_Beam_S1 $I_Beam_S1 1;
element beamWithHinges 18 25 9 1 0 1 915 $E $A_Beam_S1 $I_Beam_S1 1;
element beamWithHinges 19 9 31 1 915 1 0 $E $A_Beam_S1 $I_Beam_S1 1;
element beamWithHinges 191 31 10 1 0 1 915 $E $A_Beam_S1 $I_Beam_S1 1;

element beamWithHinges 20 13 29 2 915 2 0 $E $A_Beam_S2 $I_Beam_S2 1;
element beamWithHinges 201 29 14 2 0 2 915 $E $A_Beam_S2 $I_Beam_S2 1;
element beamWithHinges 21 14 26 2 915 2 0 $E $A_Beam_S2 $I_Beam_S2 1;
element beamWithHinges 22 26 15 2 0 2 915 $E $A_Beam_S2 $I_Beam_S2 1;
element beamWithHinges 23 15 32 2 915 2 0 $E $A_Beam_S2 $I_Beam_S2 1;
element beamWithHinges 231 32 16 2 0 2 915 $E $A_Beam_S2 $I_Beam_S2 1;

element beamWithHinges 24 19 30 3 915 3 0 $E $A_Beam_S3 $I_Beam_S3 1;
element beamWithHinges 241 30 20 3 0 3 915 $E $A_Beam_S3 $I_Beam_S3 1;
element beamWithHinges 25 20 27 3 915 3 0 $E $A_Beam_S3 $I_Beam_S3 1;
element beamWithHinges 26 27 21 3 0 3 915 $E $A_Beam_S3 $I_Beam_S3 1;
element beamWithHinges 27 21 33 3 915 3 0 $E $A_Beam_S3 $I_Beam_S3 1;
element beamWithHinges 271 33 22 3 0 3 915 $E $A_Beam_S3 $I_Beam_S3 1;

#Truss Beam Elements

element elasticBeamColumn 28 101 111 $A_Beam_trs $E $I_Beam_trs 1;
element elasticBeamColumn 29 161 171 $A_Beam_trs $E $I_Beam_trs 1;
element elasticBeamColumn 30 221 231 $A_Beam_trs $E $I_Beam_trs 1;

#Zerolength rotational spring (low stiffness)

element zeroLength 34 10 101 -mat 3 -dir 6;
element zeroLength 35 11 111 -mat 3 -dir 6;
element zeroLength 36 16 161 -mat 3 -dir 6;
element zeroLength 37 17 171 -mat 3 -dir 6;
element zeroLength 38 22 221 -mat 3 -dir 6;
element zeroLength 39 23 231 -mat 3 -dir 6;

equalDOF 10 101 1 2;
equalDOF 11 111 1 2;
equalDOF 16 161 1 2;
equalDOF 17 171 1 2;
equalDOF 22 221 1 2;
equalDOF 23 231 1 2;


#Dummy rigid column

element elasticBeamColumn 31 6 123 $A_Col_RT $E $I_Col_RT 1;
element elasticBeamColumn 32 124 183 $A_Col_RT $E $I_Col_RT 1;
element elasticBeamColumn 33 184 243 $A_Col_RT $E $I_Col_RT 1;

element zeroLength 40 12 123 -mat 3 -dir 6;
element zeroLength 41 12 124 -mat 3 -dir 6;
element zeroLength 42 18 183 -mat 3 -dir 6;
element zeroLength 43 18 184 -mat 3 -dir 6;
element zeroLength 44 24 243 -mat 3 -dir 6;

equalDOF 12 123 1 2;
equalDOF 12 124 1 2;
equalDOF 18 183 1 2;
equalDOF 18 184 1 2;
equalDOF 24 243 1 2;

#Rigid Links (in horizontal direction only)

equalDOF 11 12 1;
equalDOF 17 18 1;
equalDOF 23 24 1;


#######################################################################################

#Brace Sections

set A_HSS1 1142.0;
set I_HSS1 1831418.0;

set A_HSS2 2174.0;
set I_HSS2 3246605.0;

set A_HSS3 3884.0;
set I_HSS3 4953154.0;


#Intermediate nodes for Brace
node 251 13725 3860;
node 261 13725 7820;
node 271 13725 11780;

node 281 4575 3860;
node 291 4575 7820;
node 301 4575 11780;

node 311 22875 3860;
node 321 22875 7820;
node 331 22875 11780;

#Braces

element elasticBeamColumn 45 2 251 $A_HSS1 $E $I_HSS1 1;
element elasticBeamColumn 46 3 251 $A_HSS1 $E $I_HSS1 1;
element elasticBeamColumn 47 8 261 $A_HSS1 $E $I_HSS1 1;
element elasticBeamColumn 48 9 261 $A_HSS1 $E $I_HSS1 1;
element elasticBeamColumn 49 14 271 $A_HSS1 $E $I_HSS1 1;
element elasticBeamColumn 50 15 271 $A_HSS1 $E $I_HSS1 1;


element elasticBeamColumn 451 1 281 $A_HSS1 $E $I_HSS1 1;
element elasticBeamColumn 461 2 281 $A_HSS1 $E $I_HSS1 1;
element elasticBeamColumn 471 7 291 $A_HSS1 $E $I_HSS1 1;
element elasticBeamColumn 481 8 291 $A_HSS1 $E $I_HSS1 1;
element elasticBeamColumn 491 13 301 $A_HSS1 $E $I_HSS1 1;
element elasticBeamColumn 501 14 301 $A_HSS1 $E $I_HSS1 1;


element elasticBeamColumn 453 3 311 $A_HSS1 $E $I_HSS1 1;
element elasticBeamColumn 463 4 31 $A_HSS1 $E $I_HSS1 1;
element elasticBeamColumn 473 9 321 $A_HSS1 $E $I_HSS1 1;
element elasticBeamColumn 483 10 321 $A_HSS1 $E $I_HSS1 1;
element elasticBeamColumn 493 15 331 $A_HSS1 $E $I_HSS1 1;
element elasticBeamColumn 503 16 331 $A_HSS1 $E $I_HSS1 1;



# Define  material

#uniaxialMaterial material tag alpha Ko n gama beta A q Zetas p Shi deltaShi Lamda tolerance maxNumberIter

uniaxialMaterial BWBN 4 0.012331839 26.76 1.213 0.5 0.5 1 0.52 0.96 0.018 0.41 0.00001 0.0300 0.001 1000; 
uniaxialMaterial BWBN 5 0.007746219 54.22 0.544 0.5 0.5 1 0.38 0.95 0.015 0.27 0.00001 0.0014 0.001 1000;
uniaxialMaterial BWBN 6 0.005240081 93.51 0.300 0.5 0.5 1 0.30 0.95 0.012 0.22 0.00001 0.0002 0.001 1000; 

uniaxialMaterial Elastic 7 1.0e-20;

# Define two node link element

element twoNodeLink 51 251 25 -mat 7 4 7 7 7 7 -dir 1 2 3 4 5 6 -orient 0 1 0 -1 0 0;
element twoNodeLink 52 261 26 -mat 7 4 7 7 7 7 -dir 1 2 3 4 5 6 -orient 0 1 0 -1 0 0;
element twoNodeLink 53 271 27 -mat 7 4 7 7 7 7 -dir 1 2 3 4 5 6 -orient 0 1 0 -1 0 0;

element twoNodeLink 511 281 28 -mat 7 4 7 7 7 7 -dir 1 2 3 4 5 6 -orient 0 1 0 -1 0 0;
element twoNodeLink 521 291 29 -mat 7 4 7 7 7 7 -dir 1 2 3 4 5 6 -orient 0 1 0 -1 0 0;
element twoNodeLink 531 301 30 -mat 7 4 7 7 7 7 -dir 1 2 3 4 5 6 -orient 0 1 0 -1 0 0;

element twoNodeLink 513 311 31 -mat 7 4 7 7 7 7 -dir 1 2 3 4 5 6 -orient 0 1 0 -1 0 0;
element twoNodeLink 523 321 32 -mat 7 4 7 7 7 7 -dir 1 2 3 4 5 6 -orient 0 1 0 -1 0 0;
element twoNodeLink 533 331 33 -mat 7 4 7 7 7 7 -dir 1 2 3 4 5 6 -orient 0 1 0 -1 0 0;


equalDOF 25 251 2;
equalDOF 26 261 2;
equalDOF 27 271 2;

equalDOF 28 281 2;
equalDOF 29 291 2;
equalDOF 30 301 2;

equalDOF 31 311 2;
equalDOF 32 321 2;
equalDOF 33 331 2;


########################################################################################


#Eigenvalue analysis
set pi 3.14159265;
set lambdaN [eigen 3];
set lambda1 [lindex $lambdaN 0];
set lambda2 [lindex $lambdaN 1];
set lambda3 [lindex $lambdaN 2];

set w1 [expr pow($lambda1,0.5)];
set w2 [expr pow($lambda2,0.5)];
set w3 [expr pow($lambda3,0.5)];

set T1 [expr 2.0*$pi/$w1];
set T2 [expr 2.0*$pi/$w2];
set T3 [expr 2.0*$pi/$w3];

#puts "T1 = $T1 s";
#puts "T2 = $T2 s";
#puts "T3 = $T3 s";


#UDL

pattern Plain 1 Constant {
eleLoad -ele 16 161 17 18 19 191 20 201 21 22 23 231 28 29 -type -beamUniform -0.02544 0.0;
eleLoad -ele 24 241 25 26 27 271 30 -type -beamUniform -0.02269 0.0;
}


#Constant gravity loads

pattern Plain 2 Constant {
load 12 0.0 -3757.0 0.0;
load 18 0.0 -3757.0 0.0;
load 24 0.0 -4240.5 0.0;
}


# Gravity-analysis
constraints Plain;
#constraints Transformation;
numberer Plain;
system BandGeneral;
#system UmfPack;
test NormDispIncr 1.0e-6 100;
algorithm Newton;
set NstepGravity 10;
set DGravity [expr 1.0/$NstepGravity];
integrator LoadControl $DGravity;
analysis Static;
analyze $NstepGravity;

# maintain constant gravity loads and reset time to zero
loadConst -time 0.0;
#puts "Model Built";

 
#Rayleigh Damping
set zeta 0.02;
set alphaM [expr $zeta*(2.0*$w1*$w3)/($w1+$w3)];
set betaK [expr 2.0*$zeta/($w1+$w3)];

region 1 -eleRange 1 30 rayleigh 0.0 0.0 $betaK 0.0;#Stiffness Damping
rayleigh $alphaM 0.0 0.0 0.0;#Mass Damping


