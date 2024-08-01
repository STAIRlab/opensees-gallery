## -----------------------------------------------------------------------------------------------------------------------
# Author: Nikolay Velkov.
# Date: 7/23/2021
# ------------------------------------------------------------------------------------------------------------------------

# SET UP ----------------------------------------------------------------------------
wipe;                # clear memory of all past model definitions
model BasicBuilder -ndm 3 -ndf 6;    # Define the model builder, ndm=#dimension, ndf=#dofs


# define UNITS ----------------------------------------------------------------------------
set in 1.; 				# define basic units -- output units
set kip 1.; 			# define basic units -- output units
set sec 1.; 			# define basic units -- output units
set LunitTXT "inch";			# define basic-unit text for output
set FunitTXT "kip";			# define basic-unit text for output
set TunitTXT "sec";			# define basic-unit text for output
set ft [expr 12.*$in]; 		# define engineering units
set ksi [expr $kip/pow($in,2)];
set psi [expr $ksi/1000.];
set lbf [expr $psi*$in*$in];		# pounds force
set pcf [expr $lbf/pow($ft,3)];		# pounds per cubic foot
set psf [expr $lbf/pow($ft,3)];		# pounds per square foot
set in2 [expr $in*$in]; 		# inch^2
set in4 [expr $in*$in*$in*$in]; 		# inch^4
set cm [expr $in/2.54];		# centimeter, needed for displacement input in MultipleSupport excitation
set PI [expr 2*asin(1.0)]; 		# define constants
set g [expr 32.2*$ft/pow($sec,2)]; 	# gravitational acceleration
set Ubig 1.e10; 			# a really large number
set Usmall [expr 1/$Ubig]; 		# a really small number

# column section GEOMETRY -------------------------------------------------------------
set DSec [expr 4.0*$ft];           # Column Diameter
set numBarsSec 30;                # number of uniformly-distributed longitudinal-reinforcement bars
set barDSec [expr 1.41*$in];    # diameter of longitudinal-reinforcement bars
set barAreaSec [expr $PI*pow($barDSec,2)/4.0];    # area of longitudinal-reinforcement bars
set coverSec [expr 2.0*$in];        # Column cover
set sTbar  [expr 12.0*$in];          #Spacing of transverse spiral reinforcement
set Dcore        [expr $DSec-2.0*$coverSec];              # Diameter of circular core
set DTbar        [expr 0.5*$in];                                    # Diameter of transverse spiral reinforcement bar (#5 Rebar)
set Asp            [expr $PI*pow($DTbar,2)/4.0];          # Area of transverse spiral reinforcement bar
set Dtran        [expr $Dcore-$DTbar];                            # Diameter of spiral of transverse spiral reinforcement
set rho            [expr 4.0*$Asp/($Dtran*$sTbar)];                # Density of transverse spiral reinforcement
set Dlong        [expr $Dcore-$DTbar*2-$barDSec];                # Diameter of ring of longitudinal reinforcement
set SecTag 1;            # set tag for symmetric section

# MATERIAL parameters -------------------------------------------------------------------
set IDconcCore 1;                 # material ID tag -- confined core concrete
set IDconcCover 2;                 # material ID tag -- unconfined cover concrete
set IDreinf 3;                     # material ID tag -- reinforcement


# nominal concrete compressive strength
set fc         [expr -5.0*$ksi];        # CONCRETE Compressive Strength, ksi   (+Tension, -Compression)
set Ec         [expr 57.0*$ksi*sqrt(-$fc/$psi)];    # Concrete Elastic Modulus
set fce         [expr -5.0*$ksi];        # CONCRETE Compressive Strength, ksi   (+Tension, -Compression)
set ec0    -0.002;
set    esp -0.005;
set fy     [expr 48.0*$ksi]; # STEEL yield stress
# confined concrete
set ke         [expr 1.0-$sTbar/$Dtran];            # ratio of confined to unconfined concrete strength
set f3e            [expr -$ke*$rho*$fy/2.0];                     # Effective confinement strength
set fcc         [expr $fce+4.1*$f3e];    # Core compressive strength -compression
set fcc [expr 1.05*$fce];
set ecc         [expr $ec0*(1.0+5.0*($fcc/$fce-1.0))];    # Core strain at maximum strength -compression
set ecu         [expr -0.004-$f3e/(4.0*$fce)];            # Core crushing (ultimate) strain -compression
set ecu -0.00912;
# puts "f3e=$f3e, fcc=$fcc, ecc=$ecc, ecu=$ecu";
set lambda 0.1;                                            # Ratio between unloading slope at $eps2 and initial slope $Ec
set xu             [expr $ecu/$ecc];                        # Mander equation parameter x
set ru             [expr $Ec/($Ec-$fcc/$ecc)];             # Mander equation parameter r
set fcu         [expr $fcc*$xu*$ru/($ru-1+$xu**$ru)];    # Core crushing (ultimate) strength -compression
# puts "xu=$xu, ru=$ru, fcu=$fcu";
# tensile Properties
set ftU [expr 7.5*sqrt(-$fce/$psi)*$psi];        # Cover tensile strength +tension
set ftC [expr 7.5*sqrt(-$fcc/$psi)*$psi];        # Core tensile strength +tension
set Ets 70;                                    # Tension softening stiffness *Check if causes numerical issues (Divide by constant to make flatter if needed)
#------------------
# steel proprties
set Es        [expr 29000.*$ksi];        # modulus of steel
#------only for Stee02
#set Bs        0.01;            # strain-hardening ratio
#set R0 18;                # control the transition from elastic to plastic branches
#set cR1 0.925;                # control the transition from elastic to plastic branches
#set cR2 0.15;                # control the transition from elastic to plastic branches
# buckling properites
set Isr [expr $sTbar/$barDSec];
set beta 0.75;
#------only for -GABuck
#set r 0.;
#set gamma 0.5;

# Torsional and shear Properties
set nu 0.2;            # Poisson's ratio
set Gc [expr $Ec/2./[expr 1+$nu]];      # Torsional stiffness Modulus
set JCol [expr pow($DSec,4)*$PI/32.];                     # cross-sectional area

uniaxialMaterial Concrete02 $IDconcCore $fcc $ecc [expr 0.15*$fcc] $ecu $lambda $ftC $Ets;    # build core concrete (confined)
uniaxialMaterial Concrete02 $IDconcCover $fce $ec0 [expr 0.1*$fce] $esp $lambda $ftU $Ets;    # build cover concrete (unconfined)
#uniaxialMaterial ReinforcingSteel $IDreinf $fy $fu $Es $Esh $esh $esu -GABuck $Isr $beta $r $gamma;                 # build reinforcement material
#uniaxialMaterial ReinforcingSteel $IDreinf $fy $fu $Es $Esh $esh $esu -DMBuck $Isr $beta;            # build reinforcement material
uniaxialMaterial Steel02 $IDreinf $fy $Es 0.05; #$R0 $cR1 $cR2;                # build reinforcement material

# fiber section generation
set Rout [expr $DSec/2];    # overall (outer) radius of the section
set Rcore [expr $Dcore/2.];                    # Core radius
set Rlong [expr $Dlong/2.];                    # Longitudinal reinforcement radius
set nfCoreR 5;        # number of radial divisions in the core (number of "rings")
set nfCoreT $numBarsSec;        # number of theta divisions in the core (number of "wedges")
set nfCoverR 2;        # number of radial divisions in the cover
set nfCoverT $numBarsSec;        # number of theta divisions in the cover
# Define the fiber section
section fiberSec $SecTag -GJ [expr $Gc*$JCol] {
    patch circ $IDconcCore $nfCoreT $nfCoreR 0 0 0 $Rcore 0 360;        # Define the core patch
    patch circ $IDconcCover $nfCoverT $nfCoverR 0 0 $Rcore $Rout 0 360;    # Define the cover patch
    set theta [expr 360.0/$numBarsSec];        # Determine angle increment between bars
    layer circ $IDreinf $numBarsSec $barAreaSec 0 0 $Rlong $theta 360;    # Define the reinforcing layer
}

# define column GEOMETRY -------------------------------------------------------------
set LCol [expr 22.*$ft+33.*$in];         # column length
# calculated geometry parameters
set ACol [expr pow($DSec,2)*$PI/4.];                     # cross-sectional area

# define cap beam GEOMETRY -------------------------------------------------------------
set HBeam  [expr 66.0*$in];        # Beam Height(Depth) [inch]
set WBeam  [expr 54.0*$in];        # Beam Width [inch]
set ABeam [expr 4473.75*pow($in,4)];
set IzBeam [expr 2108740.7*pow($in,4)];
set IyBeam [expr 2881268.4*pow($in,4)];
set JBeam [expr 4983926.1*pow($in,4)];            # set large torsional stiffness


# define deck GEOMETRY -------------------------------------------------------------
set ADeck [expr 9462.97*pow($in,4)];
set IyDeck [expr 6108134.16*pow($in,4)];
set IzDeck [expr 197610268.48*pow($in,4)];
set JDeck [expr 203709907*pow($in,4)];


set wconc [expr 144.*$pcf];
set Weight [expr $LCol*$ACol*$wconc];         # superstructure weight
set Mass [expr $Weight/$g];        # nodal mass
set PCol [expr 0.05*$ACol*$fce];         # nodal dead-load weight per column

# cap beam length beyond column
set overHang [expr 6.3*$ft];
# distance between columns
set WCol [expr 287*$in];
# length of deck in the -z direction
set LleftDeck [expr 104*$ft];
# length of deck in the +z direction
set LrightDeck [expr 99*$ft];
# height of node at abutment 1 (node 8)
set HleftDeck [expr $LCol+6.125*$ft];
# angle between deck and bent normal (rad)
set tilt 0.3949;
set slope [expr 6.125/104];
# nodal coordinates:  node#, X, Y, Z
node 1 -[expr $WCol/2] 0 0;                  # base of col1
node 2 [expr $WCol/2] 0 0;    # base of col2
node 3 -[expr $WCol/2 + $overHang] $LCol 0;   # -x end of cap beam
node 4 -[expr $WCol/2] $LCol 0;           # top of col1
node 5 0 $LCol 0; # midpoint of cap beam
node 6 [expr $WCol/2] $LCol 0;  # top of col2
node 7 [expr $WCol/2 + $overHang] $LCol 0;  # +x end of cap beam
# left deck
node 8  [expr sin($tilt)*($LleftDeck)]  $HleftDeck [expr -cos($tilt)*($LleftDeck)];
node 9  [expr sin($tilt)*($LleftDeck*3/4)]  [expr $HleftDeck - $slope*$LleftDeck*3/4] [expr -cos($tilt)*($LleftDeck*3/4)];
node 10  [expr sin($tilt)*($LleftDeck*2/4)] [expr $HleftDeck - $slope*$LleftDeck*2/4] [expr -cos($tilt)*($LleftDeck*2/4)];
node 11  [expr sin($tilt)*($LleftDeck*1/4)] [expr $HleftDeck - $slope*$LleftDeck*1/4] [expr -cos($tilt)*($LleftDeck*1/4)];
# right deck
node 12 [expr -sin($tilt)*($LrightDeck*1/3)] [expr $LCol - $slope*$LrightDeck*1/3] [expr cos($tilt)*($LrightDeck*1/3)];
node 13 [expr -sin($tilt)*($LrightDeck*2/3)] [expr $LCol - $slope*$LrightDeck*2/3] [expr cos($tilt)*($LrightDeck*2/3)];
node 14 [expr -sin($tilt)*($LrightDeck)] [expr $LCol - $slope*$LrightDeck] [expr cos($tilt)*($LrightDeck)];

# Single point constraints -- Boundary Conditions
fix 1 1 1 1 1 1 1;             # column 1 base
fix 2 1 1 1 1 1 1;             # column 2 base


# define geometric transformation: performs a linear geometric transformation of beam stiffness and resisting force from the basic system to the global-coordinate system
set ColTransfTag 1;             # associate a tag to column transformation
geomTransf PDelta $ColTransfTag 0 0 -1 -jntOffset 0 0 0 0 [expr -$HBeam/2] 0;
set BeamTransfTagL 2;             # associate a tag to column transformation
set BeamTransfTagR 3;             # associate a tag to column transformation
geomTransf Linear $BeamTransfTagL 0 1 0 -jntOffset 0 0 0 -$Rout 0 0;
geomTransf Linear $BeamTransfTagR 0 1 0 -jntOffset $Rout 0 0 0 0 0;
set DeckTransfTag 4;             # associate a tag to column transformation
geomTransf Linear $DeckTransfTag 0 1 0 ;

# element connectivity:
set numIntgrPts 3;                                # number of integration points for force-based element
# bent columns
element nonlinearBeamColumn 1 1 4 $numIntgrPts $SecTag $ColTransfTag;    # self-explanatory when using variables
element nonlinearBeamColumn 2 2 6 $numIntgrPts $SecTag $ColTransfTag;    # self-explanatory when using variables
# cap beam
element elasticBeamColumn 3 3 4 $ABeam $Ec $Gc $JBeam $IyBeam $IzBeam $BeamTransfTagL;    # self-explanatory when using variables
element elasticBeamColumn 4 4 5 $ABeam $Ec $Gc $JBeam $IyBeam $IzBeam $BeamTransfTagR;    # self-explanatory when using variables
element elasticBeamColumn 5 5 6 $ABeam $Ec $Gc $JBeam $IyBeam $IzBeam $BeamTransfTagL;    # self-explanatory when using variables
element elasticBeamColumn 6 6 7 $ABeam $Ec $Gc $JBeam $IyBeam $IzBeam $BeamTransfTagR;    # self-explanatory when using variables
#  deck
element elasticBeamColumn  7  8  9 $ADeck $Ec $Gc $JDeck $IyDeck $IzDeck $DeckTransfTag;    # self-explanatory when using variables
element elasticBeamColumn  8  9 10 $ADeck $Ec $Gc $JDeck $IyDeck $IzDeck $DeckTransfTag;    # self-explanatory when using variables
element elasticBeamColumn  9 10 11 $ADeck $Ec $Gc $JDeck $IyDeck $IzDeck $DeckTransfTag;    # self-explanatory when using variables
element elasticBeamColumn 10 11  5 $ADeck $Ec $Gc $JDeck $IyDeck $IzDeck $DeckTransfTag;    # self-explanatory when using variables
element elasticBeamColumn 11  5 12 $ADeck $Ec $Gc $JDeck $IyDeck $IzDeck $DeckTransfTag;    # self-explanatory when using variables
element elasticBeamColumn 12 12 13 $ADeck $Ec $Gc $JDeck $IyDeck $IzDeck $DeckTransfTag;    # self-explanatory when using variables
element elasticBeamColumn 13 13 14 $ADeck $Ec $Gc $JDeck $IyDeck $IzDeck $DeckTransfTag;    # self-explanatory when using variables

print -json


