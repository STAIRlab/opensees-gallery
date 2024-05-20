################################################---CableResponse---####################################################
#for {set i 1} {$i<=$CableEleN} {incr i 1} {
#	file mkdir CableResponse/CableForce/$EleCable($i)
#	set Cablettt $EleCable($i)
#	recorder Element 	-file CableResponse/CableForce/$Cablettt/1.out  -time -ele $EleCable($i) axialForce
#
#}
####################################################################################################################### 


###############################################---GirderNodeDisp---####################################################
for {set i 1} {$i<=$GirderNP} {incr i 1} {
	file mkdir GirderResponse/GirderNodeDisp/$NodeGirder($i)
	set GirderNodettt $NodeGirder($i)
	recorder Node -file GirderResponse/GirderNodeDisp/$GirderNodettt/1.out -time -node $NodeGirder($i) -dof 1 2 3 disp
}
#######################################################################################################################


#############################################---PylonNodeDisp---########################################################
set Data [open PylonNodesSet.txt r]
set var3 [split [read $Data]]
set PylonNodeSetN [expr  [llength $var3]]

for {set i 1} {$i<=$PylonNodeSetN} {incr i 1} {
	set Pylset($i)    [lindex	$var3	[expr ($i-1)]]
}
close $Data
#################################################################
for {set i 1} {$i<=$PylonNodeSetN} {incr i 1} {
	file mkdir PylonNodeDispSet/$Pylset($i)
	set Pynodettt $Pylset($i)
	recorder Node -file PylonNodeDispSet/$Pynodettt/1.out -time -node $Pylset($i) -dof 1 2 3 disp
}
########################################################################################################################


#############################################---PylonSectionResponse---################################################
#for {set i 1} {$i<=$PylonNEle} {incr i 1} {
#	file mkdir PylonSectMoment/$ElePylon($i)
#	recorder Element 	-file PylonSectMoment/$ElePylon($i)/1.out -time -ele $ElePylon($i) section 1 force
#}
######################################################################################################################

##############################################---GirderElementResponse---##############################################
#for {set i 1} {$i<=118} {incr i 1} {
#	file mkdir GirderMoment/$i
#	recorder Element 	-file  GirderMoment/$i/1.out -time -ele $i localForce
#}
########################################################################################################################

# recorder Element   -file LRB1Force/$WaveNumber.out      	 	-time -ele 1003 		localForce
# recorder Element	-file LRB1Disp/$WaveNumber.out      	 		-time -ele 1003 		deformation
# recorder Element   -file LRB2Force/$WaveNumber.out      	 	-time -ele 1013 		localForce 
# recorder Element	-file LRB2Disp/$WaveNumber.out      	 		-time -ele 1013 		deformation
# recorder Element   -file LRB3Force/$WaveNumber.out      	 	-time -ele 1014 		localForce
# recorder Element	-file LRB3Disp/$WaveNumber.out      	 		-time -ele 1014 		deformation
# recorder Element   -file LRB4Force/$WaveNumber.out      	 	-time -ele 1009 		localForce
# recorder Element	-file LRB4Disp/$WaveNumber.out      	 		-time -ele 1009 		deformation
# 
# recorder Element 	-file Backfill1Force/$WaveNumber.out		-time -ele  1001     	localForce	
# recorder Element   -file BackFill1DOF/$WaveNumber.out      	-time -ele 	1001 		deformation
# recorder Element 	-file Backfill2Force/$WaveNumber.out		-time -ele  1007     	localForce	
# recorder Element   -file BackFill2DOF/$WaveNumber.out      	-time -ele 	1007 		deformation
# 
# recorder Element 	-file Abut1PoundingForce/$WaveNumber.out			-time -ele  1002     	localForce
# recorder Element	-file Abut1PoundingDisp/$WaveNumber.out       		-time -ele 	1002 		deformation
# recorder Element 	-file Abut2PoundingForce/$WaveNumber.out			-time -ele  1008     	localForce
# recorder Element	-file Abut2PoundingDisp/$WaveNumber.out       		-time -ele 	1008 		deformation
#
# recorder Element 	-file Pylon300Moment/$WaveNumber.out		-time -ele 	300			section 1 force
# recorder Element	-file Pylon300Curature/$WaveNumber.out		-time -ele  300 	 	section 1 deformation
# recorder Element 	-file Pylon400Moment/$WaveNumber.out		-time -ele 	400			section 1 force
# recorder Element	-file Pylon400Curature/$WaveNumber.out		-time -ele  400 	 	section 1 deformation
# recorder Element 	-file Pylon313Moment/$WaveNumber.out		-time -ele 	313			section 1 force
# recorder Element	-file Pylon313Curature/$WaveNumber.out		-time -ele  313 	 	section 1 deformation
# recorder Element 	-file Pylon413Moment/$WaveNumber.out		-time -ele 	413			section 1 force
# recorder Element	-file Pylon413Curature/$WaveNumber.out		-time -ele  413 	 	section 1 deformation
#
# recorder Node   	-file Pylon1topDOF/$WaveNumber.out       	-time -node 376 		-dof    1 2 disp
# recorder Node   	-file Pylon2topDOF/$WaveNumber.out       	-time -node 476 		-dof    1 2 disp
# recorder Node   	-file Girder48DOF/$WaveNumber.out       	-time -node 48 			-dof    1 2 disp
# recorder Node   	-file Girder190DOF/$WaveNumber.out       	-time -node 190 		-dof    1 2 disp
# 
# for {set i 1} {$i<=136} {incr i 1} {
#	recorder Element 	-file CableForce/$EleCable($i)/$WaveNumber.out		-time -ele 	$EleCable($i)		axialForce
#	recorder Element 	-file CableDOF/$EleCable($i)/$WaveNumber.out		-time -ele 	$EleCable($i)		deformations
#}
#
#