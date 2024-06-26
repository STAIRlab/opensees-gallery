# zhyang@ucdavis.edu
# jeremic@ucdavis.edu
# 23jan2001
# ################################
# create the modelbuilder
# #################################
model BasicBuilder -ndm 3 -ndf 3
set displayMode "displayON"
#set displayMode "displayOFF"
set g 9.81

# ################################
# build the model
# #################################
node 1 1.0 1.0 0.0
node 2 0.0 1.0 0.0
node 3 0.0 0.0 0.0
node 4 1.0 0.0 0.0
node 5 1.0 1.0 1.0
node 6 0.0 1.0 1.0
node 7 0.0 0.0 1.0
node 8 1.0 0.0 1.0
fix 1 1 1 1
fix 2 1 1 1
fix 3 1 1 1
fix 4 1 1 1
fix 5 1 0 1
fix 6 1 0 1
fix 7 1 0 1
fix 8 1 0 1
equalDOF 5 8 2
equalDOF 6 7 2
# elastic material
nDMaterial ElasticIsotropic3D 1 70000 0.3

# the template material of yours
#sset YS {DruckerPrager }
#set PS {DruckerPrager 0.05}
#
#set startstress {50 0.001 0.0}
#set otherstress {0 0 0}
#set scalars {0.05 0 0.85}
#set tensors {0.0 0.0 0.0}
#set NOS 3
#set NOT 3
#set EPS {3000.0 3000.0 0.3 1.8 $startstress $otherstrain $otherstrain $otherstrain $otherstrain $NOS $scalars $NOT $tensors}
#
#nDMaterial Template 1 -YS $YS -PS $PS -EPS $EPS ......
# tag 8 nodes matID bforce1 bforce2 bforce3 massDensity

element brick 1 5 6 7 8 1 2 3 4 1 0.0 0.0 -9.81 1.8
set Series "Path -filePath tabasFN.txt -dt 0.02 -factor $g"
pattern UniformExcitation 1 2 -accel $Series
# create the recorder
#recorder Node Node.out disp -time -node 1 2 3 4 5 6 7 8 -dof 1 2 3
recorder Node node.out disp -time -node 5 -dof 1 2 3
recorder plot node.out HelloJoey 10 10 300 300 -columns 2 1
recorder plot node.out HelloJoey 10 10 300 300 -columns 3 1
# ################################
# create the analysis
# #################################
integrator Newmark 0.5 0.25
numberer Plain
#constraints Plain
constraints Penalty 1e12 1e12
#constraints Transformation
test NormDispIncr 1.0e-12 10 0
#constraints Lagrange 1.0 1.0
#test NormDispIncr 1.0e-10 10 1
algorithm Newton
numberer RCM
system UmfPack
analysis Transient
# ################################
# perform the analysis
# #################################
analyze 1000 0.02

