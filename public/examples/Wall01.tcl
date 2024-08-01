wipe;
model basic -ndm 2 -ndf 3

set tolAx 1.0e-3
set iterAx 100;

set tolLatNew 1.0e-6
set iterLatNew 100;

set tolLatIni 1.0e-5
set iterLatIni 1000;

set dUi 0.02; # Displacement increment

set maxU 1.6; # Max. Displacement

# concrete parameters
set fc -6.21; 
set eo -0.0021; 
set r 2.91;

set k 1.36
set alphaC 0.32
set fcr 0.294;

set ecr 0.00008
set b 0.4
set alphaT 0.08;

set fcc -6.91
set ecc -0.0038
set rcc 1.88;

# steel parameters
set fyRed 59.15
set by 0.02
set Ry 1.564;

set roy 0.00327
set fyBRed 57.33
set byB 0.02;

set RyB 25.0
set royB 0.0293
set fxRed 59.15;

set bx 0.02
set Rx 1.564
set rox 0.00327;

# concrete (confined and unconfined)
uniaxialMaterial Concrete06 1 $fcc $ecc $rcc 1 $alphaC $fcr $ecr $b $alphaT;
uniaxialMaterial Concrete06 2 $fc $eo $r $k $alphaC $fcr $ecr $b $alphaT;

# steel (bound., web and horiz. reinforcement)

set E 29000.0;

uniaxialMaterial Steel02 1003 $fyBRed $E $byB $RyB 0.9 0.1 0 0.1 0 0.1 ;
uniaxialMaterial Steel02 1004 $fyRed $E $by $Ry 0.9 0.1 0 0.1 0 0.1 ;
uniaxialMaterial Steel02 1005 $fxRed $E $bx $Rx 0.9 0.1 0 0.1 0 0.1 ;

# Define cross-section

set t1 6.0
set NStrip1 2; # thickness 1

set t2 4.0
set NStrip2 4; # thickness 2

set t3 6.0
set NStrip3 2; # thickness 3

geomTransf LinearInt 1

set np 1; # int. points

set C 0.4; # center of rotation

#section definition

section FiberInt 2 -NStrip $NStrip1 $t1 $NStrip2 $t2 $NStrip3 $t3 {

#vertical fibers
    fiber -23 1 10 1; fiber -23 1 5 2; fiber -23 1 0.3 1003;
    fiber -19 1 10 1; fiber -19 1 5 2; fiber -19 1 0.3 1003;

    fiber -14 1 33 2; fiber -14 1 0.1 1004;
    fiber  -6 1 33 2; fiber  -6 1 0.1 1004;
    fiber   6 1 33 2; fiber   6 1 0.1 1004;
    fiber  14 1 33 2; fiber  14 1 0.1 1004;

    fiber 19 1 10 1; fiber 19 1 5 2; fiber 19 1 0.3 1003;
    fiber 23 1 10 1; fiber 23 1 5 2; fiber 23 1 0.3 1003;

#horiz. reinf.

    Hfiber 0 0 0.2 1005;

}

#nodes

set n 8

node 1 0 0.0; node 2 0 160; node 3 0 20; node 4 0 40;

node 5 0 60; node 6 0 80; node 7 0 100; node 8 0 120; node 9 0 140;

#element definitions
element dispBeamColumnInt 1 1 3 $np 2 1 $C
element dispBeamColumnInt 2 3 4 $np 2 1 $C
element dispBeamColumnInt 3 4 5 $np 2 1 $C
element dispBeamColumnInt 4 5 6 $np 2 1 $C
element dispBeamColumnInt 5 6 7 $np 2 1 $C
element dispBeamColumnInt 6 7 8 $np 2 1 $C
element dispBeamColumnInt 7 8 9 $np 2 1 $C
element dispBeamColumnInt 8 9 2 $np 2 1 $C

fix 1 1 1 1

# Set axial load
pattern Plain 1 Constant {
  load 2 0.0 -85 0.0
}

initialize; integrator LoadControl 0 1 0 0;

system SparseGeneral -piv; test NormUnbalance $tolAx $iterAx 0;

numberer Plain; constraints Plain;

algorithm ModifiedNewton -initial;
analysis Static;

# perform the gravity load analysis,

analyze [expr 1]

# Set the gravity loads to be constant & reset the time in the domain

loadConst -time 0.0

remove recorders

# set lateral load
pattern Plain 2 Linear {
    load 2 1.0 0.0 0;
}

system BandGeneral; constraints Transformation; numberer Plain;

# Create a recorder to monitor nodal displacement and element forces

recorder Node -file nodeTop.out -node 2 -dof 1 disp

recorder Element -file elesX.out -time -ele 1 globalForce

# recorder for element1 section1 steel stress/strain and section force-def.

recorder Element -file Sect_FandD.out -ele 1 section 1 forceAndDeformation
recorder Element -file Sect_eX.out -ele 1 section 1 eX
recorder Element -file Sect_eY.out -ele 1 section 1 eY
recorder Element -file Sect_sX.out -ele 1 section 1 sX
recorder Element -file Sect_sY.out -ele 1 section 1 sY

test NormDispIncr $tolLatNew $iterLatNew;

algorithm ModifiedNewton -initial

analysis Static

set dU $dUi;

set numSteps [expr int($maxU/$dU)];

integrator DisplacementControl 2 1 $dU 1 $dU $dU

#source cycle2.tcl

#### end

set ok [analyze $numSteps]
set jump 1;

if {$ok != 0} {

    set currentDisp [nodeDisp 2 1]

    set ok 0

    while {abs($currentDisp) < abs($maxU)} {
      set ok [analyze 1]

      puts "\n Trying.. $currentDisp\n"

# if the analysis fails try initial tangent iteration

      if {$ok != 0} {
        puts "\n regular newton failed .. try an initial stiffness"

        test NormDispIncr $tolLatIni $iterLatIni 0;

        algorithm ModifiedNewton -initial ;

        set ok [analyze 1]

        puts "\n Trying.. $currentDisp\n"

        if {$ok == 0} {
          puts " that worked .. back to regular newton \n"
          set jump 1
          integrator DisplacementControl 2 1 $dU 1

        } else {
          puts "\n that didn't worked .. Try next point\n"
          set jump [expr $jump+1];
          integrator DisplacementControl 2 1 [expr $dU*$jump] 1
        }

        test NormDispIncr $tolLatNew $iterLatNew

        algorithm Newton

      } else {
        set jump 1
        integrator DisplacementControl 2 1 $dU 1
      }

      set currentDisp [expr $currentDisp+$dU]

  }
}
