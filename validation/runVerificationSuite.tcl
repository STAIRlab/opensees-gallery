# script to run all the verification scripts
# PASS/FAILURE results in file README.md when run
#
proc range args {
  foreach {start stop step} [switch -exact -- [llength $args] {
      1 {concat 0 $args 1}
      2 {concat   $args 1}
      3 {concat   $args  }
      default {error {wrong # of args: should be "range ?start? stop ?step?"}}
  }] break
  if {$step == 0} {error "cannot create a range when step == 0"}
  set range [list]
  while {$step > 0 ? $start < $stop : $stop < $start} {
      lappend range $start
      incr start $step
  }
  return $range
}

# open results file such that it is cleared out of any data
set results [open README.md w]
puts $results "| Status | Notes |\n|--------|------------------------------|"
close $results

cd Basic
  source test_sdof.tcl
  source test_eigen.tcl
  source test_newmark.tcl
  source test_mdof.tcl
cd ..
  
source Truss/PlanarTruss.tcl
source Truss/PlanarTruss.Extra.tcl

source Frame/PortalFrame2d.tcl
source Frame/test_EigenFrame.tcl
source Frame/EigenFrame.Extra.tcl
source Frame/AISC25.tcl

source Plane/PlaneStrain.tcl
source Plane/QuadBending.tcl

# Shells
source Shell/PinchedCylinder.tcl
source Shell/PlanarShearWall.tcl

