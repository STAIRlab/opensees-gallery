# --------------------------------------------------------------------------------------------------
# Example 2. 2D cantilever column, static pushover
# fiber section, nonlinearBeamColumn element
#			Silvia Mazzoni & Frank McKenna, 2006
#
#   ^Y
#   |
#   2       ___
#   |        | 
#   |        |
#   |        |
#  (1)     LCol
#   |        |
#   |        |
#   |        |
#  =1=------_|_-------->X
#

# SET UP ----------------------------------------------------------------------------
# units: kip, inch, sec
wipe;					# clear memory of all past model definitions
file mkdir Data; 				# create data directory
model BasicBuilder -ndm 2 -ndf 3;		# Define the model builder, ndm=#dimension, ndf=#dofs


# define GEOMETRY -------------------------------------------------------------
set LCol 432; 		# column length
set Weight 2000.; 		# superstructure weight
# define section geometry
set HCol 60; 		# Column Depth
set BCol 60;		# Column Width

# calculated parameters
set PCol $Weight; 		# nodal dead-load weight per column
set g 386.4;			# g.
set Mass [expr $PCol/$g];		# nodal mass
# calculated geometry parameters
set ACol [expr $BCol*$HCol];					# cross-sectional area
set IzCol [expr 1./12.*$BCol*pow($HCol,3)]; 			# Column moment of inertia

# nodal coordinates:
node 1 0 0;			# node#, X, Y
node 2 0 $LCol 		

# Single point constraints -- Boundary Conditions
fix 1 1 1 1; 			# node DX DY RZ

# nodal masses:
mass 2 $Mass  1e-9 0.;		# node#, Mx My Mz, Mass=Weight/g, neglect rotational inertia at nodes

# Define ELEMENTS & SECTIONS -------------------------------------------------------------
set ColSecTag 1;			# assign a tag number to the column section	
# define section geometry
set coverCol 5.;			# Column cover to reinforcing steel NA.
set numBarsCol 5;			# number of longitudinal-reinforcement bars in each side of column section. (symmetric top & bot)
set barAreaCol 2.25 ;		# area of longitudinal-reinforcement bars


# MATERIAL parameters -------------------------------------------------------------------
set IDconcU 1; 			# material ID tag -- unconfined cover concrete
set IDreinf 2; 				# material ID tag -- reinforcement
# nominal concrete compressive strength
set fc -4.; 				# CONCRETE Compressive Strength (+Tension, -Compression)
set Ec [expr 57*sqrt(-$fc*1000)]; 		# Concrete Elastic Modulus (the term in sqr root needs to be in psi
# unconfined concrete
set fc1U 		$fc;			# UNCONFINED concrete (todeschini parabolic model), maximum stress
set eps1U	-0.003;			# strain at maximum strength of unconfined concrete
set fc2U 		[expr 0.2*$fc1U];		# ultimate stress
set eps2U	-0.01;			# strain at ultimate stress
set lambda 0.1;				# ratio between unloading slope at $eps2 and initial slope $Ec
# tensile-strength properties
set ftU [expr -0.14*$fc1U];			# tensile strength +tension
set Ets [expr $ftU/0.002];			# tension softening stiffness
# -----------
set Fy 66.8;				# STEEL yield stress
set Es 29000.;				# modulus of steel
set Bs 0.01;				# strain-hardening ratio 
set R0 18;				# control the transition from elastic to plastic branches
set cR1 0.925;				# control the transition from elastic to plastic branches
set cR2 0.15;				# control the transition from elastic to plastic branches
uniaxialMaterial Concrete02 $IDconcU $fc1U $eps1U $fc2U $eps2U $lambda $ftU $Ets;	# build cover concrete (unconfined)
uniaxialMaterial Steel02 $IDreinf $Fy $Es $Bs $R0 $cR1 $cR2;				# build reinforcement material

# FIBER SECTION properties -------------------------------------------------------------
# symmetric section
#                        y
#                        ^
#                        |     
#             ---------------------     --   --
#             |   o     o     o    |     |    -- cover
#             |                       |     |
#             |                       |     |
#    z <--- |          +           |     H
#             |                       |     |
#             |                       |     |
#             |   o     o     o    |     |    -- cover
#             ---------------------     --   --
#             |-------- B --------|
#
# RC section: 
   set coverY [expr $HCol/2.0];	# The distance from the section z-axis to the edge of the cover concrete -- outer edge of cover concrete
   set coverZ [expr $BCol/2.0];	# The distance from the section y-axis to the edge of the cover concrete -- outer edge of cover concrete
   set coreY [expr $coverY-$coverCol]
   set coreZ [expr $coverZ-$coverCol]
   set nfY 16;			# number of fibers for concrete in y-direction
   set nfZ 4;			# number of fibers for concrete in z-direction
   section fiberSec $ColSecTag -GJ 1e8 {; # Define the fiber section
	patch quadr $IDconcU $nfZ $nfY -$coverY $coverZ -$coverY -$coverZ $coverY -$coverZ $coverY $coverZ; 	# Define the concrete patch
	layer straight $IDreinf $numBarsCol $barAreaCol -$coreY $coreZ -$coreY -$coreZ;	# top layer reinfocement
	layer straight $IDreinf $numBarsCol $barAreaCol  $coreY $coreZ  $coreY -$coreZ;	# bottom layer reinforcement
    };	# end of fibersection definition

# define geometric transformation: performs a linear geometric transformation of beam stiffness and resisting force from the basic system to the global-coordinate system
set ColTransfTag 1; 			# associate a tag to column transformation
geomTransf Linear $ColTransfTag  ; 	

# element connectivity:
set numIntgrPts 5;								# number of integration points for force-based element
element nonlinearBeamColumn 1 1 2 $numIntgrPts $ColSecTag $ColTransfTag;	# self-explanatory when using variables

# Define RECORDERS -------------------------------------------------------------
recorder Node    -file Data/Ex2cPush-DFree.out -time -node 2 -dof 1 2 3 disp;		# displacements of free nodes
recorder Node    -file Data/Ex2cPush-DBase.out -time -node 1 -dof 1 2 3 disp;		# displacements of support nodes
recorder Node    -file Data/Ex2cPush-RBase.out -time -node 1 -dof 1 2 3 reaction;		# support reaction
recorder Drift   -file Data/Ex2cPush-Drift.out -time -iNode 1 -jNode 2 -dof 1   -perpDirn 2 ;	# lateral drift
recorder Element -file Data/Ex2cPush-FCol.out  -time -ele 2 globalForce;						# element forces -- column
recorder Element -file Data/Ex2cPush-ForceColSec1.out -time -ele 1 section 1 force;				# Column section forces, axial and moment, node i
recorder Element -file Data/Ex2cPush-DefoColSec1.out -time -ele 1 section 1 deformation;				# section deformations, axial and curvature, node i
recorder Element -file Data/Ex2cPush-ForceColSec$numIntgrPts.out -time -ele 1 section $numIntgrPts force;		# section forces, axial and moment, node j
recorder Element -file Data/Ex2cPush-DefoColSec$numIntgrPts.out  -time -ele 1 section 1 deformation;		# section deformations, axial and curvature, node j


# define GRAVITY -------------------------------------------------------------
pattern Plain 1 Linear {
   load 2 0 -$PCol 0
}

# Gravity-analysis parameters -- load-controlled static analysis
set Tol 1.0e-8;			# convergence tolerance for test
constraints Plain;     		# how it handles boundary conditions
numberer Plain;			# renumber dof's to minimize band-width (optimization), if you want to
system BandGeneral;		# how to store and solve the system of equations in the analysis
test NormDispIncr $Tol 6 ; 		# determine if convergence has been achieved at the end of an iteration step
algorithm Newton;			# use Newton's solution algorithm: updates tangent stiffness at every iteration
set NstepGravity 10;  		# apply gravity in 10 steps
set DGravity [expr 1./$NstepGravity]; 	# first load increment;
integrator LoadControl $DGravity;	# determine the next time step for an analysis
analysis Static;			# define type of analysis static or transient
analyze $NstepGravity;		# apply gravity
# ------------------------------------------------- maintain constant gravity loads and reset time to zero
loadConst -time 0.0

puts "Model Built"

# STATIC PUSHOVER ANALYSIS --------------------------------------------------------------------------------------------------
#
# we need to set up parameters that are particular to the model.
set IDctrlNode 2;			# node where displacement is read for displacement control
set IDctrlDOF 1;			# degree of freedom of displacement read for displacement contro
set Dmax [expr 0.01*$LCol];		# maximum displacement of pushover. push to 10% drift.
set Dincr [expr 0.001*$LCol];		# displacement increment for pushover. you want this to be very small, but not too small to slow down the analysis

# create load pattern for lateral pushover load
set Hload $Weight;				# define the lateral load as a proportion of the weight so that the pseudo time equals the lateral-load coefficient when using linear load pattern
pattern Plain 200 Linear {;			# define load pattern -- generalized
	load 2 $Hload 0.0 0.0 0.0 0.0 0.0;	# define lateral load in static lateral analysis
}

# ----------- set up analysis parameters
# CONSTRAINTS handler -- Determines how the constraint equations are enforced in the analysis (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/617.htm)
#          Plain Constraints -- Removes constrained degrees of freedom from the system of equations (only for homogeneous equations)
#          Lagrange Multipliers -- Uses the method of Lagrange multipliers to enforce constraints 
#          Penalty Method -- Uses penalty numbers to enforce constraints --good for static analysis with non-homogeneous eqns (rigidDiaphragm)
#          Transformation Method -- Performs a condensation of constrained degrees of freedom 
constraints Plain;		

# DOF NUMBERER (number the degrees of freedom in the domain): (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/366.htm)
#   determines the mapping between equation numbers and degrees-of-freedom
#          Plain -- Uses the numbering provided by the user 
#          RCM -- Renumbers the DOF to minimize the matrix band-width using the Reverse Cuthill-McKee algorithm 
numberer Plain

# SYSTEM (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/371.htm)
#   Linear Equation Solvers (how to store and solve the system of equations in the analysis)
#   -- provide the solution of the linear system of equations Ku = P. Each solver is tailored to a specific matrix topology. 
#          ProfileSPD -- Direct profile solver for symmetric positive definite matrices 
#          BandGeneral -- Direct solver for banded unsymmetric matrices 
#          BandSPD -- Direct solver for banded symmetric positive definite matrices 
#          SparseGeneral -- Direct solver for unsymmetric sparse matrices 
#          SparseSPD -- Direct solver for symmetric sparse matrices 
#          UmfPack -- Direct UmfPack solver for unsymmetric matrices 
system BandGeneral

# TEST: # convergence test to 
# Convergence TEST (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/360.htm)
#   -- Accept the current state of the domain as being on the converged solution path 
#   -- determine if convergence has been achieved at the end of an iteration step
#          NormUnbalance -- Specifies a tolerance on the norm of the unbalanced load at the current iteration 
#          NormDispIncr -- Specifies a tolerance on the norm of the displacement increments at the current iteration 
#          EnergyIncr-- Specifies a tolerance on the inner product of the unbalanced load and displacement increments at the current iteration 
set Tol 1.e-8;                        # Convergence Test: tolerance
set maxNumIter 6;                # Convergence Test: maximum number of iterations that will be performed before "failure to converge" is returned
set printFlag 0;                # Convergence Test: flag used to print information on convergence (optional)        # 1: print information on each step; 
set TestType EnergyIncr ;	# Convergence-test type
test $TestType $Tol $maxNumIter $printFlag;

# Solution ALGORITHM: -- Iterate from the last time step to the current (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/682.htm)
#          Linear -- Uses the solution at the first iteration and continues 
#          Newton -- Uses the tangent at the current iteration to iterate to convergence 
#          ModifiedNewton -- Uses the tangent at the first iteration to iterate to convergence 
set algorithmType Newton
algorithm $algorithmType;        

# Static INTEGRATOR: -- determine the next time step for an analysis  (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/689.htm)
#          LoadControl -- Specifies the incremental load factor to be applied to the loads in the domain 
#          DisplacementControl -- Specifies the incremental displacement at a specified DOF in the domain 
#          Minimum Unbalanced Displacement Norm -- Specifies the incremental load factor such that the residual displacement norm in minimized 
#          Arc Length -- Specifies the incremental arc-length of the load-displacement path 
# Transient INTEGRATOR: -- determine the next time step for an analysis including inertial effects 
#          Newmark -- The two parameter time-stepping method developed by Newmark 
#          HHT -- The three parameter Hilbert-Hughes-Taylor time-stepping method 
#          Central Difference -- Approximates velocity and acceleration by centered finite differences of displacement 
integrator DisplacementControl  $IDctrlNode   $IDctrlDOF $Dincr

# ANALYSIS  -- defines what type of analysis is to be performed (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/324.htm)
#          Static Analysis -- solves the KU=R problem, without the mass or damping matrices. 
#          Transient Analysis -- solves the time-dependent analysis. The time step in this type of analysis is constant. The time step in the output is also constant. 
#          variableTransient Analysis -- performs the same analysis type as the Transient Analysis object. The time step, however, is variable. This method is used when 
#                 there are convergence problems with the Transient Analysis object at a peak or when the time step is too small. The time step in the output is also variable.
analysis Static

#  ---------------------------------    perform Static Pushover Analysis
set Nsteps [expr int($Dmax/$Dincr)];        # number of pushover analysis steps
set ok [analyze $Nsteps];                # this will return zero if no convergence problems were encountered

# ---------------------------------- in case of convergence problems
if {$ok != 0} {      
# change some analysis parameters to achieve convergence
# performance is slower inside this loop
	set ok 0;
	set controlDisp 0.0;		# start from zero
	set D0 0.0;		# start from zero
	set Dstep [expr ($controlDisp-$D0)/($Dmax-$D0)]
	while {$Dstep < 1.0 && $ok == 0} {	
		set controlDisp [nodeDisp $IDctrlNode $IDctrlDOF ]
		set Dstep [expr ($controlDisp-$D0)/($Dmax-$D0)]
		set ok [analyze 1 ]
		if {$ok != 0} {
			puts "Trying Newton with Initial Tangent .."
			test NormDispIncr   $Tol 2000  0
			algorithm Newton -initial
			set ok [analyze 1 ]
			test $TestType $Tol $maxNumIter  0
			algorithm $algorithmType
		}
		if {$ok != 0} {
			puts "Trying Broyden .."
			algorithm Broyden 8
			set ok [analyze 1 ]
			algorithm $algorithmType
		}
		if {$ok != 0} {
			puts "Trying NewtonWithLineSearch .."
			algorithm NewtonLineSearch .8
			set ok [analyze 1 ]
			algorithm $algorithmType
		}
	}
	};      # end if ok !0

puts "Pushover Complete, Tip displacement: \n\t[nodeDisp 2]"
return $ok

