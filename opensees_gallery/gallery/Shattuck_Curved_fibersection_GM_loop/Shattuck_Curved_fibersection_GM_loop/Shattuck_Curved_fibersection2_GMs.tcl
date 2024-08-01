# --------------------------------------------------------------------------------------------------
# Curved BART aerial structure, located midway between Rockridge and MacArthur Stations 
#
#

# SET UP ----------------------------------------------------------------------------
wipe;				# clear memory of all past model definitions

file mkdir Data; 					# create data directory

# Loop over the ground motions
set file1 [open "Groundmotions.txt" r]
gets $file1 numgrmot;
close $file1

set gmshift 0;
set numdatperln 5;
set nrGM 0;


for { set igrx [expr $gmshift+1] } { $igrx <= $numgrmot } { incr igrx } {
    puts "GM NUMBER=$igrx"
    set nrGM [expr $nrGM+1];
    set file1 [open "Groundmotions.txt" r]
    set cntgr 0; 
    foreach line [split [read $file1] "\n"] {
	incr cntgr 1; 
	puts $cntgr
	if {$cntgr == [expr $igrx+1] } {
	    set wordloop 0;
	    foreach word [split $line] {
		if {$word !=""} {
		    incr wordloop 1;
		    if {$wordloop == 1 } {
			set grmotname $word; 
			puts "check1"
		    }
		    if {$wordloop == 2 } {
			set indvscfac $word;
			set SF $indvscfac;
			break 
			puts "check2"
		    }
		}
	    }
	    break
	}
    }
    close $file1

    source ReadSMDFile.tcl;
    
    set inFile "GMs/$grmotname.AT2";
    puts $inFile;
    set outFile "GMs/$grmotname.acc";
    puts $outFile;
    ReadSMDFile $inFile $outFile $numdatperln dttrans nptstrans;
    
	  
    
    set tGM [expr $dttrans*$nptstrans*1.5];
    set DtAnalysis 0.005;
    set Nsteps [expr int($tGM/$DtAnalysis)];	  

	model BasicBuilder -ndm 3 -ndf 6;	# Define the model builder, ndm=#dimension, ndf=#dofs
	set dataDir Data;			# set up name of data directory -- remove
	file mkdir $dataDir; 			# create data directory
	set GMdir "../GMfiles";		# ground-motion file directory
	set ViewScale 0.25;			# scaling factor for viewing deformed shape, it depends on the dimensions of the model
	source LibUnits.tcl;			# define units
	source DisplayPlane.tcl;		# procedure for displaying a plane in model
	source DisplayModel3D.tcl;		# procedure for displaying 3D perspectives of model
	source BuildRCrectSection1.tcl;		# procedure for definining RC fiber section

	# define GEOMETRY -------------------------------------------------------------

	# define NODAL COORDINATES
	# Abutment 47
	node 471	117302.3244	20222.29524	1601.64;
	node 472	117305.0871	20186.01622	1601.64;
	node 473	117308.0823	20146.68381	1601.64;
	node 474	117318.996	20003.30411	1617.96;
	node 475	117321.7585	19967.02785	1617.96;
	node 476	117324.7542	19927.68834	1617.96;

	# Intermediate nodes Abutment 47 - Pier 48
	node 111	117495.2429	20199.78856	1603.58;
	node 211	117510.0133	19980.53711	1620.31;
	node 112	117685.5192	20211.86194	1605.53;
	node 212	117698.3789	19992.40159	1622.66;
	node 113	117875.8948	20222.25595	1607.47;
	node 213	117886.841	20002.62045	1625.02;
	node 114	118066.3545	20230.96982	1609.42;
	node 214	118075.3852	20011.19275	1627.37;

	# Pier 48
	node 481	118260.44	20128.06	1320.00;
	node 482	118260.44	20128.06	1516.11;
	node 483	118260.44	20128.06	1620.54;
	node 484	118256.88	20238.00	1611.36;
	node 485	118264.00	20018.12	1629.72;

	# Intermediate nodes Pier 48 - Pier 49
	node 121	118539.1172	20245.32917	1614.38;
	node 221	118543.3861	20025.34629	1633.18;
	node 122	118821.4223	20248.96739	1617.41;
	node 222	118822.8453	20028.96049	1636.63;
	node 123	119103.7507	20248.91697	1620.43;
	node 223	119102.3279	20028.96008	1640.09;
	node 124	119386.0545	20245.17784	1623.46;
	node 224	119381.7872	20025.34493	1643.54;

	# Pier 49
	node 491	119664.78	20127.93	1356.00;
	node 492	119664.78	20127.93	1531.23;
	node 493	119664.78	20127.93	1636.74;
	node 494	119668.29	20237.75	1626.48;
	node 495	119661.18	20018.12	1647.00;

	# Intermediate nodes Pier 49 - Abutment 50
	node 131	119833.1633	20231.70342	1628.33;
	node 231	119779.9242	20013.94764	1648.44;
	node 132	119997.9903	20224.39757	1630.18;
	node 232	119898.6475	20009.1266	1649.88;
	node 133	120162.7567	20215.83339	1632.02;
	node 233	120017.3424	20003.65293	1651.32;
	node 134	120327.4529	20206.01149	1633.87;
	node 234	120136.0055	19997.52665	1652.76;

	# Abutment 50
	node 501	120494.6558	20231.3041	1635.72;
	node 502	120492.0694	20194.93225	1635.72;
	node 503	120489.2658	20155.50613	1635.72;
	node 504	120256.8134	20027.14623	1654.20;
	node 505	120254.6331	19990.74791	1654.20;
	node 506	120252.2697	19951.29292	1654.20;

	# Boundary conditions
	fix 481 1  1  1  1  1  1;    # Bent 48 Column Bottom, piles will be added later
	fix 491 1  1  1  1  1  1;    # Bent 49 Column Bottom, piles will be added later

	fix 471	1  1  1  0  0  0;    # Abutment 47 nodes, will be replaced by springs later
	fix 472	1  1  1  1  1  1;
	fix 473	1  1  1  0  0  0;
	fix 474	1  1  1  0  0  0;
	fix 475	1  1  1  0  0  0;
	fix 476	1  1  1  0  0  0;

	fix 501	1  1  1  0  0  0;    # Abutment 50 nodes, will be replaced by springs later
	fix 502	1  1  1  1  1  1;
	fix 503	1  1  1  0  0  0;
	fix 504	1  1  1  0  0  0;
	fix 505	1  1  1  1  1  1;
	fix 506	1  1  1  0  0  0;

	# ELEMENTS
	# Use rigid links for the rigid elements
	# rigidLink beam 472 471;     # Abutment 47
	# rigidLink beam 472 473;

	# rigidLink beam 502 501;     # Abutment 50
	# rigidLink beam 502 503;

	# rigidLink beam 483 482;     # Bent 48  
	# rigidLink beam 483 484;
	# rigidLink beam 483 485;

	# rigidLink beam 493 492;     # Bent 49  
	# rigidLink beam 493 494;
	# rigidLink beam 493 495;

	# columns and aerial girders
	geomTransf Linear 1 0 1 0;                # transformation for girders, consider the rigid end offset later
	geomTransf PDelta 2 0 1 0;                # transformation for columns, update later considering the actual

	# correct values for the beam, double check
	set E 4595.4;
	set G 1838.2;
	set A 7577.8750;
	set Iy 4987074.7140;
	set Iz 8119339.1141;
	set J [expr $Iy+$Iz];
	set wconc 2.246520588911893e-07; # computed as (0.150kip/386.4)/(12 inch)^3

	# correct values for the column, double check
	set hcol 106.0;
	set bcol 60.0;
	set Ecol 4595.4;
	set Gcol 1838.2;
	set Acol [expr $hcol*$bcol];
	set Iycol [expr $hcol*$hcol*$hcol*$bcol/12.0];
	set Izcol [expr $bcol*$bcol*$bcol*$hcol/12.0];
	set Jcol [expr $Iycol+$Izcol];
	set wconc 2.246520588911893e-07; # computed as (0.150kip/386.4)/(12 inch)^3

	# Define the column section
	BuildRCrectSection1 1;  #left column

	#element elasticBeamColumn $eleTag $iNode $jNode $A $E $G $J $Iy $Iz $transfTag <-mass $massDens> <-cMass>
	# span 1 (Abutment 47 - Pier 48) CL 
	element elasticBeamColumn 111 472 111 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 112 111 112 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 113 112 113 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 114 113 114 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 115 114 484 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;

	# span 1 (Abutment 47 - Pier 48) CR
	element elasticBeamColumn 211 475 211 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 212 211 212 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 213 212 213 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 214 213 214 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 215 214 485 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;

	# Pier 48
	#element elasticBeamColumn 481 481 482 $Acol $Ecol $Gcol $Jcol $Iycol $Izcol 2 -mass [expr $wconc*$Acol] -cMass;
	#element forceBeamColumn $eleTag $iNode $jNode $numIntgrPts $secTag $transfTag 
	element forceBeamColumn 481 481 482 4 1 2 -mass [expr $wconc*$Acol];

	# span 2 (Pier 48 - Pier 49) CL
	element elasticBeamColumn 121 484 121 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 122 121 122 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 123 122 123 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 124 123 124 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 125 124 494 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;

	# span 2 (Pier 48 - Pier 49) CR
	element elasticBeamColumn 221 485 221 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 222 221 222 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 223 222 223 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 224 223 224 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 225 224 495 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;

	# Pier 49
	#element elasticBeamColumn 491 491 492 $Acol $Ecol $Gcol $Jcol $Iycol $Izcol 2 -mass [expr $wconc*$Acol] -cMass;
	#element forceBeamColumn $eleTag $iNode $jNode $transfTag
	element forceBeamColumn 491 491 492 4 1 2 -mass [expr $wconc*$Acol];

	# span 3 (Pier 49 - Abutment 50) CL
	element elasticBeamColumn 131 494 131 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 132 131 132 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 133 132 133 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 134 133 134 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 135 134 502 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;

	# span 3 (Pier 49 - Abutment 50) CR
	element elasticBeamColumn 231 495 231 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 232 231 232 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 233 232 233 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 234 233 234 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 235 234 505 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;

	# rigid elements
	element elasticBeamColumn 471 471 472 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 472 472 473 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 501 501 502 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 502 502 503 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 482 482 483 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 483 483 484 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 485 483 485 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 492 492 493 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 493 493 494 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;
	element elasticBeamColumn 495 493 495 $A $E $G $J $Iy $Iz 1 -mass [expr $wconc*$A] -cMass;

	# Eigenvalue Analysis
	set lambdaN [eigen -fullGenLapack 4];

	puts "Eigenvalue analysis complete"
	set lambda1 [lindex $lambdaN 0];
	set lambda2 [lindex $lambdaN 1];
	set lambda3 [lindex $lambdaN 2];

	set omega1 [expr pow($lambda1,0.5)];
	set omega2 [expr pow($lambda2,0.5)];
	set omega3 [expr pow($lambda3,0.5)];

	set pi 3.14159265359;

	set T1 [expr 2.0*$pi/$omega1];
	set T2 [expr 2.0*$pi/$omega2];
	set T3 [expr 2.0*$pi/$omega3];

	puts "T1 = $T1; T2 = $T2; T3=$T3"
	
	set Damp 0.0171;
    
    set alphaM [expr 2.0*$Damp*$omega1*$omega2/($omega1+$omega2)]; # M-prop. damping; D = alphaM*M
    set betaKcurr 0.;                                      # current-K-prop. damping;   + beatKcurr*KCurrent
    set betaKinit [expr 2.0*$Damp/($omega1+$omega2)];                                      # initial-k prop. damping;   + beatKinit*Kini
    set betaKcomm 0.0;      # committ-K-prop. damping;   + betaKcomm*KlastCommitt
    rayleigh $alphaM $betaKcurr $betaKinit $betaKcomm; 	   # RAYLEIGH damping
    
    
    #rayleigh [expr 2*0.5*pow($lambda,0.5)] 0. 0. 0.;		# set damping based on first eigen mode
    #rayleigh 0. 0. 0. 0.;		# set damping based on first eigen mode
    
	#set accelSeries "Series -dt 0.01 -filePath H-e12140.g3 -factor 386.4";	# define acceleration vector from file (dt=0.01 is associated with the input file gm)
    set GMfattx [expr 386.4*$SF];
    set AccelSeries	"Series -dt $dttrans -filePath $outFile -factor [expr $GMfattx]";

    puts "ACCEL $AccelSeries"

    set IDloadTag	4;
    set GMdirection	 1;
    puts "check3";
    # pattern UniformExcitation 1 1 -accel  $AccelSeries  ;        # create Unifform excitation
    pattern UniformExcitation $IDloadTag $GMdirection -accel $AccelSeries;
    puts "check4";

    # set per [expr 2*3.14/pow($lambda,0.5)]
    # puts "per=$per"
    # create the analysis
    #wipeAnalysis;					# clear previously-define analysis parameters
    system BandGeneral
    
    # create the DOF numberer
    numberer RCM
    
    # create the constraint handler
    constraints Transformation
    
    # create the convergence test
    test EnergyIncr 1.0e-6 10
    
    # create the integration scheme
    #integrator NewmarkExplicit 0.5
    #integrator HHTGeneralizedExplicit 0.0 0.5
    #integrator NewmarkExplicit 0.5
    #integrator AlphaOS 1.0
	
	integrator Newmark 0.5 0.25
    
    # create the solution algorithm
    #algorithm Linear
	algorithm Newton
    
    # create the analysis object 
    analysis Transient
    # open output file for writing

    set outFileID1 [open elapsedTime.txt w]
    # perform the transient analysis
    # run the analysis longer for k=1.0 20000 for others 13550
    
    
    set tTot [time {
	for {set i 1} {$i < $Nsteps} {incr i} {    
	    set t [time {analyze  1  [expr $DtAnalysis]}]
	    puts $outFileID1 $t
	    #puts "step $i"
	}
    }]

    puts "\nElapsed Time = $tTot \n"
    # close the output file
    close $outFileID1
    
    #analyze 1950 0.02;					# apply 1000 0.02-sec time steps in analysis
    
    
    puts "Done!"
    wipe;

}