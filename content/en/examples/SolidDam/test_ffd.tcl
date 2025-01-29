set jj 1
foreach i {0.1 0.01 0.001 0.0001 0.00001} {
set filename dispG$jj
set jj [expr $jj+1]
set perturb [expr $i+1]

wipe




# model dam
#
source model_sgk_df_damp_ffd.tcl

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
test NormDispIncr 1.0E-8 10 2
algorithm Newton
integrator Newmark 0.5 0.25

analysis Transient



analyze 1000 0.01

puts "Dynamic analysi done..."

set endT [clock seconds]
puts "Execution time: [expr $endT-$startT] seconds."

}
