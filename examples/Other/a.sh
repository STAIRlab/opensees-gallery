#!/bin/bash
#


ls $@ | grep -v -e "Proc.*" -e '.*FrictionPendulum.*' -e lasticPileSection.tcl -e Dispwall1-cg.tcl -e Dynamic.EQ.Uniform_LimitState.tcl -e Ex[68].genericFrame[23]D.build'\.' -e "Lib.*" -e TestSlider -e "Read.*" -e "Ex.*\.analyze\..*" -e "^PUL.*" -e "CenterCol[A-Z]" -e '.*_input_.*'  -e Tags.tcl -e 'NRHA_IR.tcl' -e 'NR94cnp.tcl' | while read i; do
echo $i
done

