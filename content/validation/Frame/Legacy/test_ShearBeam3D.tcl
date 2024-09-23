# 3D Cantilever column
#
set E  30000.0
set A  20.0
set Iz 1400.0
set Iy 1200.0
set G  18000.0
set J  [expr $Iz+$Iy]
set alpha [expr 5.0/6.0]

set L  100.0
set beta 0.2
set lp [expr $beta*$L]

set Py 200.0
set Pz 300.0

set nIP 3

set elements {1 2 7}

proc printRow {quantity computed bend shear} {
  puts [format "%10s %10f %10f (%10f + %10f)" $quantity $computed [expr $bend+$shear] $bend $shear];
}

foreach element $elements {
	
    model basic -ndm 3 -ndf 6
	
    node 1 0.0 0.0 0.0
    node 2  $L 0.0 0.0
    
    fix 1 1 1 1 1 1 1

    section Elastic 1 $E $A $Iz $Iy $G $J

    uniaxialMaterial Elastic 1 [expr $alpha*$G*$A]
    uniaxialMaterial Elastic 2 [expr $G*$J]
    section Aggregator 2 1 Vy 1 Vz 2 T

    section Aggregator 3 1 Vy 1 Vz 2 T -section 1

    geomTransf Linear 1 0 0 1
    
    switch $element {
	1 {
	    puts "Element: NonlinearBeamColumn"
	    element nonlinearBeamColumn 1 1 2 $nIP 3 1
	}
	2 {
	    puts "Element: BeamWithHinges"
	    element beamWithHinges 1 1 2 3 $lp 1 $lp $E $A $Iz $Iy $G $J 1
	}
	3 {
	    puts "Element: BeamWithHinges2"
	    element beamWithHinges2 1 1 2 1 $lp 1 $lp $E $A $Iz $Iy $G $J 1 -constHinge 2
	}
	7 {
	    puts "Element: ForceFrame"
	    element ForceFrame 1 1 2 $nIP 3 1
	}
    }
    
    pattern Plain 1 "Constant" {
	load 2 0.0 $Py $Pz 0.0 0.0 0.0
    }
    
    test NormUnbalance 1.0e-10 10 ; #1
    algorithm Newton
    integrator LoadControl 1.0
    constraints Plain
    system ProfileSPD
    numberer Plain
    analysis Static
    
    analyze 1
 

    set bend [expr $Py*pow($L,3)/(3*$E*$Iz)]
    set shear [expr $Py*$L/($alpha*$G*$A)]

#   puts "Exact displacement:   [expr $bend + $shear]"
#   puts "Bending contribution: $bend"
#   puts "Shear contribution:   $shear"
#   puts ""
    printRow "z-z" [nodeDisp 2 2] $bend $shear

    set bend [expr $Pz*pow($L,3)/(3*$E*$Iy)]
    set shear [expr $Pz*$L/($alpha*$G*$A)]
#   puts "Exact displacement:   [expr $bend + $shear]"
#   puts "Bending contribution: $bend"
#   puts "Shear contribution:   $shear"
#   puts ""

    printRow "y-y" [nodeDisp 2 3] $bend $shear

    wipe
}
