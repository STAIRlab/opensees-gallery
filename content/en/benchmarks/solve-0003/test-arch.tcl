#
model  -ndm 3 -ndf 6
node  1 -5000.0 0.0 0 
node  2 -4009.568694135459 179.6181055187626 0 
node  3 -3012.765365914115 319.6179637813475 0 
node  4 -2011.1741391101941 419.7770864617414 0 
node  5 -1006.386746445197 479.9363002877908 0 
node  6 -200.0 500.0 0 
node  7 1006.3867464451962 479.9363002877908 0 
node  8 2011.1741391101934 419.7770864617414 0 
node  9 3012.765365914115 319.6179637813475 0 
node 10 4009.568694135459 179.6181055187626 0 
node 11 5000.0 0.0 0 
fix  1 1 1 0 1 1 0 
fix 11 1 1 0 1 1 0 

section ElasticFrame 1 -A 10000.0 -E 200 -Iy 100000000.0 -Iz 100000000.0 -J 200000000.0 -G 200 -Ay 1000000.0 -Az 1000000.0

geomTransf Corotational02 1 0 0 1 

element ForceFrame  1  1  2 -section 1 -transform 1
element ForceFrame  2  2  3 -section 1 -transform 1
element ForceFrame  3  3  4 -section 1 -transform 1
element ForceFrame  4  4  5 -section 1 -transform 1
element ForceFrame  5  5  6 -section 1 -transform 1
element ForceFrame  6  6  7 -section 1 -transform 1
element ForceFrame  7  7  8 -section 1 -transform 1
element ForceFrame  8  8  9 -section 1 -transform 1
element ForceFrame  9  9 10 -section 1 -transform 1
element ForceFrame 10 10 11 -section 1 -transform 1

fix  1 -dof 3
fix  2 -dof 3
fix  3 -dof 3
fix  4 -dof 3
fix  5 -dof 3
fix  6 -dof 3
fix  7 -dof 3
fix  8 -dof 3
fix  9 -dof 3
fix 10 -dof 3
fix 11 -dof 3
pattern Plain 1 Linear 
nodalLoad 6 0.0 -1.0 0.0 0 0 0 -pattern 1 

system BandGeneral -det
test NormDispIncr 1e-08 8 0
algorithm Newton 
analysis Static
integrator ArcLength 45 0 -det -exp 0.5 -reference point

verify value [analyze 110] 0
verify error [nodeDisp 6 2] -1118.474348344846 1e-4

