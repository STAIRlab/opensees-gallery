from math import cos,sin,sqrt,pi
import opensees.openseespy as ops


def create_column():
    E = 29000.0
    I = 110.0
    A = 9.12e3
    L = 60.0

    NumberOfElements = 10
    ElementType      = "ForceBeamColumn"
    GeomTransfType   = "Corotational"

    # END OF INPUT

    NumIntegrationPoints = 3
    NumberOfNodes = NumberOfElements + 1
    EulerLoad     = pi*pi*E*I/(L*L)

    model = ops.Model(ndm=2,  ndf=3)

    # Define nodes
    for i in range(1, NumberOfNodes+1):
        y = ((i-1)/float(NumberOfElements)*L)
        model.node(i, 0.0, y)
        model.mass(i, 1.0, 1.0, 1.0)


    # Define boundary conditions
    model.fix(            1, 1, 1, 0)
    model.fix(NumberOfNodes, 1, 0, 0)

    # Define cross-section 
    SectionTag = 1
    model.section('Elastic', SectionTag, E, A, I)

    # Define geometric transformation
    GeomTransfTag = 1
    model.geomTransf(GeomTransfType, GeomTransfTag)

    # Define elements
    model.eval("pragma openseespy off")
    for i in range(1, NumberOfElements+1):
        model.element(ElementType, i, i, i+1, NumIntegrationPoints, SectionTag, GeomTransfTag)
    model.eval("pragma openseespy on")

    # Apply loads
    model.pattern('Plain', 1, "Linear")
    model.load(NumberOfNodes, 0.0, -EulerLoad, 0.0, pattern=1)

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
#           print(f"Element Type:                    {ElementType}")
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

