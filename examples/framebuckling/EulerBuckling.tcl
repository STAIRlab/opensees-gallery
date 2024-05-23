
set E 29000.0
set I 110.0
set A 9.12e3
set L 60.0

set NumberOfElements 10
set ElementType forceBeamColumn
set GeomTransfType Corotational

set LoadStep 0.01
set PeakLoadRatio 2.00



# END OF INPUT

set NumIntegrationPoints 3
set NumberOfNodes [expr $NumberOfElements+1]
set pi [expr acos(-1)]
set EulerLoad [expr $pi*$pi*$E*$I/($L*$L)]

model basic -ndm 2 -ndf 3

# Define Nodes
for { set i 1 } { $i <= $NumberOfNodes } { incr i } {
  set y [expr ($i-1)/double($NumberOfElements)*$L]
  node $i 0.0 $y
  mass $i 1.0 1.0 1.0
}

# Define Boundary Conditions
fix              1 1 1 0
fix $NumberOfNodes 1 0 0

# Define Section 
set SectionTag 1
section Elastic $SectionTag $E $A $I

# Define Geometric Transformation
set GeomTransfTag 1
geomTransf $GeomTransfType $GeomTransfTag

# Define Elements
for { set i 1 } { $i <= $NumberOfElements } { incr i } {
  element $ElementType $i $i [expr $i+1] $NumIntegrationPoints $SectionTag $GeomTransfTag
}

# Apply loads
pattern Plain 1 Linear {
  load $NumberOfNodes 0.0 -$EulerLoad 0.0
}

# Analysis Options
system UmfPack
constraints Transformation
test NormUnbalance 1.0e-6 20 0
algorithm Newton 
numberer Plain
integrator LoadControl $LoadStep
analysis Static

set LastLoadRatio  [getTime]
set LastEigenvalue [eigen 1]

for { set i 1 } { $i <= [expr int($PeakLoadRatio/$LoadStep)] } { incr i } {
    analyze 1
    set CurrentLoadRatio   [getTime]
    set CurrentEigenvalue  [eigen 1]
    
    if { $CurrentEigenvalue <= 0.0 } {
        puts "Analysis Finished"
        
        set InterpolatedLoadRatio [expr $LastLoadRatio+($CurrentLoadRatio-$LastLoadRatio)*$LastEigenvalue/($LastEigenvalue-$CurrentEigenvalue)]
        
        puts "Limit Point Found"
        puts "Number Of Elements:               $NumberOfElements"
        puts "Element Type:                     $ElementType"
        puts "Geometric Transformation Type:    $GeomTransfType"
        puts "Exact Euler Load:                 [format "%.2f" $EulerLoad]"
        puts "Computed Euler Load:              [format "%.2f" [expr $InterpolatedLoadRatio*$EulerLoad]]"
        puts "Percent Error:                    [format "%.2f%%" [expr 100*($InterpolatedLoadRatio-1)]]"
        exit
    }
    
    set LastLoadRatio  $CurrentLoadRatio
    set LastEigenvalue $CurrentEigenvalue
}


puts "Analysis Finished"
puts "No Limit Point Found"
