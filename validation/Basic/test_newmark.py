from math import cos,sin,sqrt,pi
import opensees.openseespy as ops

# Newmark Integrators - Linear & Nonlinear Examples

# REFERENCES: 
# 1) Chopra, A.K. "Dynamics of Structures: Theory and Applications"
#    Prentice Hall, 4th Edition, 2012.
#    - Sections 5:
#         Linear:    Examples 5.3 and 5.4
#         Nonlinear: Examples 5.5 and 5.6


print("Newmark.tcl: Verification of Newmark Integrators (Chopra)")

# global variables
PI =  pi
testOK = 0
tol = 1.0e-3

# procedure to build a linear model
#   input args: K - desired stiffness
#               periodStruct - desired structure period (used to compute mass)
#               dampRatio (zeta) - desired damping ratio
def buildModel(k, m, dampRatio, yieldDisp):

    wn = sqrt(k/m)

    model = ops.Model(ndm=1,  ndf=1)

    model.node( 1,  0.)
    model.node( 2,  0., mass=m, )

    if yieldDisp == 0.:
        model.uniaxialMaterial('Elastic', 1, k)
    else:
        model.uniaxialMaterial('ElasticPP', 1, k, yieldDisp)

    model.element('zeroLength', 1, 1, 2, mat=1,  dir=1)

    model.fix(1, 1)


    a0 = 2.0*wn*dampRatio
    model.rayleigh(a0, 0., 0., 0.)
    return model



#
# procedure to build a transient analysis
#    input args: integrator command
#                algoType: Linear do Linear analysis, else do Nonlinear Newton
def buildAnalysis(model, integratorCommand, algoCmd):

    model.constraints('Plain')
    model.numberer('Plain')
    model.eval(integratorCommand)
    model.test('NormDispIncr', 1.0e-4, 6, 0)
    model.eval(algoCmd)
    model.system('ProfileSPD')
    model.analysis('Transient')


#
# Section 5.4 - Newmark Linear System
#
print("Linear System")
# model properties
m = 0.2533
k = 10.0
dampRatio = 0.05

integratorCmds = [
  ["Newmark Average Acceleration", "integrator Newmark 0.5 0.25 -alpha 1" ],
  ["Newmark Linear Acceleration" , "integrator Newmark 0.5 [expr 1.0/6.0] -alpha 1"]
]


resultsD = [
    [0.0437, 0.2326, 0.6121, 1.0825, 1.4309, 1.4231, 0.9622, 0.1908, -0.6044, -1.1442],
    [0.0300, 0.2193, 0.6166, 1.1130, 1.4782, 1.4625, 0.9514, 0.1273, -0.6954, -1.2208]]

resultsV = [
    [0.8733, 2.9057, 4.6833, 4.4260, 2.2421, -2.3996, -6.8192, -8.6092, -7.2932, -3.5026],
    [0.8995, 2.9819, 4.7716, 4.7419, 2.1802, -2.6911, -7.1468, -8.7758, -7.1539, -3.0508]]

resultsA = [
    [17.4666, 23.1801, 12.3719, -11.5175, -38.1611, -54.6722, -33.6997, -2.1211, 28.4423, 47.3701],
    [17.9904, 23.6566, 12.1372, -12.7305, -39.9425, -56.0447, -33.0689,  0.4892, 31.9491, 50.1114]]


count = 0
for integratorName, integratorCmd in integratorCmds:

    print(f"\n - {integratorName}")
    formatString = "%20s%20s%20s"
    print(formatString % ('Displacement', 'Velocity', 'Acceleration'))
    formatString = "%10s%10s%10s%10s%10s%10s"
    print(formatString % ('OpenSees', 'Hand', 'OpenSees', 'Hand', 'OpenSees', 'Hand'))
    formatString = "%10.4f%10.4f%10.4f%10.4f%10.4f%10.4f"
    resultD = resultsD[count]
    resultV = resultsV[count]
    resultA = resultsA[count]


    model = buildModel(k, m, dampRatio, 0.)


    model.timeSeries('Trig', 1, 0.0, 0.6, 1.2, factor=10.0)

    model.pattern('Plain', 1, 1, load={2: [1.0]})



    buildAnalysis(model, integratorCmd, "algorithm Linear")


    for i in range(10):
        model.analyze(1, 0.1)
        tCurrent  = 2
        uOpenSees = model.nodeDisp(2, 0)
        uComputed = resultD[i]
        vOpenSees = model.nodeVel(2, 0)
        vComputed = resultV[i]
        aOpenSees = model.nodeAccel(2, 0)
        aComputed = resultA[i]
        if abs(uComputed-uOpenSees) > tol:
            testOK = -1
            print(formatString % (uOpenSees, uComputed))
            print("failed  abs(uOpenSees - uComputed) = (abs(uComputed-uOpenSees))> tol")
            i = 11
        else:
            print(formatString % (uOpenSees, uComputed, vOpenSees, vComputed, aOpenSees, aComputed))


    count += 1


#
# Section 5.7 - Newmark Nonlinear System
#
print("\n\nNonlinear System - Newton Average Acceleration With Differing Nonlinear Algorithms")

integratorCmd = "integrator Newmark 0.5 0.25"

algorithmCmds = [
    ["Newton",           "algorithm Newton"],
    ["Modified Newton",  "algorithm ModifiedNewton"]]

resultsD = [
    [0.0437, 0.2326, 0.6121, 1.1143, 1.6214, 1.9891, 2.0951, 1.9240, 1.5602, 1.415],
    [0.0437, 0.2326, 0.6121, 1.1143, 1.6214, 1.9891, 2.0951, 1.9240, 1.5602, 1.414]]
resultsV = [
    [0.8733, 2.9057, 4.6833, 5.3624, 4.7792, 2.5742, -0.4534, -2.960, -4.3075, -4.0668],
    [0.8733, 2.9057, 4.6833, 5.3623, 4.7791, 2.5741, -0.4534, -2.960, -4.3076, -4.0668]]
resultsA = [
    [17.4666, 23.1801, 12.3719, 1.2103, -12.8735, -31.2270, -29.3242, -20.9876, -5.7830, 10.5962],
    [17.4666, 23.1801, 12.3719, 1.2095, -12.8734, -31.2270, -29.3242, -20.9879, -5.7824, 10.5969]]


count = 0
for algoName, algoCmd in algorithmCmds:

    print(f"\n - {algoCmd}")
    formatString = "%20s%20s%20s"
    print(formatString % ('Displacement', 'Velocity', 'Acceleration'))
    formatString = "%10s%10s%10s%10s%10s%10s"
    print(formatString % ('OpenSees', 'Hand', 'OpenSees', 'Hand', 'OpenSees', 'Hand'))
    formatString = "%10.4f%10.4f%10.4f%10.4f%10.4f%10.4f"

    resultD = resultsD[count]
    resultV = resultsV[count]
    resultA = resultsA[count]


    model = buildModel(k, m, dampRatio, 0.75)


    model.timeSeries('Trig', 1, 0.0, 0.6, 1.2, factor=10.0)

    model.pattern('Plain', 1, 1, load={2: [1.0]})


    buildAnalysis(model,integratorCmd, algoCmd)


    for i in range(9):
        model.analyze(1, 0.1)
        tCurrent =  model.getTime()
        uOpenSees = model.nodeDisp(2, 0)
        uComputed = resultD[i]
        vOpenSees = model.nodeVel(2, 0)
        vComputed = resultV[i]
        aOpenSees = model.nodeAccel(2, 0)
        aComputed = resultA[i]
        if abs(uComputed-uOpenSees) > tol:
            testOK = -1
            print(formatString % (uOpenSees, uComputed))
            print("failed  abs(uOpenSees - uComputed) = (abs(uComputed-uOpenSees))> tol")
            break
        else:
            print(formatString % (uOpenSees, uComputed, vOpenSees, vComputed, aOpenSees, aComputed))


    count += 1


if testOK == 0:
    print("\nPASSED Verification Test NewmarkIntegrator.tcl \n\n")
else:
    print("\nFAILED Verification Test NewmarkIntegrator.tcl \n\n")

