import os
import os.path
from pathlib import Path
import opensees.openseespy as ops

#os.chdir(os.path.dirname(os.path.abspath(__file__)))

from math import asin, sin, sqrt, exp, cos


def ReadRecord(inFilename, outFilename):
    """
    A procedure which parses a ground motion record from the PEER
    strong motion database by finding dt in the record header, then
    echoing data values to the output file.

    Formal arguments
       inFilename -- file which contains PEER strong motion record
       outFilename -- file to be written in format G3 can read
    Return values
       dt -- time step determined from file header
       nPts -- number of data points from file header

    Assumptions
       The header in the PEER record is, e.g., formatted as 1 of following:
     1) new PGA database
        PACIFIC ENGINEERING AND ANALYSIS STRONG-MOTION DATA
         IMPERIAL VALLEY 10/15/79 2319, EL CENTRO ARRAY 6, 230
         ACCELERATION TIME HISTORY IN UNITS OF G
         3930 0.00500 NPTS, DT

      2) old SMD database
        PACIFIC ENGINEERING AND ANALYSIS STRONG-MOTION DATA
         IMPERIAL VALLEY 10/15/79 2319, EL CENTRO ARRAY 6, 230
         ACCELERATION TIME HISTORY IN UNITS OF G
         NPTS=  3930, DT= .00500 SEC
    """


    dt = 0.0
    npts = 0

    # Open the input file and catch the error if it can't be read
    inFileID = open(inFilename, 'r')

    # Open output file for writing
    outFileID = open(outFilename, 'w')

    # Flag indicating dt is found and that ground motion
    # values should be read -- ASSUMES dt is on last line
    # of header!!!
    flag = 0

    # Look at each line in the file
    for line in inFileID:
        if line == '\n':
            # Blank line --> do nothing
            continue
        elif flag == 1:
            # Echo ground motion values to output file
            outFileID.write(line)
        else:
            # Search header lines for dt
            words = line.split()
            lengthLine = len(words)

            if lengthLine >= 4:

                if words[0] == 'NPTS=':
                    # old SMD format
                    for word in words:
                        if word != '':
                            # Read in the time step
                            if flag == 1:
                                dt = float(word)
                                break

                            if flag == 2:
                                npts = int(word.strip(','))
                                flag = 0

                            # Find the desired token and set the flag
                            if word == 'DT=' or word == 'dt':
                                flag = 1

                            if word == 'NPTS=':
                                flag = 2


                elif words[-1] == 'DT':
                    # new NGA format
                    count = 0
                    for word in words:
                        if word != '':
                            if count == 0:
                                npts = int(word)
                            elif count == 1:
                                dt = float(word)
                            elif word == 'DT':
                                flag = 1
                                break

                            count += 1

                        

    inFileID.close()
    outFileID.close()

    return dt, npts

# Linear Elastic SINGLE DOF Model Transient Analysis

#REFERENCES: 
# 1) Chopra, A.K. "Dynamics of Structures: Theory and Applications"
# Prentice Hall, 1995.
#   - Sections 3.1, Section 3.2 and Section 6.4

print("================================================================")
print("sdofTransient.py: Verification of Elastic SDOF systems (Chopra)")

#
# global variables
#
def test_sdofTransient():
    PI = 2.0*asin(1.0)
    g = 386.4
    testOK = 0    # variable used to keep track of SUCCESS or FAILURE
    tol = 1.0e-2


    # procedure to build a linear model
    #   input args: K - desired stiffness
    #               periodStruct - desired structre period (used to compute mass)
    #               dampRatio (zeta) - desired damping ratio

    def buildModel(K, periodStruct, dampRatio):

        wn = 2.0 * PI / periodStruct
        m = K/(wn * wn)

        ops.wipe()
        ops.model('basic', '-ndm', 1, '-ndf', 1)

        ops.node(  1,  0.)
        ops.node(  2 , 0., '-mass', m)

        ops.uniaxialMaterial( 'Elastic', 1, K)
        ops.element( 'zeroLength', 1, 1, 2, '-mat', 1, '-dir', 1)
        ops.fix( 1, 1)

        # add damping using rayleigh damping on the mass term
        a0 =2.0*wn*dampRatio
        ops.rayleigh(a0, 0., 0., 0.)


    #
    # procedure to build a linear transient analysis
    #    input args: integrator command newmark

    def buildLinearAnalysis(gamma, beta):
        # do analysis
        ops.constraints('Plain')
        ops.numberer('Plain')
        ops.algorithm('Linear')
        ops.integrator('Newmark', gamma, beta)
        ops.system('ProfileSPD')
        ops.analysis('Transient')


    # Section 3.1 - Harmonic Vibrartion of Undamped Elastic SDOF System
    print("   - Undamped System Harmonic Exciatation (Section 3.1)")

    # harmonic force propertires
    P = 2.0
    periodForce = 5.0
    tFinal = 2.251*periodForce

    # model properties
    periodStruct = 0.8
    K = 2.0

    # derived quantaties
    w = 2.0 * PI / periodForce
    wn = 2.0 * PI / periodStruct


    # build the model
    buildModel( K, periodStruct, 0.0)

    # add load pattern
    ops.timeSeries('Trig', 1, 0.0, 100.0*periodForce, periodForce, '-factor', P)
    ops.pattern('Plain', 1, 1) 
    ops.load(2, 1.0) 

    # build analysis
    buildLinearAnalysis(0.5, 1.0/6.0)

    # perform analysis, checking at every step
    dt = periodStruct/1.0e4 # something small for accuracy
    tCurrent = 0.
    print("\n  for 1000 time steps computing solution and checking against exact solution")
    count = 0

    while tCurrent < tFinal:
        ops.analyze( 1, dt)
        tCurrent = ops.getTime()
        uOpenSees = ops.nodeDisp( 2, 1)
        uExact = P/K * 1.0/(1 - (w*w)/(wn*wn)) * (sin(w*tCurrent) - (w/wn)*sin(wn*tCurrent))

        if abs(uExact-uOpenSees) > tol:
            testOK = -1
            print("failed undamped harmonic> ", abs(uExact-uOpenSees), "> tol at time tCurrent")
            tCurrent = tFinal



    print("\n  example results for last step at ", tCurrent, " (sec):")
    print('         OpenSees: ', uOpenSees, '     Exact:', uExact)


    if abs(uExact-uOpenSees) > tol:
        testOK = -1;
        print("failed  undamped harmonic>", abs(uExact-uOpenSees), " ", tol)





    # Section 3.2 - Harmonic Vibrartion of Damped Elastic SDOF System
    print("\n\n   - Damped System Harmonic Excitation (Section 3.2)")

    dampRatio = 0.05

    # build the model
    buildModel( K, periodStruct, dampRatio)

    # add load pattern
    ops.timeSeries( 'Trig', 1, 0.0, 100.0*periodForce, periodForce, '-factor', P)
    ops.pattern( 'Plain', 1, 1) 
    ops.load( 2, 1.0) 

    # build analysis
    buildLinearAnalysis(0.5, 1.0/6.0)

    # some variables needed in exact computation
    wd = wn*sqrt(1-dampRatio*dampRatio)
    wwn2 = (w*w)/(wn*wn)
    det = (1.0-wwn2)*(1-wwn2) + 4.0 * dampRatio*dampRatio*wwn2
    ust = P/K

    C = ust/det * (1.-wwn2)
    D = ust/det * (-2.*dampRatio*w/wn)
    A = -D
    B = ust/det * (1.0/wd) * ((-2. * dampRatio * w/wn) - w * (1.0 - wwn2))

    t = 0.0
    while t < tFinal:
        ops.analyze(1, dt)
        t = ops.getTime()
        uOpenSees = ops.nodeDisp(2,1)
        uExact = exp(-dampRatio*wn*t)*(A * cos(wd * t) + B*sin(wd*t)) + C*sin(w*t) + D*cos(w*t)
        if abs(uExact-uOpenSees) > tol:
            testOk = -1
            print("failed  damped harmonic>", abs(uExact-uOpenSees), "> ", tol, "at time ", t)
            t = tFinal


    print("\n  example results for last step at ", t, " (sec):")
    print('         OpenSees: ', uOpenSees, '     Exact:', uExact)


    if abs(uExact-uOpenSees) > tol:
        testOK = -1;
        print("failed  damped harmonic>", abs(uExact-uOpenSees), " ", tol)

    # Section 6.4 - Earthquake Response of Linear System

    print("\n\n   - Earthquake Response (Section 6.4)\n")

    tol = 3.0e-2;
    results = [2.67, 5.97, 7.47, 9.91, 7.47, 5.37]


    # read earthquake record, setting dt and nPts variables with data in te file elCentro.at2
    dir = Path(__file__, "..").resolve()
    given_file = str(dir/"elCentro.at2")
    plain_file = str(dir/"elCentro.dat")
    dt, nPts = ReadRecord(given_file, plain_file)

    # print table header
    print('{:>15}{:>15}{:>15}{:>15}'.format('Period','dampRatio','OpenSees','Exact'))

    # perform analysis for bunch of periods and damping ratio's
    counter = 0
    for (period, dampRatio) in [(0.5,0.02),(1.0,0.02),(2.0,0.02),(2.0,0.0),(2.0,0.02),(2.0,0.05)]:
        # build the model
        buildModel(K,period,dampRatio)

        # add load pattern
        ops.timeSeries('Path',1,'-filePath', plain_file, '-dt',dt,'-factor',g)
        ops.pattern('UniformExcitation', 1, 1, '-accel',1)

        # build analysis
        buildLinearAnalysis(0.5, 1.0/6.0)

        maxU = 0.0
        for i in range(nPts):
            ops.analyze(1,dt)
            u = abs(ops.nodeDisp(2,1))
            if u > maxU:
                maxU = u

        uExact = results[counter]
        print('{:>15.2f}{:>15.2f}{:>15.2f}{:>15.2f}'.format(period,dampRatio,maxU,uExact))

        if abs(maxU-uExact) > tol:
            testOK = -1
            print('failed earthquake record period: ',period,' ',dampRatio,': ',dampRatio,': ',maxU,' ',uExact,' ',abs(uExact-maxU),' ',tol)


        counter += 1

    assert testOK == 0

