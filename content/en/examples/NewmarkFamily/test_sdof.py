import sys
from pathlib import Path
import numpy as np
from numpy import cos,sin,sqrt,pi,exp
import opensees.openseespy

# Linear Elastic SINGLE DOF Model Transient Analysis

# REFERENCES
#
# 1) Chopra, A.K. "Dynamics of Structures: Theory and Applications"
# Prentice Hall, 1995.
#   - Sections 3.1, Section 3.2 and Section 6.4

def ReadRecordAT2(inFilename):
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
    data = []

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
            if "end" in line.lower():
                break

            data.extend(map(float, line.split()))

        else:
            # Search header lines for dt
            words = line.split()

            if len(words) >= 4:

                if words[0] == 'NPTS=':
                    # old SMD format
                    for word in words:
                        if word == '':
                            continue

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
                        if word == '':
                            continue
                        if count == 0:
                            npts = int(word)
                        elif count == 1:
                            dt = float(word)
                        elif word == 'DT':
                            flag = 1
                            break

                        count += 1


    inFileID.close()

    return dt, npts, np.array(data)



#
# global variables
#
gravity = 386.4
testOK  = 0     # variable used to keep track of SUCCESS or FAILURE
tol     = 1.0e-4

# procedure to build a linear model
#   input args: K - desired stiffness
#               periodStruct - desired structure period (used to compute mass)
#               dampRatio (zeta) - desired damping ratio

def create_sdof(K, period, dampRatio):

    wn = 2.0 * pi / period
    m  = K/(wn**2)

    model = opensees.openseespy.Model(ndm=1,  ndf=1)

    model.node( 1,  0.)
    model.node( 2,  0., mass=m)

    model.uniaxialMaterial("Elastic",  1, K)
    model.element("ZeroLength", 1, *[1, 2], mat=1,  dir=1)

    model.fix(1, 1)

    # add damping using rayleigh damping on the mass term
    a0 = 2.0*wn*dampRatio
    model.rayleigh(a0, 0., 0., 0.)

    return model


def build_analysis(model, integrator):
    model.constraints('Plain')
    model.numberer('Plain')
    model.algorithm('Linear') #'Newton')
    model.system('ProfileSPD')
    model.integrator(*integrator)
    model.analysis('Transient')
    return model


def harmonic_undamped(tCurrent, w, wn, P, K):
    return P/K * 1.0/(1 - (w*w)/(wn*wn)) * (sin(w*tCurrent) - (w/wn)*sin(wn*tCurrent))


def harmonic_damped(t, w, wn, dampRatio, P, K):
    wd = (wn*sqrt(1-dampRatio*dampRatio))
    wwn2 = (w*w)/(wn*wn)
    det = (1.0-wwn2)*(1-wwn2) + 4.0 * dampRatio*dampRatio*wwn2
    ust = P/K

    C = ust/det * (1.-wwn2)
    D = ust/det * (-2.*dampRatio*w/wn)
    A = -D
    B = ust/det * (1.0/wd) * ((-2. * dampRatio * w/wn) - w * (1.0 - wwn2))

    return exp(-dampRatio*wn*t)*(A * cos(wd * t) + B*sin(wd*t)) + C*sin(w*t) + D*cos(w*t)


def test_earthquake():
    #
    # Section 6.4 - Earthquake Response of Linear System
    #
    print("\n\nEarthquake Response (Section 6.4)\n")

    testOK = 0

    periodStruct = 0.8
    K  = 2.0

    tol = 3e-2
    dt  = 0.01 # analysis time step

    dir = Path(__file__, "..").resolve()
    dt, _, accel = ReadRecordAT2(str(dir/"elCentro.at2"))

    # print table header
    print("%15s%15s%15s%15s"%('Period', 'Damping', 'OpenSees', 'Reference'))

    # perform analysis for various periods and damping ratios (Figure 6.4.1)
    for  period, dampRatio, peak  in {(0.5, 0.02, 2.67 ),
                                      (1.0, 0.02, 5.97 ),
                                      (2.0, 0.02, 7.47 ),
                                      (2.0, 0.00, 9.91 ),
                                      (2.0, 0.02, 7.47 ),
                                      (2.0, 0.05, 5.37 )}:


        # Create a model
        model = create_sdof(K, period, dampRatio)

        # add load pattern
#       model.timeSeries('Path', 1, filePath='elCentro.dat', dt=0.02,  factor=gravity)
        model.timeSeries('Path', 1, values=accel, dt=dt,  factor=gravity)
        model.pattern("UniformExcitation", 1, 1, accel=1)
#       model.pattern("Plain", 1, 1, factor=-1/m)

        # Configure analysis
        model = build_analysis(model, ["Newmark", 0.5 , 1.0/6.0])

        maxU = 0.0
        for _ in range(int(len(accel.data)*0.02/dt)):
            model.analyze(1, dt)
            u = abs(model.nodeDisp(2))
            if u > maxU:
                maxU = u


        print("%15.2f%15.2f%15.2f%15.2f"%(period,dampRatio,maxU,peak))

        if abs(maxU-peak) > tol :
            testOK = -1;
            print(f"FAILED earthquake response ({period = }, {dampRatio =  })")
            print(f"    {maxU} {peak}, {abs(peak-maxU) = } > {tol}")

    assert testOK == 0



def test_earthquake_inelastic():
    damp = 0.05
    period = 0.5
    # Figure 7.4.3
    for fy, peak, resid  in {( 1.0  , 2.25, 0.00),
                             ( 0.5  , 1.62, 0.17),
                             ( 0.25 , 1.75, 1.10),
                             ( 0.125, 2.07, 1.13)}:
        pass

def test_harmonic_undamped():
    #
    # Section 3.1 - Harmonic Vibrartion of Undamped Elastic SDOF System
    #
    print("Undamped System Harmonic Exciatation (Section 3.1)")

    # model properties
    periodStruct = 0.8
    K  = 2.0
    # harmonic loading
    P = 2.0
    periodForce = 5.0
    tFinal = 2.251*periodForce

    dt = periodStruct/1.0e4; # something, small, for, accuracy

    # derived quantaties
    w  =  2.0 * pi / periodForce
    wn =  2.0 * pi / periodStruct

    #
    # build the model
    #
    model = create_sdof(K, periodStruct, 0.0)

    # add load pattern
    time = np.linspace(0, 100*periodForce, 100)
    series = 1
    model.timeSeries("Trig", series, 0.0, 100.0*periodForce, periodForce, factor=P)
    #   model.timeSeries("Path", series, dt=dt, values=list(np.sin(time)*P)) #, factor=P)

    model.pattern("Plain",  1,  series, load={2: [1.0]})

    # build analysis
    model = build_analysis(model, ["Newmark", 0.5, 1.0/6.0])

    # perform analysis, checking at every step
    tCurrent = 0.
    while tCurrent < tFinal :
        model.analyze(1, dt)
        tCurrent  = model.getTime()
        uOpenSees = model.nodeDisp(2)
        uExact    = harmonic_undamped(tCurrent, w, wn, P, K)

        if abs(uExact - uOpenSees) > tol :
            testOK = -1;
            print(f"failed  undamped harmonic: {abs(uExact - uOpenSees) = } > {tol} at time {tCurrent}")
            tCurrent = tFinal

    print("%20s%15.5f%10s%15.5f" % ("OpenSees: ", uOpenSees, "Exact: ", uExact))

def test_harmonic_damped():

    #
    # Section 3.2 - Harmonic Vibrartion of Damped Elastic SDOF System
    #
    print("\n\nDamped System Harmonic Excitation (Section 3.2)")

    # model properties
    periodStruct = 0.8
    K  = 2.0
    # harmonic loading
    P = 2.0
    periodForce = 5.0
    tFinal = 2.251*periodForce

    dt = periodStruct/1.0e4; # something, small, for, accuracy

    w  =  2.0 * pi / periodForce
    wn =  2.0 * pi / periodStruct

    tol = 1.0e-2
    dampRatio = 0.05

    # build the model
    model = create_sdof(K, periodStruct, dampRatio)

    # add load pattern
    model.timeSeries('Trig', 1, 0.0, 100.0*periodForce, periodForce , factor=P)
    model.pattern("Plain", 1, 1, load={2: [1.0]})

    # build analysis
    model = build_analysis(model, ["Newmark", 0.5, 1.0/6.0])

    t = 0.
    while t < tFinal :
        model.analyze(1, dt)
        t = model.getTime()
        uOpenSees = model.nodeDisp(2)
        uExact    = harmonic_damped(t, w, wn, dampRatio, P, K)
        if abs(uExact-uOpenSees) > tol:
            testOK = -1
            print(f"  failed  damped harmonic>, {abs(uExact-uOpenSees) = } > {tol} at time {t}")
            t = tFinal


    print(f"\n  Displacement Comparison at {t = } (sec):")
    print("%20s%15.5f%10s%15.5f"%("OpenSees: ", uOpenSees, "Exact: ", uExact))


if __name__ == "__main__":

    print("sdofTransient.tcl: Verification of Elastic SDOF systems (Chopra)")

    test_harmonic_undamped()
    test_harmonic_damped()
    test_earthquake()

