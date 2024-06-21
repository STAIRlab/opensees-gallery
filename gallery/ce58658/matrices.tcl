proc reset {} {
  wipeAnalysis 
  numberer RCM
  algorithm Linear
  constraints Transformation
  system "FullGeneral"
  # analysis "Transient"
}

# Stiffness
reset
integrator "GimmeMCK" 0.0 0.0 1.0
analysis "Static"
analyze 1 1.0
printA "-file" "K.out"
 
# Mass
reset
integrator "GimmeMCK" 1.0 0.0 0.0
analysis "Transient"
analyze 1 1.0  
printA "-file" "M.out"
 
 
# # Damping
# reset
# integrator "GimmeMCK" 0.0 1.0 0.0
# analysis "Transient"
# analyze 1 1.0
# printA "-file" "C.out"
