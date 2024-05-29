mkdir -p out/
record="$HOME/packages/quakeio/dat/58658_007_20210426_10.09.54.P.zip"
#time python -m opensees nonlinear.tcl $record out/
OpenSees nonlinear.tcl "" $record out/
