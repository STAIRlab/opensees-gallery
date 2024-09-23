wipe
model basic -ndm 3 -ndf 6
reliability
timeSeries Linear
timeSeries Linear 1
timeSeries Constant 2
# Materials
uniaxialMaterial Concrete01 1 -29.89 -0.002 -0.3 -0.006
uniaxialMaterial Steel01 2 381.98 216722.0 0.0023
uniaxialMaterial Steel01 3 310.8 216722.0 0.002256

set As [expr 28 * 28 * 3.14159 / 4]
# Section
section Fiber 1 -GJ 1e14 {
  patch rect     1 5 1200 -200 -600 200 600
  layer straight 3 8 $As -160 -560 160 -560
  layer straight 3 3 $As -160 560 160 560
}

# Create nodes
node 1     0 0 0
node 2  7675 0 0
node 3  5675 0 0
node 4  3675 0 0
node 5 11350 0 0
# Boundary conditions
fix 1 0 1 1 1 0 1
fix 5 1 1 1 1 0 1

# Create elements
geomTransf Linear 1 0.0 0.0 1.0
element forceBeamColumn 1 1 2 1 Lobatto 1 5
element forceBeamColumn 2 2 3 1 Lobatto 1 5
element forceBeamColumn 3 3 4 1 Lobatto 1 5
element forceBeamColumn 4 4 5 1 Lobatto 1 5

# Parameters
parameter 1
parameter 2
parameter 3

foreach ele [getEleTags] {
  addToParameter 1 element $ele E
  addToParameter 2 element $ele fy
  addToParameter 3 element $ele fc
}

# Self weight
#pattern Plain 1 1 {
# eleLoad -ele 1 2 3 4 -type -beamUniform 0.0 -12.0
#}
#test NormDispIncr 1e-12 100 2
#integrator LoadControl 0.1
#analysis Static
#analyze 10
#loadConst -time 0.0

print node 3
foreach p [getParamTags] {
  set fileid fid_$p
  set $fileid [open "sensLambda_$p.out" "w+"]
}

recorder Node -file nodeDisp3.out -time -node 3 -dof 3 "disp"

# 4 point bending
pattern Plain 2 1 {
  load 2 0.0 0.0 -500.0 0.0 0.0 0.0
  load 4 0.0 0.0 -500.0 0.0 0.0 0.0
}
integrator DisplacementControl 3 3 -1.0
analysis Static
sensitivityAlgorithm -computeAtEachStep
analyze 1

# Save sensitivity
foreach p [getParamTags] {
  puts "[nodeDisp 3 3] [sensLambda 2 $p]"
  puts "[expr $fid_$p]" "[nodeDisp 3 3] [sensLambda 2 $p]"
}

# print some checks
print node 3
foreach p [getParamTags] {
  set val [getParamValue $p]
  puts “Parameter $p: $val”
  close [expr $fid_$p]
}

