import opensees.openseespy as ops
#import openseespy.opensees as ops

E = 29000
Fy = 50
Hkin = 500

A = 10
L = 100

g = 386.4
m = 1000 / g


ops.wipe()
ops.model("basic", "-ndm", 2, "-ndf", 2)

ops.node(1, 0, 0)
ops.fix(1, 1, 1)
ops.node(2, L, 0)
ops.fix(2, 0, 1)

ops.mass(2, m, 0)

ops.uniaxialMaterial("Hardening", 1, E, Fy, 0, Hkin)

ops.element("truss", 1, 1, 2, A, 1)


ops.parameter(1, "element", 1, "E")
ops.parameter(2, "element", 1, "A")
ops.parameter(3, "element", 1, "Fy")
ops.parameter(4, "element", 1, "Hkin")

ops.timeSeries("Linear", 1)
ops.pattern("Plain", 1, 1) #"Linear")
ops.load(2, 1.0, 0) #, pattern=1)


ops.constraints("Plain")
ops.system("ProfileSPD")
#ops.print("-json")

if False:

    Py = A * Fy
    Pmax = 1.2 * Py
    Nsteps = 100
    dP = Pmax / Nsteps

    ops.integrator("LoadControl", dP)
    ops.analysis("Static")


    ops.sensitivityAlgorithm("-computeAtEachStep")

    for i in range(Nsteps):
        ops.analyze(1)
        print(ops.nodeDisp(2, 1), ops.getLoadFactor(1))

        for param in ops.getParamTags():
            print(param, ops.sensNodeDisp(2, 1, param))

if True:
    ops.wipeAnalysis()

    Umax = 2.2
    Nsteps = 100
    Uincr = Umax/Nsteps

    ops.integrator("DisplacementControl",2,1,Uincr)
    ops.analysis("Static")

    ops.sensitivityAlgorithm('-computeAtEachStep')

    for i in range(Nsteps):
        ops.analyze(1)
        print(ops.nodeDisp(2,1), ops.getLoadFactor(1))
        for param in ops.getParamTags():
            print(param, ops.sensLambda(1,param))
#           print(param, ops.sensNodeDisp(2, 1, param))


