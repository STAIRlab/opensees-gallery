
model basic 3 6

set E 1.0
set G 2.0

set b 2.0
set d 12.0

set A  [expr $b*$d]
set Iz [expr 1.0/12*$b*$d*$d*$d]
set Iy [expr 1.0/12*$d*$b*$b*$b]
set J  [expr $Iz+$Iy]
section Elastic 1 $E $A $Iz $Iy $G $J

invoke FrameSection 1 {puts [tangent]}

