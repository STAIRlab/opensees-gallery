import opensees.openseespy as ops

# Input [N, m, kg, sec]
L = 5.0              # Total length of cantilever
F = 300000.0         # Lateral point load
P = 0.0              # Axial force
w = 10000.0          # Distributed load
E = 200e9            # Modulus of elasticity
G = E*0.6
hw = 0.355           # Web height
bf = 0.365           # Flange width
tf = 0.018           # Flange thickness
tw = 0.011           # Web thickness
nf = 3               # Number of fibers in the flange
nw = 8               # Number of fibres in the web

nel = 1

# Area and moment of inertia
A = tw * (hw - 2 * tf) + 2 * bf * tf
I = tw * (hw - 2 * tf) ** 3 / 12.0 + 2 * bf * tf * (0.5 * (hw - tf)) ** 2


Ay =  A*1e5
Az =  A*1e5

Iz = I
Iy = I
J  = 2*I

# Create the model
model = ops.Model(ndm=3, ndf=6)

# Define nodes
model.node(1, 0, 0, 0)
model.node(2, L, 0, 0)
model.fix(1, 1, 1, 1, 1, 1, 1)

# Configure material and element properties
model.section("FrameElastic", 1, E=E, A=A, Ay=Ay, Az=Az, Iz=Iz, Iy=Iy, J=J, G=G)
model.geomTransf("Linear", 1, (0, 0, 1))
# Create the frame element
model.element("CubicFrame", 1, (1, 2), section=1, transform=1)

# Define parameters
model.parameter(1, "element", 1, "E")
model.parameter(2, "element", 1, "A")
model.parameter(3, "element", 1, "Iz")
model.parameter(4, "node", nel+1, "coord", 1)

model.pattern("Plain", 1, "Linear")
model.load(2, (0.0, 1.0, 0.0, 0.0, 0.0, 0.0), pattern=1)


model.constraints("Plain")
model.system("ProfileSPD")

if True:

    Pmax = F
    Nsteps = 1
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

    model.integrator("DisplacementControl",2,2,Uincr)
    model.analysis("Static")

    model.sensitivityAlgorithm("-computeAtEachStep")

    for i in range(Nsteps):
        model.analyze(1)
        print(model.nodeDisp(2,1), model.getLoadFactor(1))
        for param in model.getParamTags():
            print(param, model.sensLambda(1, param))
#           print(param, model.sensNodeDisp(2, 1, param))



print("u", F*L**3/(3*E*I))
print("L", F*L**2/(E*I))
print("F",   L**3/(3*E*I))

