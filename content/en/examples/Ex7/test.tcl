
#foreach section {RCsec Wsec} {
foreach section {RCsec} {
#                   Dynamic.EQ.bidirect
  foreach analysis {
                    Static.Push
                  } {
#                   Static.Cycle
#                   Dynamic.EQ.Uniform
#                   Dynamic.EQ.multipleSupport
#                   Dynamic.sine.multipleSupport
    puts "\t$section \t $analysis"
    source Ex7.Frame3D.build.$section.tcl
    source Ex7.Frame3D.analyze.$analysis.tcl

  }
}
