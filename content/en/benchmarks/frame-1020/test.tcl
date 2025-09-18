verify about "Frame follower loading"

model  -ndm 3 -ndf 6

set ne 10
node 0 0.0 0 0 
node 1 10.0 0 0 
node 2 20.0 0 0 
node 3 30.0 0 0 
node 4 40.0 0 0 
node 5 50.0 0 0 
node 6 60.0 0 0 
node 7 70.0 0 0 
node 8 80.0 0 0 
node 9 90.0 0 0 
node 10 100.0 0 0 
fix 0 1 1 1 1 1 1

section ElasticFrame 1 -E 1 -G 1 -A 161538000.0 -Ay 161538000.0 -Az 161538000.0 -Iy 3500000000.0 -Iz 35000000.0 -J 35000000.0

geomTransf Linear 1 0 0 1 

element ExactFrame  1 {0  1} -section 1 -transform 1
element ExactFrame  2 {1  2} -section 1 -transform 1
element ExactFrame  3 {2  3} -section 1 -transform 1
element ExactFrame  4 {3  4} -section 1 -transform 1
element ExactFrame  5 {4  5} -section 1 -transform 1
element ExactFrame  6 {5  6} -section 1 -transform 1
element ExactFrame  7 {6  7} -section 1 -transform 1
element ExactFrame  8 {7  8} -section 1 -transform 1
element ExactFrame  9 {8  9} -section 1 -transform 1
element ExactFrame 10 {9 10} -section 1 -transform 1

foreach i [range $ne] {nodeRotation $i}

pattern Plain 1 Linear 
eleLoad Frame Dirac -force {0 1 0} -basis director -offset {1.0 0 0} -pattern 1 -elements {10}
system FullGeneral 
integrator LoadControl 300.0 
#
#test EnergyIncr 1e-12 8 0
test EnergyIncr 1e-12 10 0
algorithm Newton 
analysis Static 

verify value [analyze 500] 0

