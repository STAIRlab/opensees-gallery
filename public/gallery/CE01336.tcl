


#============================================================
# Initializations
#============================================================
# Parameters


# Create ModelBuilder (with 3 dimensions and 6 DOF/node)
model BasicBuilder -ndm 3 -ndf 6
lassign {1 2 3 4 5 6} dx dy dz rx ry rz
#============================================================
# Materials
#============================================================

geomTransf Linear  1   0  0  1 
geomTransf Linear  2   0  0  1 -jntOffset   0.0  0.0  0.0   0.0  -40.45295044121206  0.0 

#============================================================
# Assemblage
#============================================================

node  1   0.0  244.4529504412121  0.0 -mass  0.0  0.0  0.0  0.0  0.0  0.0
node  2   2496.0000000000005  244.4529504412121  0.0 -mass  0.0  0.0  0.0  0.0  0.0  0.0
node  3   1248.0000000000002  244.4529504412121  0.0 -mass  0.0  0.0  0.0  0.0  0.0  0.0
node  4   1248.0000000000002  0.0  0.0 -mass  0.0  0.0  0.0  0.0  0.0  0.0


element elasticBeamColumn  1   1  3  6602.708333333339  4074280.688047892  1697616.9533532884  20000000.0  79592596.30902787  4583234.085550575  1 -mass 1.4350248390398423 -cMass

element elasticBeamColumn  2   4  3  2827.4333882308147  4074280.688047892  1697616.9533532884  20000000.0  636172.5123519334  636172.5123519334  2 -mass 0.6145110366844612 -cMass

element elasticBeamColumn  3   3  2  6602.708333333339  4074280.688047892  1697616.9533532884  20000000.0  79592596.30902787  4583234.085550575  1 -mass 1.4350248390398423 -cMass

#============================================================
# Constraints
#============================================================

fix 1 1 1 1 1 1 1
fix 2 1 1 1 1 1 1
fix 4 1 1 1 1 1 1


print -json
# source Library/ResponseHistoryLib.tcl
# rayleigh {*}[rayleigh_alpha {1 0.05} {2 0.05}]
# 
# 
# ResponseHistory create rh
# rh patterns {
#     UniformQuake 3 /home/claudio/brace/CSMIP/meloland/Calexico_30Dec2009_CE01336P.zip 2 -s 0.393701
# }
# recorder Node -file a.txt -time -node 3 -dof 3 disp
# 
# 
# rh analyze 

#exec sleep 10

# write_displ

