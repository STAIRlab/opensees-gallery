import opensees.openseespy as ops

E = 29000
G = 16000
fy = 50

A  = 10
Ay =  6
Az =  6

Iz = 100
Iy = 100
J  = 200

L = 100

g = 386.4
m = 1000 / g


model = ops.Model(ndm=3, ndf=6)

model.node(1, 0, 0, 0)
model.node(2, L, 0, 0)
model.fix(1, 1, 1, 1, 1, 1, 1)
#model.fix(2, 0, 0, 0, 0, 0, 0)

model.mass(2, m, 0)

model.section("FrameElastic", 1, E=E, A=A, Ay=Ay, Iz=Iz, Iy=Iy, J=J, G=G)
model.geomTransf("Linear", 1, (0, 0, 1))
model.element("PrismFrame", 1, (1, 2), section=1, transform=1)

model.parameter(1, "element", 1, "E")
model.parameter(2, "element", 1, "A")
model.parameter(3, "element", 1, "Iz")

model.pattern("Plain", 1, "Linear")
model.load(2, (0.0, 1.0, 0.0, 0.0, 0.0, 0.0), pattern=1)


model.constraints("Plain")
model.system("ProfileSPD")
model.print("-json")

if True:

    Py = A * fy
    Pmax = 1.2 * Py
    Nsteps = 100
    dP = Pmax / Nsteps

    model.integrator("LoadControl", dP)
    model.analysis("Static")


    model.sensitivityAlgorithm("-computeAtEachStep")

    for i in range(Nsteps):
        print(model.analyze(1))
        print(model.nodeDisp(2, 2), model.getLoadFactor(1))

        for param in model.getParamTags():
            print("\t", param, model.sensNodeDisp(2, 2, param))

if False:
    model.wipeAnalysis()

    Umax = 2.2
    Nsteps = 100
    Uincr = Umax/Nsteps

    model.integrator("DisplacementControl",2,1,Uincr)
    model.analysis("Static")

    model.sensitivityAlgorithm("-computeAtEachStep")

    for i in range(Nsteps):
        model.analyze(1)
        print(model.nodeDisp(2,1), model.getLoadFactor(1))
        for param in model.getParamTags():
            print(param, model.sensLambda(1, param))
#           print(param, model.sensNodeDisp(2, 1, param))


