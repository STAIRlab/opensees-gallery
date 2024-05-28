from math import cos,sin,sqrt,pi
import opensees.openseespy as ops


def create_column():
    E = 29000.0
    I = 110.0
    A = 9.12e3
    L = 60.0

    ne = 10         # Number of elements discretizing the column
    ElemName      = "ForceBeamColumn"
    GeomTransfType   = "Corotational"


    nIP = 3 # number of integration points along each element
    nn = ne + 1
    EulerLoad = (pi**2)*E*I/L**2

    model = ops.Model(ndm=2,  ndf=3)

    # Define nodes
    for i in range(1, nn+1):
        y = (i-1)/float(ne)*L
        model.node(i, 0.0, y)
        model.mass(i, 1.0, 1.0, 1.0)


    # Define boundary conditions
    model.fix( 1, 1, 1, 0) # Fix dofs 1 and 2 at node 1
    model.fix(nn, 1, 0, 0) # Fix dof 1 at last node

    # Define cross-section 
    SectionTag = 1
    model.section('Elastic', SectionTag, E, A, I)

    # Define geometric transformation
    GeomTransfTag = 1
    model.geomTransf(GeomTransfType, GeomTransfTag)

    # Define elements
    model.eval("pragma openseespy off")
    for i in range(1, ne+1):
        model.element(ElemName, i, i, i+1, nIP, SectionTag, GeomTransfTag)

    model.eval("pragma openseespy on")

    # Apply loads
    model.pattern('Plain', 1, "Linear")
    model.load(nn, 0.0, -EulerLoad, 0.0, pattern=1)

    return model, EulerLoad


def buckling_analysis(model, EulerLoad):
    LoadStep      = 0.01
    PeakLoadRatio = 2.00

    # Analysis Options
    model.system('UmfPack')
    model.constraints('Transformation')
    model.test('NormUnbalance', 1.0e-6, 20, 0)
    model.algorithm('Newton', )
    model.numberer('Plain')
    model.integrator('LoadControl', LoadStep)
    model.analysis('Static')

    LastLoadRatio =  model.getTime()
    LastEigenvalue = model.eigen( 1)

    success = False
    for i in range(1, int(PeakLoadRatio/LoadStep)+1):
        model.analyze(1)
        CurrentLoadRatio =   model.getTime()
        CurrentEigenvalue =  model.eigen(1)[0]

        if CurrentEigenvalue <= 0.0:
            print("Analysis Finished")

            InterpolatedLoadRatio = LastLoadRatio + (CurrentLoadRatio-LastLoadRatio)*LastEigenvalue/(LastEigenvalue-CurrentEigenvalue)

            print(f"Limit Point Found")
#           print(f"Number Of Elements:              {NumberOfElements}")
#           print(f"Element Type:                    {ElemName}")
#           print(f"Geometric Transformation Type:   {GeomTransfType}")
            print(f"Exact Euler Load:                {EulerLoad:.2f}")
            print(f"Computed Euler Load:             {InterpolatedLoadRatio*EulerLoad:.2f}")
            print(f"Percent Error:                   {100*(InterpolatedLoadRatio-1):.2f}")
            success = True
            break


        LastLoadRatio =  CurrentLoadRatio
        LastEigenvalue = CurrentEigenvalue


if __name__ == "__main__":
    model, load   = create_column()
    success       = buckling_analysis(model, load)

    print("Analysis Finished")

    if not success:
        print("No Limit Point Found")

