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
set results [open STATUS.md w]
puts $results "| Status | Notes |\n|--------|------------------------------|"
close $results

if 1 {
cd content/validation/Basic
  source test_sdof.tcl
  source test_eigen.tcl
  source test_newmark.tcl
  source test_mdof.tcl
cd ../../..

source content/validation/Truss/PlanarTruss.tcl
source content/validation/Truss/PlanarTruss.Extra.tcl
}
  
cd content/validation/Frame
  source test.tcl
cd ../../../

source content/validation/Plane/PlaneStrain.tcl
source content/validation/Plane/QuadBending.tcl

# Shells
source content/validation/Shell/PinchedCylinder.tcl
source content/validation/Shell/PlanarShearWall.tcl

