source LibUnits.tcl

foreach model {
    Ex9a.build.UniaxialSection2D.tcl
    Ex9b.build.WSection2D.tcl
    Ex9c.build.RectUnconfinedSymm2D.tcl
    Ex9d.build.RectConfinedSymm2D.tcl
    Ex9e.build.Rect2D.tcl
    Ex9f.build.Circ2D.tcl
  } {
    wipe
    puts "Model: $model"
    source $model
    source Ex9.analyze.MomentCurvature2D.tcl
}


foreach model {
    Ex9a.build.UniaxialSection3D.tcl
    Ex9b.build.WSection3D.tcl
    Ex9c.build.RectUnconfinedSymm3D.tcl
    Ex9d.build.RectConfinedSymm3D.tcl
    Ex9e.build.Rect3D.tcl
    Ex9f.build.Circ3D.tcl
    Ex9g.build.HollowSection3D.tcl
  } {
    wipe
    puts "Model: $model"
    source $model
    source Ex9.analyze.MomentCurvature3D.tcl
}
