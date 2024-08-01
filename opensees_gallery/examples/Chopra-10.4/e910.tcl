timeSeries Path 1 -dt 0.02 -filePath tabasFN.txt -factor $g
timeSeries Path 2 -dt 0.02 -filePath tabasFP.txt -factor $g

pattern MultipleSupport 1 {
   groundMotion 1 Plain -accel 1
   imposedMotion 1 1 1 ;# node, dof, gmTag
   groundMotion 2 Plain -accel 2
   imposedMotion 3 1 2
}