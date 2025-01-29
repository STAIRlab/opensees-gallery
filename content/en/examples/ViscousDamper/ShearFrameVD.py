"""
Example Python script translating the original Tcl input for a 
Single-Story Shear Frame with a Nonlinear Viscous Damper using openseesrt.

All units are in mm, KN, and seconds.
"""

import math
from pathlib import Path

import opensees.openseespy as ops

def main():

    #-----------------------------------------------------------------------------
    # 1. Define model (ndm=2, ndf=3)
    #-----------------------------------------------------------------------------
    model = ops.Model(2, 3)  # matches `model BasicBuilder -ndm 2 -ndf 3` in Tcl

    #-----------------------------------------------------------------------------
    # 2. Create data directory using pathlib
    #-----------------------------------------------------------------------------
    output_dir = Path("Output")
    output_dir.mkdir(parents=True, exist_ok=True)

    #-----------------------------------------------------------------------------
    # 3. Define geometry
    #-----------------------------------------------------------------------------
    L = 5000.0  # bay width (mm)
    h = 3000.0  # story height (mm)

    #-----------------------------------------------------------------------------
    # 4. Define nodal coordinates
    #-----------------------------------------------------------------------------
    model.node(1, 0.0, 0.0)
    model.node(2,  L,  0.0)
    model.node(3, 0.0,  h )
    model.node(4,  L,   h )

    #-----------------------------------------------------------------------------
    # 5. Single point constraints (fixities)
    #-----------------------------------------------------------------------------
    model.fix(1, 1, 1, 1)
    model.fix(2, 1, 1, 1)

    #-----------------------------------------------------------------------------
    # 6. MP constraints (equalDOF)
    #-----------------------------------------------------------------------------
    model.equalDOF(3, 4, 2, 3)

    #-----------------------------------------------------------------------------
    # 7. Mass assignment
    #-----------------------------------------------------------------------------
    W = 1000.0      # KN
    g = 9810.0      # mm/s^2
    m = W / g       # mass in consistent units

    model.mass(3, 0.5*m, 0.0, 0.0)
    model.mass(4, 0.5*m, 0.0, 0.0)

    #-----------------------------------------------------------------------------
    # 8. Basic structural parameters
    #-----------------------------------------------------------------------------
    Tn = 0.7
    pi = math.acos(-1.0)

    K = (2.0 * pi / Tn)**2 * m  # KN/mm
    E = 200.0                  # KN/mm^2
    Ic = (K * (h**3)) / (24.0 * E)
    Ib = 1.0e12 * Ic
    A  = 1.0e12

    #-----------------------------------------------------------------------------
    # 9. Damper properties
    #-----------------------------------------------------------------------------
    Kd = 25.0
    Cd = 20.7452
    ad = 0.35

    # uniaxialMaterial ViscousDamper 1 Kd Cd ad
    model.uniaxialMaterial("ViscousDamper", 1, Kd, Cd, ad)

    #-----------------------------------------------------------------------------
    # 10. Geometric transformation
    #-----------------------------------------------------------------------------
    transfTag = 1
    model.geomTransf("Linear", transfTag)

    #-----------------------------------------------------------------------------
    # 11. Define Elements
    #-----------------------------------------------------------------------------
    # element elasticBeamColumn tag iNode jNode A E I transfTag
    model.element("elasticBeamColumn", 1, 1, 3, A, E, Ic, transfTag)
    model.element("elasticBeamColumn", 2, 2, 4, A, E, Ic, transfTag)
    model.element("elasticBeamColumn", 3, 3, 4, A, E, Ib, transfTag)

    # element twoNodeLink tag iNode jNode -mat 1 -dir 1
    model.element("twoNodeLink", 4, 1, 4, mat=1, dir=1)

    print("Model Built")

    #-----------------------------------------------------------------------------
    # 12. Time series & pattern
    #-----------------------------------------------------------------------------
    # timeSeries Path 1 -dt 0.01 -filePath TakY.th -factor 0.50*g
    model.timeSeries("Path", 1, dt=0.01, filePath="TakY.th", factor=0.50*g)

    # pattern UniformExcitation 1 1 -accel 1
    model.pattern("UniformExcitation", 1, 1, accel=1)

    #-----------------------------------------------------------------------------
    # 13. Recorders
    #   (All recorder lines mimic Tcl flags, using pathlib for file paths.)
    #-----------------------------------------------------------------------------
    model.recorder(
        "Node",
        "-file", str(output_dir / "Disp.out"),
        "-time",
        "-node", 4,
        "-dof", 1,
        "disp"
    )

    model.recorder(
        "Node",
        "-file", str(output_dir / "Acc.out"),
        "-timeSeries", 1,
        "-time",
        "-node", 4,
        "-dof", 1,
        "accel"
    )

    model.recorder(
        "Node",
        "-file", str(output_dir / "Base.out"),
        "-time",
        "-node", 1, 2,
        "-dof", 1,
        "reaction"
    )

    model.recorder(
        "Node",
        "-file", str(output_dir / "NBase.out"),
        "-time",
        "-node", 1, 2,
        "-dof", 2,
        "reaction"
    )

    model.recorder(
        "Element",
        "-file", str(output_dir / "Damperdisp.out"),
        "-time",
        "-ele", 4,
        "deformations"
    )

    model.recorder(
        "Element",
        "-file", str(output_dir / "Damperforce.out"),
        "-time",
        "-ele", 4,
        "localForce"
    )

    model.recorder(
        "Element",
        "-file", str(output_dir / "Dampergbforce.out"),
        "-time",
        "-ele", 4,
        "-dof", 1,
        "force"
    )

    model.recorder(
        "Element",
        "-file", str(output_dir / "Frameforce.out"),
        "-time",
        "-ele", 1, 2,
        "-dof", 1,
        "force"
    )

    #-----------------------------------------------------------------------------
    # 14. Rayleigh damping (first eigenvalue)
    #-----------------------------------------------------------------------------
    eigen_values = model.eigen(1)  # returns the first eigenvalue in a list
    freq = math.sqrt(eigen_values[0])
    period = 2.0 * pi / freq
    print(period)

    damp = 0.02
    # rayleigh alphaM, betaK, betaKinit, betaKcomm
    model.rayleigh(2.0*damp*freq, 0.0, 0.0, 0.0)

    #-----------------------------------------------------------------------------
    # 15. Define and run transient analysis
    #-----------------------------------------------------------------------------
    model.wipeAnalysis()
    model.constraints("Transformation")
    model.numberer("RCM")
    model.system("UmfPack")
    model.test("EnergyIncr", 1.0e-10, 100)
    model.algorithm("KrylovNewton")
    model.integrator("Newmark", 0.5, 0.25)
    model.analysis("Transient")

    steps = 10 * 4096
    dt = 0.001
    ok = model.analyze(steps, dt)

    print("Done!")
    return ok

if __name__ == "__main__":
    main()

