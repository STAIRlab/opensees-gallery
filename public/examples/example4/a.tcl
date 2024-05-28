model  -ndm 2 -ndf 3
node 1 0.0 0.0 
node 2 0.0 180.0 -mass 0.1 0.1 0.0 
node 3 0.0 324.0 -mass 0.1 0.1 0.0 
node 4 288.0 0.0 
node 5 288.0 180.0 -mass 0.1 0.1 0.0 
node 6 288.0 324.0 -mass 0.1 0.1 0.0 
node 7 576.0 0.0 
node 8 576.0 180.0 -mass 0.1 0.1 0.0 
node 9 576.0 324.0 -mass 0.1 0.1 0.0 
node 10 864.0 0.0 
node 11 864.0 180.0 -mass 0.1 0.1 0.0 
node 12 864.0 324.0 -mass 0.1 0.1 0.0 
fix 1 1 1 1 
fix 4 1 1 1 
fix 7 1 1 1 
fix 10 1 1 1 
uniaxialMaterial Concrete01 1 -6.0 -0.004 -5.0 -0.014 
uniaxialMaterial Concrete01 2 -5.0 -0.002 -0.0 -0.006 
uniaxialMaterial Steel01 3 60.0 30000.0 0.015 
section Fiber 1 
patch quad 2 1 12 -11.5 10.0 -11.5 -10.0 11.5 -10.0 11.5 10.0 -section 1 -section 1
patch quad 1 1 14 -13.5 -10.0 -13.5 -12.0 13.5 -12.0 13.5 -10.0 -section 1 -section 1
patch quad 1 1 14 -13.5 12.0 -13.5 10.0 13.5 10.0 13.5 12.0 -section 1 -section 1
patch quad 1 1 2 -13.5 10.0 -13.5 -10.0 -11.5 -10.0 -11.5 10.0 -section 1 -section 1
patch quad 1 1 2 11.5 10.0 11.5 -10.0 13.5 -10.0 13.5 10.0 -section 1 -section 1
layer straight 3 6 1.56 -10.5 9.0 -10.5 -9.0 -section 1 -section 1
layer straight 3 6 1.56 10.5 9.0 10.5 -9.0 -section 1 -section 1
beamIntegration Lobatto 1 1 4 
section Fiber 2 
patch quad 2 1 10 -10.0 10.0 -10.0 -10.0 10.0 -10.0 10.0 10.0 -section 2 -section 2
patch quad 1 1 12 -12.0 -10.0 -12.0 -12.0 12.0 -12.0 12.0 -10.0 -section 2 -section 2
patch quad 1 1 12 -12.0 12.0 -12.0 10.0 12.0 10.0 12.0 12.0 -section 2 -section 2
patch quad 1 1 2 -12.0 10.0 -12.0 -10.0 -10.0 -10.0 -10.0 10.0 -section 2 -section 2
patch quad 1 1 2 10.0 10.0 10.0 -10.0 12.0 -10.0 12.0 10.0 -section 2 -section 2
layer straight 3 6 0.79 -9.0 9.0 -9.0 -9.0 -section 2 -section 2
layer straight 3 6 0.79 9.0 9.0 9.0 -9.0 -section 2 -section 2
beamIntegration Lobatto 2 2 4 
section Fiber 3 
patch quad 1 1 12 -12.0 9.0 -12.0 -9.0 12.0 -9.0 12.0 9.0 -section 3 -section 3
layer straight 3 4 1.0 -9.0 9.0 -9.0 -9.0 -section 3 -section 3
layer straight 3 4 1.0 9.0 9.0 9.0 -9.0 -section 3 -section 3
beamIntegration Lobatto 3 3 4 
geomTransf Linear 1 
element ForceBeamColumn 1 1 2 1 2 
element ForceBeamColumn 2 2 3 1 2 
element ForceBeamColumn 3 4 5 1 1 
element ForceBeamColumn 4 5 6 1 1 
element ForceBeamColumn 5 7 8 1 1 
element ForceBeamColumn 6 8 9 1 1 
element ForceBeamColumn 7 10 11 1 2 
element ForceBeamColumn 8 11 12 1 2 
geomTransf Linear 2 
element ForceBeamColumn 9 2 5 2 3 
element ForceBeamColumn 10 5 8 2 3 
element ForceBeamColumn 11 8 11 2 3 
element ForceBeamColumn 12 3 6 2 3 
element ForceBeamColumn 13 6 9 2 3 
element ForceBeamColumn 14 9 12 2 3 
timeSeries Linear 1 
pattern Plain 1 1 -fact 1.0 
nodalLoad 2 0.0 -192.0 0.0 -pattern 1 
nodalLoad 3 0.0 -96.0 0.0 -pattern 1 
nodalLoad 5 0.0 -384.0 0.0 -pattern 1 
nodalLoad 6 0.0 -192.0 0.0 -pattern 1 
nodalLoad 8 0.0 -384.0 0.0 -pattern 1 
nodalLoad 9 0.0 -192.0 0.0 -pattern 1 
nodalLoad 11 0.0 -192.0 0.0 -pattern 1 
nodalLoad 12 0.0 -96.0 0.0 -pattern 1 
print -JSON -file Example4.1.json 
system BandGeneral 
numberer RCM 
constraints Plain 
test NormDispIncr 1e-08 10 0 
algorithm Newton 
integrator LoadControl 0.1 
analysis Static 
initialize  
analyze 10 
loadConst -time 0.0 
pattern Plain 2 1 -fact 1.0 
nodalLoad 2 5.0 0.0 0.0 -pattern 2 
nodalLoad 3 10.0 0.0 0.0 -pattern 2 
recorder Node disp -node 2 3 -dof 1 -file Node41.out -time
eigen 2 
integrator LoadControl 1.0 4 0.02 2.0 
record  
analyze 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
test NormDispIncr 1e-08 4000 0 
algorithm ModifiedNewton -initial 
analyze 1 
test NormDispIncr 1e-08 10 0 
algorithm Newton 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
test NormDispIncr 1e-08 4000 0 
algorithm ModifiedNewton -initial 
analyze 1 
test NormDispIncr 1e-08 10 0 
algorithm Newton 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
test NormDispIncr 1e-08 4000 0 
algorithm ModifiedNewton -initial 
analyze 1 
test NormDispIncr 1e-08 10 0 
algorithm Newton 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
test NormDispIncr 1e-08 4000 0 
algorithm ModifiedNewton -initial 
analyze 1 
test NormDispIncr 1e-08 10 0 
algorithm Newton 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
analyze 1 
nodeDisp 3 1 
test NormDispIncr 1e-08 4000 0 
algorithm ModifiedNewton -initial 
analyze 1 
test NormDispIncr 1e-08 10 0 
algorithm Newton 
analyze 1 
nodeDisp 3 1 
print node 3 
wipe  
