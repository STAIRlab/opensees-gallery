
# --------------------------------------------------------------------------------------------------
# LibUnits.tcl -- define system of units
#		Silvia Mazzoni & Frank McKenna, 2006
#
# Modified by @siwalan for personal purposes (Metric data). 
# Correctness not guaranteed (at least for my addition). Use it at your own discretion

# define UNITS ----------------------------------------------------------------------------
set meter 1.;
set mm [expr 1./1000.*$meter];

#set mm [expr 1.0];
#set meter [expr 1000*$mm];
set N 1.;
set inch [expr 25.4*$mm];
set in [expr 25.4*$mm];
set ft [expr 12*$inch]
set kip [expr 4448.226*$N];
set sec 1.;
set MPa [expr $N/pow($mm,2)];
set GPa [expr 1000.0 * $MPa]
set kip [expr 4.44822 * 1000.0 * $N]
set ksi [expr $kip/pow($in,2)];

set LunitTXT "meter";			# define basic-unit text for output
set FunitTXT "Newton";			# define basic-unit text for output
set TunitTXT "sec";			# define basic-unit text for output

set PI [expr 2*asin(1.0)]; 		# define constants
set g [expr 32.2*$ft/pow($sec,2)]; 	# gravitational acceleration
set kg [expr 1*$sec/pow($meter,2)]
set kgf [expr $kg*$g]; # Asume Newton Second Meter
set ton [expr 1000.0 *$kg]
set tonf [expr $ton*$g]
set Ubig 1.e10; 			# a really large number
set Usmall [expr 1/$Ubig]; 		# a really small number

proc Wsection { secID matID d bf tf tw nfdw nftw nfbf nftf {Orient ZZ}} {
    # ###################################################################
    # Wsection  $secID $matID $d $bf $tf $tw $nfdw $nftw $nfbf $nftf
    # ###################################################################
    # create a standard W section given the nominal section properties
    # written: Remo M. de Souza
    # date: 06/99
    # modified: 08/99  (according to the new general modelbuilder)
    # input parameters
    # secID - section ID number
    # matID - material ID number 
    # d  = nominal depth
    # tw = web thickness
    # bf = flange width
    # tf = flange thickness
    # nfdw = number of fibers along web depth 
    # nftw = number of fibers along web thickness
    # nfbf = number of fibers along flange width
    # nftf = number of fibers along flange thickness

    set dw [expr $d - 2 * $tf]
    set y1 [expr -$d/2.0]
    set y2 [expr -$dw/2.0]
    set y3 [expr  $dw/2.0]
    set y4 [expr  $d/2.0]
    
    set z1 [expr -$bf/2.0]
    set z2 [expr -$tw/2.0]
    set z3 [expr  $tw/2.0]
    set z4 [expr  $bf/2.0]

    if {$Orient == "Weak" || $Orient == "YY" } {
	set dw [expr $d - 2 * $tf]
	set z1 [expr -$d/2.0]
	set z2 [expr -$dw/2.0]
	set z3 [expr  $dw/2.0]
	set z4 [expr  $d/2.0]

	set y1 [expr  $bf/2.0]
	set y2 [expr  $tw/2.0]
	set y3 [expr -$tw/2.0]
	set y4 [expr -$bf/2.0]
	
	section fiberSec  $secID  {
	    patch quadr  $matID  $nfbf $nftf   $y1 $z3   $y1 $z4   $y4 $z4   $y4 $z3
	    patch quadr  $matID  $nftw $nfdw   $y2 $z3   $y3 $z3   $y3 $z2   $y2 $z2
	    patch quadr  $matID  $nfbf $nftf   $y1 $z1   $y1 $z2   $y4 $z2   $y4 $z1
	}
	
    } else {
	set dw [expr $d - 2 * $tf]
	set y1 [expr -$d/2.0]
	set y2 [expr -$dw/2.0]
	set y3 [expr  $dw/2.0]
	set y4 [expr  $d/2.0]

	set z1 [expr -$bf/2.0]
	set z2 [expr -$tw/2.0]
	set z3 [expr  $tw/2.0]
	set z4 [expr  $bf/2.0]
	
	section fiberSec  $secID  -GJ 1e8 {
	    #                     nfIJ  nfJK    yI  zI    yJ  zJ    yK  zK    yL  zL
	    patch quadr  $matID  $nfbf $nftf   $y1 $z4   $y1 $z1   $y2 $z1   $y2 $z4
	    patch quadr  $matID  $nftw $nfdw   $y2 $z3   $y2 $z2   $y3 $z2   $y3 $z3
	    patch quadr  $matID  $nfbf $nftf   $y3 $z4   $y3 $z1   $y4 $z1   $y4 $z4
	}
    }
}

# Define Material
set Fy [expr 345*$MPa]
set Es [expr 204*$GPa];		# Steel Young's Modulus
set hardening 0.01
set matIDhard 1

foreach ndm {2 3} {

  wipe
  model BasicBuilder -ndm $ndm;

  uniaxialMaterial Steel01  $matIDhard $Fy $Es $hardening

  set transformationKey 1
  if {$ndm == 2} {
    node 1  0 0
    node 2 10 0
    node 3 20 0
    node 4 30 0

    fix 1 1 1 1
    fix 2 1 1 1
    fix 3 1 1 1
    fix 4 1 1 1
    geomTransf Linear 1

  } else {
    node 1  0 0 0
    node 2 10 0 0
    node 3 20 0 0
    node 4 30 0 0

    fix 1 1 1 1 1 1 1
    fix 2 1 1 1 1 1 1
    fix 3 1 1 1 1 1 1
    fix 4 1 1 1 1 1 1
    geomTransf Linear 1 0 0 1
  }


  set nfdw 4;		# number of fibers along web depth 
  set nftw 1;		# number of fibers along web thickness
  set nfbf 1;		# number of fibers along flange width
  set nftf 4;		# number of fibers along flange thickness


  ##### W14x370
  set d [expr 17.9*$in];	# depth
  set tw [expr 1.66*$in];	# web thickness
  set bf [expr 16.5*$in];	# flange width
  set tf [expr 2.66*$in];	# flange thickness
  Wsection  1 1 $d $bf $tf $tw $nfdw $nftw $nfbf $nftf 

  set section 1

  set W2144Area [expr 13.0*$inch*$inch]; 
  set W2144xI  [expr 843*$inch*$inch*$inch*$inch];

  puts "Es: [expr 20400*$MPa]"
  element elasticBeamColumn 12 1 2  $W2144Area [expr 204000*$MPa] $W2144xI $transformationKey -release 1;
  element elasticBeamColumn 23 2 3 $section $transformationKey  -release 3 ;
  element elasticBeamColumn 34 3 4 $section $transformationKey  ;

  print -json
}
