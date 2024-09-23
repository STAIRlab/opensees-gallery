import opensees.openseespy as ops

E = 29000
fy = 50
Hkin = 500

A = 10
L = 100

g = 386.4
m = 1000 / g


model = ops.Model(ndm=2, ndf=2)

model.node(1, 0, 0)
model.fix(1, 1, 1)
model.node(2, L, 0)
model.fix(2, 0, 1)

model.mass(2, m, 0)

model.uniaxialMaterial("Hardening", 1, E, fy, 0, Hkin)

model.element("truss", 1, 1, 2, A, 1)

model.parameter(1, "element", 1, "E")
model.parameter(2, "element", 1, "A")
model.parameter(3, "element", 1, "Fy")
model.parameter(4, "element", 1, "Hkin")

model.pattern("Plain", 1, "Linear")
model.load(2, 1.0, 0, pattern=1)


model.constraints("Plain")
model.system("ProfileSPD")
#model.print("-json")

if True:

    Py = A * fy
    Pmax = 1.2 * Py
    Nsteps = 100
    dP = Pmax / Nsteps

    model.integrator("LoadControl", dP)
    model.analysis("Static")


    model.sensitivityAlgorithm("-computeAtEachStep")

    for i in range(Nsteps):
        model.analyze(1)
        print(model.nodeDisp(2, 1), model.getLoadFactor(1))

        for param in model.getParamTags():
            print(param, model.sensNodeDisp(2, 1, param))

if True:
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


