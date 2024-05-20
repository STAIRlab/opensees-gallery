#
perf record --call-graph dwarf -- python -m opensees $1
perf script | stackcollapse-perf.pl > out.perf-folded
flamegraph.pl out.perf-folded > perf.svg
