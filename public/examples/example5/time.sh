


# for elem in forceBeamColumn; do
#   echo Original
#   time for i in $(seq 1 10); do 
#      python -m opensees Example5.tcl $elem;
#   done
# 
#   echo New
#   time for i in $(seq 1 10); do 
#      CRD="" python -m opensees Example5.tcl $elem;
#   done
# done

for elem in ForceFrame; do
  echo $elem
  time for i in $(seq 1 10); do 
     CRD="" python -m opensees Example5.tcl $elem;
  done
done

# ops=${OPENSEESRT_LIB/debug/local}
# time for i in $(seq 1 3); do OPENSEESRT_LIB=$ops CRD="" python -m opensees Example5.tcl; done
# time for i in $(seq 1 3); do OPENSEESRT_LIB=$ops python -m opensees Example5.tcl; done
