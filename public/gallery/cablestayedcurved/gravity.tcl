	puts  "Gravity Analysis..."
 #----------------------------------------------------------------
	system         BandGeneral
	constraints    Transformation
	numberer       RCM
	test           NormDispIncr 1.0e-2 100 3
	algorithm      NewtonLineSearch .5
	integrator     LoadControl 1
	analysis       Static
	analyze        1
	puts           "Completing Gravity Analysis."
	loadConst      -time 0.0
	puts "completing the gravity analysis"
#****************************************************************
