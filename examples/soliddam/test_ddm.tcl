


#
# model dam
#
source model_sgk_df_damp_ddm.tcl

#
# model reservoir
#



#
# Define analysis
#

set startT [clock seconds]

wipeAnalysis
constraints Plain
system BandGeneral
numberer RCM
test NormDispIncr 1.0E-5 10 0
algorithm Newton
integrator Newmark 0.5 0.25

analysis Transient
sensitivityAlgorithm -computeAtEachStep


analyze 1000 0.01

puts "Dynamic analysi done..."

set endT [clock seconds]
puts "Execution time: [expr $endT-$startT] seconds."


