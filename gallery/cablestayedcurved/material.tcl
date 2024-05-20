#model basic -ndm 3 -ndf 6
#============================================================
#puts "钢筋的材料参数"
set HRB235(1)      1;              
set HRB235(2)      235.0e3;         # Yield stress
set HRB235(3)      2.1e8;           # Young's modulus
set HRB235(4)      0.005;  		#hardening ratio
uniaxialMaterial Steel01  $HRB235(1)  $HRB235(2) $HRB235(3) $HRB235(4)    
#------------------------------------------------------------
#The element of the vector HRB335 is Tag,Yield stress,Young's modulus and strenth hardening,respectively
#global HRB335(1)
set HRB335(1)      2;             
set HRB335(2)      335.0e3;         # Yield stress
set HRB335(3)      2.0e8;           # Young's modulus
set HRB335(4)      0.005;  		#hardening ratio
uniaxialMaterial Steel01  $HRB335(1)  $HRB335(2) $HRB335(3) $HRB335(4)      
#------------------------------------------------------------
#The element of the vector HRB335 is Tag,Yield stress,Young's modulus and strenth hardening,respectively
#global HRB335(1)
set HRB400(1)      3;             
set HRB400(2)      400.0e3;         # Yield stress
set HRB400(3)      2.0e8;           # Young's modulus
set HRB400(4)      0.005;  		#hardening ratio
uniaxialMaterial Steel01  $HRB400(1)  $HRB400(2) $HRB335(3) $HRB400(4)                                                        
#************************************************************

#============================================================
#puts "普通混凝土C40的材料参数"
#------------------------------------------------------------
# The element of the vector C40_Cover is Tag,cfy,cdy,cfu,cdu, E respectively
#global C40_Cover(1)
set C40_Cover(1)      11;
set C40_Cover(2)     -18400;        #-26800
set C40_Cover(3)     -0.0020;
set C40_Cover(4)     [expr 0.2*$C40_Cover(2)];
set C40_Cover(5)     -0.0035;  
set C40_Cover(6)      3.25e7                                                         
uniaxialMaterial Concrete01 $C40_Cover(1)  $C40_Cover(2)    $C40_Cover(3)     $C40_Cover(4)     $C40_Cover(5)    
#************************************************************


#============================================================
#puts "普通混凝土C50的材料参数"
#------------------------------------------------------------
#global C50_Cover(1)
set C50_Cover(1)      13;
set C50_Cover(2)     -32400;
set C50_Cover(3)     -0.002;
set C50_Cover(4)     [expr 0.2*$C50_Cover(2)];
set C50_Cover(5)     -0.0035; 
set C50_Cover(6)     3.45e7                                                             
uniaxialMaterial Concrete01 $C50_Cover(1)  $C50_Cover(2)    $C50_Cover(3)     $C50_Cover(4)     $C50_Cover(5)      
#************************************************************


#============================================================
#puts "边墩核心混凝土C40的材料参数"
#------------------------------------------------------------
#global C40_Core(1)
set C40_Core(1)      12; 
set C40_Core(2)     -24400;            
set C40_Core(3)     -0.004;
set C40_Core(4)     [expr 0.2*$C40_Core(2)];
set C40_Core(5)     -0.016; 
set C40_Core(6)     3.25e7;            #E                                                             
uniaxialMaterial Concrete01 $C40_Core(1)  $C40_Core(2)    $C40_Core(3)    $C40_Core(4)    $C40_Core(5)        
#************************************************************

#============================================================
#puts "主塔核心混凝土C50的材料参数"
#------------------------------------------------------------
#global C50_Core(1)
set C50_Core(1)       14; 
set C50_Core(2)      -36500;            
set C50_Core(3)      -0.0022; 
set C50_Core(4)      [expr 0.2*$C50_Core(2)];
set C50_Core(5)      -0.016;  
set C50_Core(6)      3.45e7                                                           
uniaxialMaterial Concrete01 $C50_Core(1)   $C50_Core(2)     $C50_Core(3)      $C50_Core(4)      $C50_Core(5)      
#************************************************************

#set coreT1 101
#set coverT1 102
#
#uniaxialMaterial Concrete01 $coreT1 -16685 	-0.005	-14665	-0.0157
#uniaxialMaterial Concrete01 $coverT1 -13000	-0.002	-11416	-0.004
#













   