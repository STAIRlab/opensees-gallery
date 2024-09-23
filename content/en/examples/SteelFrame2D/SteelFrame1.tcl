# Steel two story, two bay frame 
# Static pushover analysis with zero length elements 
# Pinned column bases 
# Rotational springs w/EPP behavior
# Units: kip, in
#
#
# @__________@_@__________@ _
# | | |
# | | | 54"
# | | |
# |@__________@|@__________@| _
# | | |
# | | |
# | | | 54"
# | | | _
# ^ ^ ^
# | 108" | 108" |
# comment out one of lines if wish to see graphics or not
#set displayMode "displayON"
set displayMode "displayOFF"
model BasicBuilder -ndm 2 -ndf 3
# tag X Y
node 1 0 0
node 2 0 54
node 3 0 54
node 4 0 108
node 5 0 108
node 6 108 0
node 7 108 54
node 8 108 54
node 9 108 54
node 10 108 108
node 11 108 108
node 12 108 108
node 13 216 0
node 14 216 54
node 15 216 54
node 16 216 108
node 17 216 108
# node DX DY RZ
fix 1 1 1 0
fix 6 1 1 0
fix 13 1 1 0
# Define beam and column property variables
set E 29000
# Columns W6x12:
set Acol 3.55
set Icol 22.1
# Beams S4x7.7:
set Agir 2.26
set Igir 6.08
# Define moment-rotation relationship for spring - EPP
# E ep
uniaxialMaterial ElasticPP 1 26290 0.005
# Source in proc to define rotational zero-length element
source rotSpring2D.tcl
# id ndR ndC matID
rotSpring2D 1 2 3 1
rotSpring2D 2 4 5 1
rotSpring2D 3 7 8 1
rotSpring2D 4 8 9 1
rotSpring2D 5 10 11 1
rotSpring2D 6 11 12 1
rotSpring2D 7 14 15 1
rotSpring2D 8 16 17 1
# Coordinate transformation
geomTransf Linear 1
# id ndI ndJ A E I transfTag
element elasticBeamColumn 9 1 2 $Acol $E $Icol 1
element elasticBeamColumn 10 2 4 $Acol $E $Icol 1
element elasticBeamColumn 11 6 8 $Acol $E $Icol 1
element elasticBeamColumn 12 8 11 $Acol $E $Icol 1
element elasticBeamColumn 13 13 15 $Acol $E $Icol 1
element elasticBeamColumn 14 15 17 $Acol $E $Icol 1
element elasticBeamColumn 15 3 7 $Agir $E $Igir 1
element elasticBeamColumn 16 5 10 $Agir $E $Igir 1
element elasticBeamColumn 17 9 14 $Agir $E $Igir 1
element elasticBeamColumn 18 12 16 $Agir $E $Igir 1
# Constant gravity loads
pattern Plain 1 Constant {
# node FX FY MZ
load 2 0.0 -1.0 0.0
load 8 0.0 -4.0 0.0
load 15 0.0 -1.0 0.0
load 4 0.0 -2.0 0.0
load 11 0.0 -6.0 0.0
load 17 0.0 -2.0 0.0
}
# Lateral load
set H 0.2
pattern Plain 2 Linear {
# node FX FY MZ
load 2 $H 0.0 0.0
load 3 $H 0.0 0.0
}
# Record displacements at 1st floor and roof
recorder Node StFrPZL1.out disp -time -node 2 4 8 10 -dof 1
# Record spring forces
recorder Element 1 -file StFrPZL1el1.out -time forces
recorder Element 2 -file StFrPZL1el2.out -time forces
recorder Element 3 -file StFrPZL1el3.out -time forces
recorder Element 4 -file StFrPZL1el4.out -time forces
recorder Element 5 -file StFrPZL1el5.out -time forces
recorder Element 6 -file StFrPZL1el6.out -time forces
recorder Element 7 -file StFrPZL1el7.out -time forces
recorder Element 8 -file StFrPZL1el8.out -time forces
# Record beam & column forces
recorder Element 9 -file StFrPZL1el9.out -time forces
recorder Element 10 -file StFrPZL1el10.out -time forces
recorder Element 11 -file StFrPZL1el11.out -time forces
recorder Element 12 -file StFrPZL1el12.out -time forces
recorder Element 13 -file StFrPZL1el13.out -time forces
recorder Element 14 -file StFrPZL1el14.out -time forces
recorder Element 15 -file StFrPZL1el15.out -time forces
recorder Element 16 -file StFrPZL1el16.out -time forces
recorder Element 17 -file StFrPZL1el17.out -time forces
recorder Element 18 -file StFrPZL1el18.out -time forces
# Source in some commands to display the model
if {$displayMode == "displayON"} {
  source StFramePZLdisplay.tcl
}
integrator LoadControl 1 3 0.2 1
test EnergyIncr 1.0e-6 10 1
algorithm Newton
numberer Plain
constraints Transformation 1.0
system SparseGeneral
analysis Static
# Perform the pushover analysis
analyze 30
# Switch to displacement control
integrator DisplacementControl 4 1 .001 3 .001 1.0
# Continue the pushover analysis
analyze 20
# Get the roof displacement
print node 2 3 4 5

