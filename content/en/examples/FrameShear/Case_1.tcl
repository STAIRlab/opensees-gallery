# AISC Benchmark Problem, Case 1
# AISC 360-16, Commentary Figure C-C2.2
#
# Pinned-pinned column with uniform lateral load of 0.200 kip/ft and varying axial load
#
# Units: kip, in, sec

set use_shear 1

if { $use_shear } {
    set Mbench_list [list 235.0 270.0 316.0 380.0]
    set Dbench_list [list 0.202 0.230 0.269 0.322]

} else {
    set Mbench_list [list 235.0 269.0 313.0 375.0]
    set Dbench_list [list 0.197 0.224 0.261 0.311]
}


# Cross-section geometry
set A  14.1
set I  484.0
set d  13.8
set tw 0.340

# Material settings
set E  29000.0
set G  11200.0

# Shear coefficient from Iyer 2005: A/Av
set k  [expr ($d*$tw)/$A]


model BasicBuilder -ndm 2 -ndf 3

# Nodes
node 1 0.0   0.0
node 2 0.0  42.0
node 3 0.0  84.0
node 4 0.0 126.0
node 5 0.0 168.0
node 6 0.0 210.0
node 7 0.0 252.0
node 8 0.0 294.0 
node 9 0.0 336.0

fix 1 1 1 0
fix 9 1 0 0

# Sections
if { $use_shear } {
    section Elastic 1 $E $A $I $G $k
} else {
    section Elastic 1 $E $A $I
}
geomTransf Corotational 1

# Elements
element ForceBeamColumn 1 1 2 3 1 1
element ForceBeamColumn 2 2 3 3 1 1
element ForceBeamColumn 3 3 4 3 1 1
element ForceBeamColumn 4 4 5 3 1 1
element ForceBeamColumn 5 5 6 3 1 1
element ForceBeamColumn 6 6 7 3 1 1
element ForceBeamColumn 7 7 8 3 1 1
element ForceBeamColumn 8 8 9 3 1 1

timeSeries Linear 1
pattern Plain 1 1 {
    eleLoad -ele 1 -type -beamUniform [expr -0.200/12]
    eleLoad -ele 2 -type -beamUniform [expr -0.200/12]
    eleLoad -ele 3 -type -beamUniform [expr -0.200/12]
    eleLoad -ele 4 -type -beamUniform [expr -0.200/12]
    eleLoad -ele 5 -type -beamUniform [expr -0.200/12]
    eleLoad -ele 6 -type -beamUniform [expr -0.200/12]
    eleLoad -ele 7 -type -beamUniform [expr -0.200/12]
    eleLoad -ele 8 -type -beamUniform [expr -0.200/12]
}

constraints Transformation
numberer Plain
system UmfPack
test NormDispIncr 1.0e-6 30 0
algorithm Newton
integrator LoadControl 0.1
analysis Static
analyze 10

loadConst -time 0.0

set Mmid [lindex [eleResponse 4 forces] 5]
set Dmid [nodeDisp 5 1]
set Mbench [lindex $Mbench_list 0]
set Dbench [lindex $Dbench_list 0]
puts [format "Axial Force, P = %.0f kips" [getTime]]
puts [format "Mid-height moment, Mmid = %.1f kip-in" $Mmid]
puts [format "   compared to %.0f kip-in | %.2f%% " $Mbench [expr 100*($Mbench-$Mmid)/$Mbench]]
puts [format "Mid-height displacement, Dmid = %.4f in" $Dmid]
puts [format "   compared to %.3f in, a %.2f%% \n" $Dbench [expr 100*($Dbench-$Dmid)/$Dbench]]

timeSeries Linear 2
pattern Plain 2 2 {
    load 9 0 -1 0
}

integrator LoadControl 15.0
analyze 10

set Mmid [lindex [eleResponse 4 forces] 5]
set Dmid [nodeDisp 5 1]
set Mbench [lindex $Mbench_list 1]
set Dbench [lindex $Dbench_list 1]
puts [format "Axial Force, P = %.0f kips" [getTime]]
puts [format "Mid-height moment, Mmid = %.1f kip-in" $Mmid]
puts [format "   compared to %.0f kip-in, a %.2f%% difference" $Mbench [expr 100*($Mbench-$Mmid)/$Mbench]]
puts [format "Mid-height displacement, Dmid = %.4f in" $Dmid]
puts [format "   compared to %.3f in, a %.2f%% difference\n" $Dbench [expr 100*($Dbench-$Dmid)/$Dbench]]

analyze 10

set Mmid [lindex [eleResponse 4 forces] 5]
set Dmid [nodeDisp 5 1]
set Mbench [lindex $Mbench_list 2]
set Dbench [lindex $Dbench_list 2]
puts [format "Axial Force, P = %.0f kips" [getTime]]
puts [format "Mid-height moment, Mmid = %.1f kip-in" $Mmid]
puts [format "   compared to %.0f kip-in, a %.2f%% difference" $Mbench [expr 100*($Mbench-$Mmid)/$Mbench]]
puts [format "Mid-height displacement, Dmid = %.4f in" $Dmid]
puts [format "   compared to %.3f in, a %.2f%% difference\n" $Dbench [expr 100*($Dbench-$Dmid)/$Dbench]]

analyze 10

set Mmid [lindex [eleResponse 4 forces] 5]
set Dmid [nodeDisp 5 1]
set Mbench [lindex $Mbench_list 3]
set Dbench [lindex $Dbench_list 3]
puts [format "Axial Force, P = %.0f kips" [getTime]]
puts [format "Mid-height moment, Mmid = %.1f kip-in" $Mmid]
puts [format "   compared to %.0f kip-in, a %.2f%% difference" $Mbench [expr 100*($Mbench-$Mmid)/$Mbench]]
puts [format "Mid-height displacement, Dmid = %.4f in" $Dmid]
puts [format "   compared to %.3f in, a %.2f%% difference\n" $Dbench [expr 100*($Dbench-$Dmid)/$Dbench]]

