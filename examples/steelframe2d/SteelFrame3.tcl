# Steel two story, two bay frame # Static pushover analysis with hinged element # Fiber hinge
# Units: kip, in
#
#
# @__________@_@__________@ _
# |           |           |
# |           |           | 54"
# |           |           |
# |@__________@|@__________@| _
# |            |            |
# |            |            |
# |            |            | 54"
# |            |            | _
# ===         ===          ===
# | 108"       |    108"    |
#
# comment out one of lines if wish to see graphics or not
#set displayMode "displayON"
set displayMode "displayOFF"
model BasicBuilder -ndm 2 -ndf 3
# tag X Y
node 1 0 0
node 2 0 54
node 3 0 108
node 4 108 0
node 5 108 54
node 6 108 108
node 7 216 0
node 8 216 54
node 9 216 108
# node DX DY RZ
fix 1 1 1 1
fix 4 1 1 1
fix 7 1 1 1
# Define beam and column property variables
set E 29000.0
set fy 60.0
# tag E fy Hiso Hkin
uniaxialMaterial Hardening 1 $E $fy 0 1000
# Columns W6x12:
set Acol 3.55
set Icol 22.1
# Beams S4x7.7:
set Agir 2.26
set Igir 6.08
source Wsection.tcl
# Beam hinge section ... S4x7.7
# tag matID d tw bf tf nfdw nftw nfbf nftf
Wsection 1 1 4.00 0.193 2.663 0.293 10 1 1 2
# Coordinate transformation
geomTransf Linear 1
# tag ndI ndJ A E I transfTag
element elasticBeamColumn 9 1 2 $Acol $E $Icol 1
element elasticBeamColumn 10 2 3 $Acol $E $Icol 1
element elasticBeamColumn 11 4 5 $Acol $E $Icol 1
element elasticBeamColumn 12 5 6 $Acol $E $Icol 1
element elasticBeamColumn 13 7 8 $Acol $E $Icol 1
element elasticBeamColumn 14 8 9 $Acol $E $Icol 1
# tag ndI ndJ secI lenI secJ lenJ E A I transfTag
element beamWithHinges 15 2 5 1 0.1 1 0.1 $E $Agir $Igir 1
element beamWithHinges 16 3 6 1 0.1 1 0.1 $E $Agir $Igir 1
element beamWithHinges 17 5 8 1 0.1 1 0.1 $E $Agir $Igir 1
element beamWithHinges 18 6 9 1 0.1 1 0.1 $E $Agir $Igir 1
# Constant gravity loads
pattern Plain 1 Constant {
# node FX FY MZ
load 2 0.0 -1.0 0.0
load 5 0.0 -4.0 0.0
load 8 0.0 -1.0 0.0
load 3 0.0 -2.0 0.0
load 6 0.0 -6.0 0.0
load 9 0.0 -2.0 0.0
}
# Lateral load
set H 0.2
pattern Plain 2 Linear {
# node FX FY MZ
load 2 $H 0.0 0.0
load 3 $H 0.0 0.0
}
# Record displacements at 1st floor and roof
recorder Node StFrPZL3.out disp -time -node 2 3 5 6 -dof 1
# Record section forces
recorder Element 15 -file StFrPZL3el1.out -time section 1 force
recorder Element 15 -file StFrPZL3el2.out -time section 2 force
recorder Element 16 -file StFrPZL3el3.out -time section 1 force
recorder Element 16 -file StFrPZL3el4.out -time section 2 force
recorder Element 17 -file StFrPZL3el5.out -time section 1 force
recorder Element 17 -file StFrPZL3el6.out -time section 2 force
recorder Element 18 -file StFrPZL3el7.out -time section 1 force
recorder Element 18 -file StFrPZL3el8.out -time section 2 force
# Record beam & column forces
recorder Element 9 -file StFrPZL3el9.out -time forces
recorder Element 10 -file StFrPZL3el10.out -time forces
recorder Element 11 -file StFrPZL3el11.out -time forces
recorder Element 12 -file StFrPZL3el12.out -time forces
recorder Element 13 -file StFrPZL3el13.out -time forces
recorder Element 14 -file StFrPZL3el14.out -time forces
recorder Element 15 -file StFrPZL3el15.out -time forces
recorder Element 16 -file StFrPZL3el16.out -time forces
recorder Element 17 -file StFrPZL3el17.out -time forces
recorder Element 18 -file StFrPZL3el18.out -time forces

integrator LoadControl 1 3 0.2 1
test EnergyIncr 1.0e-6 10 1
algorithm Newton
numberer Plain
constraints Plain
system SparseGeneral
analysis Static
# Perform the pushover analysis
analyze 20
# Switch to displacement control
integrator DisplacementControl 3 1 .001 3 .001 1.0
# Continue the pushover analysis
#analyze 20
# Get the roof displacement
print node 2 3 5 6
