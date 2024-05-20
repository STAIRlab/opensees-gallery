set g 9810;
set GMtime [expr $dt*$TotalNumberOfSteps + 10.0];
 
#Define acceleration series
set accelSeries "Series -dt $dt -filePath $GMfile -factor [expr $Scalefact*$g]";
 
#Create load pattern
pattern UniformExcitation 3 1 -accel $accelSeries;

 
#Dynamic analysis
set dt_analysis 0.0001;
wipeAnalysis;
constraints Plain;
numberer RCM;
system UmfPack;
test NormDispIncr 1.0e-4 1000;
algorithm Newton;
integrator Newmark 0.5 0.25;
analysis Transient;
set NumSteps [expr round(($GMtime + 0.0)/$dt_analysis)];
analyze $NumSteps $dt_analysis;

#Output time at end of analysis	
set currentTime [getTime];
puts "The current time is: $currentTime";

wipe;