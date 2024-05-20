
source material.tcl
proc Circle {SecTag Diameter a row delta fiberWidth Cover Core Bar}  {



	#Diameter is the diameter of the circle section.
	#a is the cover thickness of the concrete, row is the reinforcement percentage. 
	#Cover,Core,Bar are of their Tags, which can be found in the material.tcl file
	#delta is the distance between adjancent bars
	#fiberWidth is the width of the discreted concrete fiber

	set totAs	[expr 3.14*$Diameter*$Diameter*$row/4.0]
	set Nbar	[expr int(3.14*($Diameter-2*$a)/double($delta))]
	set As	[expr $totAs/double($Nbar)]
	set NRadia	[expr int($Diameter/(2*double($delta)))+1] 
	set NCirc	[expr int(3.14*$Diameter/double($delta))+1]
	set d		[expr (4*$As/3.14)**0.5]      
	
 	section Fiber $SecTag -GJ 1e8 {
      	
      	patch circ $Cover $NCirc 	1 	      0.0 0.0 [expr ($Diameter/2.0-$a)] 	[expr $Diameter/2.0] 0 360;
      	patch circ $Core 	$NCirc	$NRadia 	0.0 0.0 0 					[expr $Diameter/2.0-$a] 0 360;
		layer circ $Bar 	$Nbar 	$As 	      0.0 0.0 [expr $Diameter/2.0-$a-$d/2.0] 0 360;

 	} 
}



proc Rect {SecTag L W a row delta fiberWidth Cover Core Bar}  {
	#L W are the length and width of the rectangle section.
	#a is the cover thickness of the concrete, row is the reinforcement percentage. 
	#Cover,Core,Bar are of their Tags, which can be found in the material.tcl file
	#NumY-number of subvision along local y direction 
	#NumZ-number of subvison along local z direction
	                                 

#                             z（纵向）
#                               ^                                
#	#             ___________ |______________
#	#           |             |              |  
#	#           |             |              |
#	#           |             |              |  W
#	#           |             |              |
#	#        ---|---- --------|--------- --- |----> y（横向）
#	#           |             |              |
#	#           |             |              |
#	#           |             |              |         
#	#           |_____________|______________| 
#	#                         |   L
#	#                         |

 	set Area    [expr $L*$W]
	set totAs	[expr $Area*$row]
	set Ntot	[expr int(2*($L+$W-4*$a)/double($delta))]
	set As	[expr $totAs/double($Ntot)]
	set d		[expr (4*$As/3.14)**0.5]
	set NBary	[expr int(($L-2*$a)/double($delta))+1]  
	set NBarz	[expr int(($W-2*$a)/double($delta))+1]
	set NumY	[expr int(($L-2*$a)/double($fiberWidth))+1]
	set NumZ	[expr int(($W-2*$a)/double($fiberWidth))+1]                                              

	set y1       [expr $L/2.0]
 	set z1       [expr $W/2.0]
 	set y2       [expr $L/2.0-$a]
 	set z2       [expr $W/2.0-$a]
 	#************************************************************ 
	
	
 	section Fiber $SecTag -GJ 1e8 {
		#************************************************************
		#Create the concrete cover fibers (top, bottom, left, right) 
		#The material Tag of the C40 is defined as $C40_Cover(1), seen in the material.tcl
      	patch rect $Cover $NumY 	1 	-$y2 	$z2  	$y2  	$z1
      	patch rect $Cover $NumY 	1 	-$y2 	-$z1 	$y2 	-$z2
      	patch rect $Cover 1 	$NumZ		-$y1 	-$z1 	-$y2 	$z1
     		patch rect $Cover 1	$NumZ   	$y2 	-$z1 	$y1 	$z1
 		#************************************************************

 		# The material Tag of the C40 is defined as $C40_Core(1), seen in the material.tcl
 		#************************************************************
      	patch rect $Core $NumY $NumZ  -$y2 -$z2 $y2 $z2
 		#************************************************************   
     
		# Create the reinforcing fibers 
 		#************************************************************	 
      	layer straight $Bar $NBary $As [expr -($y2-$d/2.0)] [expr ($z2-$d/2.0)]  [expr ($y2-$d/2.0)] [expr ($z2-$d/2.0)]
		layer straight $Bar $NBary $As [expr -($y2-$d/2.0)] [expr -($z2-$d/2.0)]  [expr ($y2-$d/2.0)] [expr -($z2-$d/2.0)]
            layer straight $Bar $NBarz $As [expr -($y2-$d/2.0)] [expr -($z2-$d/2.0-$delta)]  [expr -($y2-$d/2.0)] [expr ($z2-$d/2.0-$delta)]
		layer straight $Bar $NBarz $As [expr  ($y2-$d/2.0)] [expr -($z2-$d/2.0-$delta)]  [expr ($y2-$d/2.0)] [expr ($z2-$d/2.0-$delta)]
 		#************************************************************
 	}  
}

#####################################################################################################################################
proc Rect1Hole {SecTag L W L1 W1 a row delta fiberWidth Cover Core Bar}  {
	#L W are the length and width of the rectangle section.
	#a is the cover thickness of the concrete, row is the reinforcement percentage. 
	#Cover,Core,Bar are of their Tags, which can be found in the material.tcl file
	#NumY-number of subvision along local y direction 
	#NumZ-number of subvison along local z direction
	                                 

#                             z（纵向）
#                               ^                                
	#             ___________ |______________
	#           |             |              |  
	#           |         W1  |              |
	#           |     —————————      |  W
	#           |     |       |       |   L1 |
	#        ---|---- |-------|----- -|--- - |----> y（横向）
	#           |     |       |       |      |
	#           |     |----------------      |       
	#           |             |              |         
	#           |_____________|______________| 
	#                         |   L
	#                         |

 	set Area    [expr $L*$W-($L-2*$L1)*($W-2*$W1)]
	set totAs	[expr $Area*$row]
	set Ntot	[expr int((3*$L+3*$W-2*$L1-2*$W1)/double($delta))]
	set As	[expr $totAs/double($Ntot)]
	set As1	[expr $As/2.0]
	set d		[expr (4*$As/3.14)**0.5]
	set d1	[expr (4*$As1/3.14)**0.5]
	set NBary	[expr int(($L-2*$a)/double($delta))+1]  
	set NBarz	[expr int(($W-2*$a)/double($delta))+1] 
	set NBary1	[expr int(($L-2*$L1)/double($delta))+1]  
	set NBarz1	[expr int(($W-2*$W1)/double($delta))+1]
	set Numy	[expr int($L/double($fiberWidth))+1]
	set Numz	[expr int($W/double($fiberWidth))+1]
	set Numy1	[expr int($L1/double($fiberWidth))+1]
	set Numz1	[expr int($W1/double($fiberWidth))+1]
	set Numy2	[expr int(($L-2*$L1)/double($fiberWidth))]                                             

	set y1       [expr $L/2.0]
 	set z1       [expr $W/2.0]
 	set y2       [expr $L/2.0-$a]
 	set z2       [expr $W/2.0-$a]
	set y3	 [expr $L/2.0-$L1]
	set z3	 [expr $W/2.0-$W1]
 	#************************************************************ 
	
	
 	section Fiber $SecTag -GJ 1e8 {
		#************************************************************
		#Create the concrete cover fibers (top, bottom, left, right) 
		#The material Tag of the C40 is defined as $C40_Cover(1), seen in the material.tcl
      	patch rect $Cover $Numy 	1 	-$y2 	$z2  	$y2  	$z1
      	patch rect $Cover $Numy 	1 	-$y2 	-$z1 	$y2 	-$z2
      	patch rect $Cover 1 	$Numz		-$y1 	-$z1 	-$y2 	$z1
     		patch rect $Cover 1	$Numz   	 $y2 	-$z1 	$y1 	$z1
 		#************************************************************

 		# The material Tag of the C40 is defined as $C40_Core(1), seen in the material.tcl
 		#************************************************************
      	patch rect $Core $Numy2 $Numz1  -$y3  $z3 $y3 $z2
		patch rect $Core $Numy2 $Numz1  -$y3 -$z2 $y3 -$z3
		patch rect $Core $Numy1 $Numz  -$y2 -$z2 -$y3  $z2
		patch rect $Core $Numy1 $Numz   $y3 -$z2  $y2  $z2

 		#************************************************************   
     
		# Create the reinforcing fibers 
 		#************************************************************	 
      	layer straight $Bar $NBary $As [expr -($y2-$d/2.0)] [expr ($z2-$d/2.0)]  [expr ($y2-$d/2.0)] [expr ($z2-$d/2.0)]
		layer straight $Bar $NBary $As [expr -($y2-$d/2.0)] [expr -($z2-$d/2.0)]  [expr ($y2-$d/2.0)] [expr -($z2-$d/2.0)]
            layer straight $Bar $NBarz $As [expr -($y2-$d/2.0)] [expr -($z2-$d/2.0-$delta)]  [expr -($y2-$d/2.0)] [expr ($z2-$d/2.0-$delta)]
		layer straight $Bar $NBarz $As [expr  ($y2-$d/2.0)] [expr -($z2-$d/2.0-$delta)]  [expr ($y2-$d/2.0)] [expr ($z2-$d/2.0-$delta)]

		layer straight $Bar $NBary1 $As1 [expr -($y3)] [expr ($z3+$a)]  [expr ($y3)] [expr ($z3+$a)]
		layer straight $Bar $NBary1 $As1 [expr -($y3)] [expr -($z3+$a)]  [expr ($y3)] [expr -($z3+$a)]
            layer straight $Bar $NBarz1 $As1 [expr -($y3+$a)] [expr -($z3)]  [expr -($y3+$a)] [expr ($z3)]
		layer straight $Bar $NBarz1 $As1 [expr  ($y3+$a)] [expr -($z3)]  [expr ($y3+$a)] [expr ($z3)]
 		#************************************************************
 	}  
}

########################################################################################################################



proc Rect3Hole {SecTag L W L1 L2 L3 L4 L5 L6 L7 W1 a row delta fiberWidth Cover Core Bar}  {
	#L W are the length and width of the rectangle section.
	#a is the cover thickness of the concrete, row is the reinforcement percentage. 
	#Cover,Core,Bar are of their Tags, which can be found in the material.tcl file
	#NumY-number of subvision along local y direction 
	#NumZ-number of subvison along local z direction
	                                 

#                                      z（纵向）
##                                      ^                               
	#             ____________________|________________________
	#           |                     |                       |
	#           |       W1            |             	    |
	#           |   ---------     ---------     |---------    |                      
	#           |L1 |       | L3  |   |    | L5 |        | L7 |  L1              
	#        W--|---|------ |-----|---|----|----| - --- -|-----------> y（横向）
	#           |   |       |     |   |    |    |        |    |                  
	#           |   ---------     ---------     ---------|    |                            
	#           |      L2             |L4          L6         |              
	#           |_____________________________________________| 
	#                                 |   L
	#                                 |

 	set Area    [expr $L*$W-$L2*($W-2*$W1)-$L4*($W-2*$W1)-$L6*($W-2*$W1)]
	set totAs	[expr $Area*$row]
	set Ntot	[expr int((2*$L+2*$W+3*($W-2*$W1)+$L2+$L4+$L6)/double($delta))]
	set As	[expr $totAs/double($Ntot)]
	set As1	[expr $As/2.0]
	set d		[expr (4*$As/3.14)**0.5]
	set d1	[expr (4*$As1/3.14)**0.5]
	set NBary	[expr int(($L-2*$a)/double($delta))+1]  
	set NBarz	[expr int(($W-2*$a)/double($delta))+1] 
	set NBary1	[expr int(($L2)/double($delta))+1]
	set NBary2	[expr int(($L4)/double($delta))+1]
	set NBary3	[expr int(($L6)/double($delta))+1]  
	set NBarz1	[expr int(($W-2*$W1)/double($delta))+1]
	set Numy	[expr int($L/double($fiberWidth))+1]
	set Numz	[expr int($W/double($fiberWidth))+1]
	set Numy1	[expr int($L1/double($fiberWidth))+1]
	set Numy3	[expr int($L3/double($fiberWidth))+1]
	set Numy5	[expr int($L5/double($fiberWidth))+1]
	set Numy7	[expr int($L7/double($fiberWidth))+1]
	set Numz1	[expr int($W1/double($fiberWidth))+1]
	set Numz2	[expr int(($W-2*$W1)/double($fiberWidth))+1]                                             

	set y1       [expr $L/2.0]
 	set z1       [expr $W/2.0]
 	set y2       [expr $L/2.0-$a]
 	set z2       [expr $W/2.0-$a]
	set y3	 [expr $L4/2.0]
	set y4	 [expr $L4/2.0+$L3]
	set y5	 [expr $L4/2.0+$L3+$L2]
	set z3	 [expr ($W-2*$W1)/2.0]
 	#************************************************************ 
	
	
 	section Fiber $SecTag -GJ 1e8 {
		#************************************************************
		#Create the concrete cover fibers (top, bottom, left, right) 
		#The material Tag of the C40 is defined as $C40_Cover(1), seen in the material.tcl
      	patch rect $Cover $Numy 	1 	-$y2 	$z2  	$y2  	$z1
      	patch rect $Cover $Numy 	1 	-$y2 	-$z1 	$y2 	-$z2
      	patch rect $Cover 1 	$Numz		-$y1 	-$z1 	-$y2 	$z1
     		patch rect $Cover 1	$Numz   	$y2 	-$z1 	$y1 	$z1
 		#************************************************************

 		# The material Tag of the C40 is defined as $C40_Core(1), seen in the material.tcl
 		#************************************************************
      	patch rect $Core $Numy $Numz1  -$y2  $z3 $y2  $z2
		patch rect $Core $Numy $Numz1  -$y2 -$z2 $y2 -$z3
		patch rect $Core $Numy1 $Numz2 -$y2 -$z3 -$y5 $z3
		patch rect $Core $Numy3 $Numz2 -$y4 -$z3 -$y3 $z3
		patch rect $Core $Numy3 $Numz2  $y3 -$z3  $y4 $z3
		patch rect $Core $Numy3 $Numz2  $y5 -$z3  $y2 $z3

 		#************************************************************   
     
		# Create the reinforcing fibers 
 		#************************************************************	 
      	layer straight $Bar $NBary $As [expr -($y2-$d/2.0)] [expr ($z2-$d/2.0)]  [expr ($y2-$d/2.0)] [expr ($z2-$d/2.0)]
		layer straight $Bar $NBary $As [expr -($y2-$d/2.0)] [expr -($z2-$d/2.0)]  [expr ($y2-$d/2.0)] [expr -($z2-$d/2.0)]
            layer straight $Bar $NBarz $As [expr -($y2-$d/2.0)] [expr -($z2-$d/2.0-$delta)]  [expr -($y2-$d/2.0)] [expr ($z2-$d/2.0-$delta)]
		layer straight $Bar $NBarz $As [expr  ($y2-$d/2.0)] [expr -($z2-$d/2.0-$delta)]  [expr ($y2-$d/2.0)] [expr ($z2-$d/2.0-$delta)]

		layer straight $Bar $NBary1 $As1 [expr -($y5)] [expr ($z3+$a)]  [expr ($y4)] [expr ($z3+$a)]
		layer straight $Bar $NBary1 $As1 [expr -($y5)] [expr -($z3+$a)]  [expr ($y4)] [expr -($z3+$a)]
            layer straight $Bar $NBarz1 $As1 [expr -($y5+$a)] [expr -($z3)]  [expr -($y5+$a)] [expr ($z3)]
		layer straight $Bar $NBarz1 $As1 [expr -($y4-$a)] [expr -($z3)]  [expr -($y4-$a)] [expr ($z3)]

		layer straight $Bar $NBary1 $As1 [expr -($y3)] [expr ($z3+$a)]   [expr ($y3)] [expr ($z3+$a)]
		layer straight $Bar $NBary1 $As1 [expr -($y3)] [expr -($z3+$a)]  [expr ($y3)] [expr -($z3+$a)]
            layer straight $Bar $NBarz1 $As1 [expr -($y3+$a)] [expr -($z3)]  [expr -($y3+$a)] [expr ($z3)]
		layer straight $Bar $NBarz1 $As1 [expr  ($y3+$a)] [expr -($z3)]  [expr  ($y3+$a)] [expr ($z3)]


		layer straight $Bar $NBary1 $As1 [expr  ($y4)] [expr ($z3+$a)]   [expr ($y5)] [expr ($z3+$a)]
		layer straight $Bar $NBary1 $As1 [expr  ($y4)] [expr -($z3+$a)]  [expr ($y5)] [expr -($z3+$a)]
            layer straight $Bar $NBarz1 $As1 [expr ($y4-$a)] [expr -($z3)]  [expr ($y4-$a)] [expr ($z3)]
		layer straight $Bar $NBarz1 $As1 [expr  ($y5+$a)] [expr -($z3)]  [expr  ($y5+$a)] [expr ($z3)]



 		#************************************************************
 	}  
}
