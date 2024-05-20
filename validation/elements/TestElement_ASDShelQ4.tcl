# set up a 3D-6DOFs model
model Basic -ndm 3 -ndf 6

node 1  0.0  0.0 0.0 -mass 0 0 0 1 1 1
node 2  1.0  0.0 0.0
node 3  1.0  1.0 0.0 -mass 0 0 0 1 1 1
node 4  0.0  1.0 0.0

fix  1  1 1 1 1 1 1
fix  2  1 1 1 0 0 0
fix  3  1 1 1 0 0 0
fix  4  1 1 1 0 0 0

# create a fiber shell section with 4 layers of material 1
# each layer has a thickness = 0.025
nDMaterial ElasticIsotropic  1  1000.0  0.2
section    LayeredShell  11  4   1 0.025   1 0.025   1 0.025   1 0.025

# create the shell element using the small displacements/rotations assumption
#element ASDShellQ4  1  1 2 3 4  11
# or you can use the corotational flag for large displacements/rotations (geometric nonlinearity)
element ASDShellQ4  1  1 2 3 4  11 -corotational

# record global forces at element nodes (24 columns, 6 for each node)
recorder Element  -xml  out/force_out.xml  -ele  1  force
# record local section forces at gauss point 1 (8 columns: | 3 membrane | 3 bending | 2 transverse shear |)
# note: gauss point index is 1-based
recorder Element  -xml  out/force_gp1_out.xml  -ele  1  material  1  force
# record local stresses at fiber 1 of gauss point 1 (5 columns: Szz is neglected (0) )
# note: fiber index is 1-based (while in beams it is 0-based!)
recorder Element  -xml  out/stress_gp1_fib0_out.xml  -ele  1  material  1  fiber 1 stress

eigen 1

wipe
