# AISC Benchmark Problem, Case 2
# AISC 360-16, Commentary Figure C-C2.3
#
# Cantilever column with a 1-kip lateral point load at the end and a varying axial load
#
# Units: kip, in, sec

set use_shear 1

if { $use_shear } {
    set Mbench_list [list 336.0 470.0 601.0 856.0]
    set Dbench_list [list 0.907 1.34  1.77  2.60 ]

} else {
    set Mbench_list [list 336.0 469.0 598.0 848.0]
    set Dbench_list [list 0.901 1.33  1.75  2.56 ]
}


# Cross-section
set A  14.1
set I  484.0
set d  13.8
set tw 0.340

# Material
set E  29000.0
set G  11200.0

# Shear coefficient from Iyer 2005: A/Av
set k  [expr ($d*$tw)/$A]


model BasicBuilder -ndm 2 -ndf 3

# Nodes
node 1 0.0   0.0
node 2 0.0  84.0
node 3 0.0 168.0
node 4 0.0 252.0
node 5 0.0 336.0

fix 1 1 1 1

# Sections
if { $use_shear } {
    section Elastic 1 $E $A $I $G $k
} else {
    section Elastic 1 $E $A $I
}
geomTransf Corotational 1

# Elements
element forceBeamColumn 1 1 2 3 1 1
element forceBeamColumn 2 2 3 3 1 1
element forceBeamColumn 3 3 4 3 1 1
element forceBeamColumn 4 4 5 3 1 1

pattern Plain 1 Linear {
    load 5 1 0 0
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

set Mbase [lindex [eleResponse 1 forces] 2]
set Dtip [nodeDisp 5 1]
set Mbench [lindex $Mbench_list 0]
set Dbench [lindex $Dbench_list 0]
puts [format "Axial Force, P = %.0f kips" [getTime]]
puts [format "Base moment, Mbase = %.0f kip-in" $Mbase]
puts [format "   compared to %.0f kip-in, a %.2f%% difference" $Mbench [expr 100*($Mbench-$Mbase)/$Mbench]]
puts [format "Tip displacement, Dtip = %.4f in" $Dtip]
puts [format "   compared to %.3f in, a %.2f%% difference\n" $Dbench [expr 100*($Dbench-$Dtip)/$Dbench]]


pattern Plain 2 Linear {
    load 5 0 -1 0
}

integrator LoadControl 10.0
analyze 10

set Mbase [lindex [eleResponse 1 forces] 2]
set Dtip [nodeDisp 5 1]
set Mbench [lindex $Mbench_list 1]
set Dbench [lindex $Dbench_list 1]
puts [format "Axial Force, P = %.0f kips" [getTime]]
puts [format "Base moment, Mbase = %.0f kip-in" $Mbase]
puts [format "   compared to %.0f kip-in, a %.2f%% difference" $Mbench [expr 100*($Mbench-$Mbase)/$Mbench]]
puts [format "Tip displacement, Dtip = %.3f in" $Dtip]
puts [format "   compared to %.2f in, a %.2f%% difference\n" $Dbench [expr 100*($Dbench-$Dtip)/$Dbench]]

analyze 5

set Mbase [lindex [eleResponse 1 forces] 2]
set Dtip [nodeDisp 5 1]
set Mbench [lindex $Mbench_list 2]
set Dbench [lindex $Dbench_list 2]
puts [format "Axial Force, P = %.0f kips" [getTime]]
puts [format "Base moment, Mbase = %.0f kip-in" $Mbase]
puts [format "   compared to %.0f kip-in, a %.2f%% difference" $Mbench [expr 100*($Mbench-$Mbase)/$Mbench]]
puts [format "Tip displacement, Dtip = %.3f in" $Dtip]
puts [format "   compared to %.2f in, a %.2f%% difference\n" $Dbench [expr 100*($Dbench-$Dtip)/$Dbench]]

analyze 5

set Mbase [lindex [eleResponse 1 forces] 2]
set Dtip [nodeDisp 5 1]
set Mbench [lindex $Mbench_list 3]
set Dbench [lindex $Dbench_list 3]
puts [format "Axial Force, P = %.0f kips" [getTime]]
puts [format "Base moment, Mbase = %.0f kip-in" $Mbase]
puts [format "   compared to %.0f kip-in, a %.2f%% difference" $Mbench [expr 100*($Mbench-$Mbase)/$Mbench]]
puts [format "Tip displacement, Dtip = %.3f in" $Dtip]
puts [format "   compared to %.2f in, a %.2f%% difference\n" $Dbench [expr 100*($Dbench-$Dtip)/$Dbench]]

