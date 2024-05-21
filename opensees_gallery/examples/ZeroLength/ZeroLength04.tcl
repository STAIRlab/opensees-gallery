# Two translational springs # Transient EQ analysis
#
# https://opensees.berkeley.edu/OpenSees/manuals/ExamplesManual/HTML/806.htm
#
# Written: MHS
# Date: Feb 2000
# Units: kip, in
# Define the model builder
model BasicBuilder -ndm 2 -ndf 3
set g 386.4
# Set some variables
set L 120
set A 20
set E 30000
set I 1400
set M 0.02588
# Define nodes
node 1 0.0 0.0
node 2 0.0 0.0 -mass $M $M 0
node 3 $L 0.0
# Define single point constraints
fix 1 1 1 1
fix 3 1 1 1
# Define force-deformation relationship for spring
uniaxialMaterial ElasticPP 3 1050 0.02
uniaxialMaterial Elastic 4 -50
uniaxialMaterial Parallel 1 3 4
# id ndI ndJ mats dirs
element zeroLength 1 1 2 -mat 1 1 -dir 1 2
# Geometric transformation
geomTransf Linear 1
# id ndI ndJ A E I transf
element elasticBeamColumn 2 2 3 $A $E $I 1

# tag dir accel deltaT
pattern UniformExcitation 1 1 -accel "Path -filePath tabasFN.txt -dt 0.02 -factor $g"
pattern UniformExcitation 2 2 -accel "Path -filePath tabasFP.txt -dt 0.02 -factor $g"

recorder Node -file ZeroLength4.out disp -time -node 2 -dof 1 2

integrator Newmark 0.5 0.25
test EnergyIncr 1.0e-6 10 1
algorithm Newton
numberer Plain
constraints Transformation 1.0
system SparseGeneral
analysis Transient
analyze 1500 0.02

