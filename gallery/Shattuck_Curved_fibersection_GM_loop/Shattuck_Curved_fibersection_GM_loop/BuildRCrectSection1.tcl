proc BuildRCrectSection1 {id } {
    source LibUnits.tcl

#   Define the materials

	#uniaxialMaterial Concrete02 $coreID $fc1C $eps1C $fc2C $eps2C $lambda $ftC $Ets;	# Core concrete (confined)
	
    #uniaxialMaterial Concrete02 $matTag $fpc $epsc0 $fpcu $epsU $lambda $ft $Ets
	uniaxialMaterial Concrete02 1 -6.5 -0.002 -0.5 -0.005 0.1 0.65 500.;  # cover concrete
    uniaxialMaterial Concrete02 2 -6.5 -0.002 -0.5 -0.005 0.1 0.65 500.;   # core concrete  # assuming the transverse reinforcement spacing is 24", core concrete is the same as cover concrete
	# this can be updated as needed later if it turns out the transverse reinforcement spacing is actually different
#	uniaxialMaterial Steel02 $IDSteel  $Fy $Es $Bs <$R0 $cR1 $cR2>
    uniaxialMaterial Steel02 3  40.0 29000.0 0.1;                       # steel

	# Define the fiber section, dimensions of the section are 106" by 60" with a cover of 3"
	section fiberSec $id -GJ 1000000000000.0 {     # this is to add a large stiffness in torsion
		# Define the core patch
		#patch rect $matTag $numSubdivY $numSubdivZ $yI $zI $yJ $zJ
		patch rect 2 60 100 -27.0 -50.0 27.0 50.0;     # short direction is y, long direction is z
		
		# define the four cover patches
		patch rect 1   3 106  27.0 -53.0  30.0  53.0;     # top strip along the z direction 
		patch rect 1   3 106 -30.0 -53.0 -27.0  53.0;     # bottom strip along the z direction
		patch rect 1  54   3  27.0  53.0 -27.0 -50.0;     # left strip along the y direction
		patch rect 1  54   3  27.0 -50.0 -27.0 -53.0;     # right strip along the y direction
		
		# define reinforcing layers
		# layer straight $matTag $numBars $areaBar    $yStart    $zStart     $yEnd      $zEnd
		  layer straight       3       18      4.0    25.3715    48.3715   25.3715   -48.3715;  # top reinforcement layer along the z direction
		  layer straight       3       18      4.0   -25.3715    48.3715  -25.3715   -48.3715;  # bottom reinforcement layer along the z direction
		  layer straight       3        8      4.0    19.7334    48.3715  -19.7334    48.3715;  # left reinforcement layer along the y direction 
		  layer straight       3        8      4.0    19.7334   -48.3715  -19.7334   -48.3715;  # right reinforcement layer along the y direction
		  layer straight       3        3      4.0    19.7334    36.9900   19.7334    14.2269;
		  layer straight       3        3      4.0    19.7334   -14.2269   19.7334   -36.9900;
		  layer straight       3        3      4.0   -19.7334    36.9900  -19.7334    14.2269;
		  layer straight       3        3      4.0   -19.7334   -14.2269  -19.7334   -36.9900;
		  
		  
		  
		# layer straight $steelID $numBarsInt $barAreaInt  -$coreY $coreZ $coreY $coreZ;	# intermediate skin reinf. +z
		# layer straight $steelID $numBarsInt $barAreaInt  -$coreY -$coreZ $coreY -$coreZ;	# intermediate skin reinf. -z
		# layer straight $steelID $numBarsTop $barAreaTop $coreY $coreZ $coreY -$coreZ;	# top layer reinfocement
		# layer straight $steelID $numBarsBot $barAreaBot  -$coreY $coreZ  -$coreY -$coreZ;	# bottom layer reinforcement





	# #    
	# #                        y
	# #                        ^
	# #                        |     
	# #             ---------------------    --   --
	# #             |   o     o     o    |     |    -- coverH
	# #             |                      |     |
	# #             |   o            o    |     |
	# #    z <--- |          +          |     HSec
	# #             |   o            o    |     |
	# #             |                      |     |
	# #             |   o o o o o o    |     |    -- coverH
	# #             ---------------------    --   --
	# #             |-------Bsec------|
	# #             |---| coverB  |---|
	# #
	# #                       y
	# #                       ^
	# #                       |    
	# #             ---------------------
	# #             |\      cover        /|
	# #             | \------Top------/ |
	# #             |c|                   |c|
	# #             |o|                   |o|
	# #  z <-----|v|       core      |v|  HSec
	# #             |e|                   |e|
	# #             |r|                    |r|
	# #             | /-------Bot------\ |
	# #             |/      cover        \|
	# #             ---------------------
	# #                       Bsec
	# #    
	# #
	# # Notes
	# #    The core concrete ends at the NA of the reinforcement
	# #    The center of the section is at (0,0) in the local axis system
	# # 

	};	# end of fibersection definition
};		# end of procedure

