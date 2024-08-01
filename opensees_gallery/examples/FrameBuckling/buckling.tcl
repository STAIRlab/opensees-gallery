#
#
#
proc euler_buckling {
    { ElementType forceBeamColumn }
    { GeomTransfType Corotational }
    { elem_count 10 } } {


  set E 29000.0
  set I 110.0
  set A 9.12e3
  set L 60.0

  set load_step 0.01
  set PeakLoadRatio 2.00


  set NumIntegrationPoints 3

  # Constants
  set node_count [expr $elem_count+1]
  set pi [expr acos(-1)]
  set euler_load [expr $pi*$pi*$E*$I/($L*$L)]

  model basic -ndm 2 -ndf 3

  # Define Nodes
  for { set i 1 } { $i <= $node_count } { incr i } {
    set y [expr ($i-1)/double($elem_count)*$L]
    node $i 0.0 $y
    mass $i 1.0 1.0 1.0
  }

  # Define boundary conditions
  fix           1 1 1 0
  fix $node_count 1 0 0

  # Define section 
  set sec_tag 1
  section Elastic $sec_tag $E $A $I

  # Define geometric transformation
  set GeomTransfTag 1
  geomTransf $GeomTransfType $GeomTransfTag

  # Define Elements
  for { set i 1 } { $i <= $elem_count } { incr i } {
    element $ElementType $i $i [expr $i+1] $NumIntegrationPoints $sec_tag $GeomTransfTag
  }

  # Define loads
  pattern Plain 1 Linear {
    load $node_count 0.0 -$euler_load 0.0
  }

  #
  # Analysis
  #
  # Configure solver
  system UmfPack
  constraints Transformation
  test NormUnbalance 1.0e-6 20 0
  algorithm Newton 
  numberer Plain
  integrator LoadControl $load_step
  analysis Static

  # Initialize
  set lam_0 [getTime]
  set eig_0 [eigen 1]

  for { set i 1 } { $i <= [expr int($PeakLoadRatio/$load_step)] } { incr i } {
      analyze 1
      set lam   [getTime]
      set eig  [eigen 1]
      
      if { $eig <= 0.0 } {
          
          set lam_i [expr $lam_0+($lam-$lam_0)*$eig_0/($eig_0-$eig)]
          
          puts "Limit Point Found"
          puts "Number Of Elements:               $elem_count"
          puts "Element Type:                     $ElementType"
          puts "Geometric Transformation Type:    $GeomTransfType"
          puts "Exact Euler Load:                 [format "%.2f" $euler_load]"
          puts "Computed Euler Load:              [format "%.2f" [expr $lam_i*$euler_load]]"
          puts "Percent Error:                    [format "%.2f%%" [expr 100*($lam_i-1)]]"
          return [expr $lam_i*$euler_load]
      }
      
      set lam_0 $lam
      set eig_0 $eig
  }
}

euler_buckling

