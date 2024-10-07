set pid [getPID]
set np [getNP]

if {$np != 2} exit

model BasicBuilder -ndm 2 -ndf 2
uniaxialMaterial Elastic 1 3000

if {$pid == 0} {
  node 1 0.0 0.0
  node 4 72.0 96.0
  fix 1 1 1
  element truss 1 1 4 10.0 1
  pattern Plain 1 "Linear" {
    load 4 100 -50
  }
} else {
  node 2 144.0 0.0
  node 3 168.0 0.0
  node 4 72.0 96.0
  fix 2 1 1
  fix 3 1 1
  element truss 2 2 4 5.0 1
  element truss 3 3 4 5.0 1
}

#create the analysis
constraints Transformation
numberer ParallelPlain 
system Mumps
test NormDispIncr 1.0e-6 6 2
algorithm Newton
integrator LoadControl 0.1
analysis Static
#perform the analysis
analyze 10
# print to screen node 4
print node 4

