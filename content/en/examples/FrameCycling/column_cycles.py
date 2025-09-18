#--------------------------------------------------------
# Cyclic analysis of a Lehman's Column 415 (PEER 1998/01)
#--------------------------------------------------------
#
# Written: Vesna Terzic (vesna@berkeley.edu)
# Created: 12/2011
#
import os
from math import sqrt, pi
import xara
import matplotlib.pyplot as plt
try:
    plt.style.use("veux-web")
except:
    pass
from opensees.units.iks import *
import numpy as np

def single_cycle(umax, n, running):

    rate = 0.01
    N =  4*n-3
    dt =  4.0*umax/rate/(N-1)
    m =  umax/(n-1)/dt

    tval, uval = np.zeros((2, N))

    for i in range(N):
          tval[i] = i*dt
          if   i >=  3*n-3:
               uval[i] =   m*tval[i]-4.0*umax

          elif i >=  n:
               uval[i] =  -m*tval[i]+2.0*umax

          else:
               uval[i] = (m*tval[i])

          tval[i] = tval[i] + running


    return tval, uval

def lehman_section(model, D, clearCover):

    coreTag = 1
    coverTag = 2
    steelTag = 3

    # Define materials
    # Longitudinal reinforcement
    barArea = 0.31 * inch**2  # Area of longitudinal bar #5
    db = 0.625 * inch         # Longitudinal bar diameter
    numBars = 22              # Number of longitudinal bars
    fy = 70.0 * ksi  # Yield strength of longitudinal bars
    Es = 29000.0 * ksi  # Modulus of elasticity of steel
    Esf = Es * 0.025  # Tangent at initial strain hardening (calibrated from the coupon test)

    # Transverse reinforcement
    dh = 0.25 * inch  # Diameter of the spiral #2
    NoHoops = 1  # Number of hoops in the bundle
    Asp1 = 0.0491 * inch2  # Area of transverse reinforcement bar
    stran = 1.25 * inch  # Centerline distance between spirals along the height of the column
    fyh = 96.6 * ksi  # Yield strength of the hoop

    # Define steel model
    model.uniaxialMaterial("Steel02", steelTag + 1, fy, Es, 0.025, 18.0, 0.925, 0.15)
    model.uniaxialMaterial("MinMax", steelTag, steelTag + 1, "-min", -0.080, "-max", 0.080)

    # Define concrete model (plain and confined)
    # Plain (unconfined) concrete
    fc = 4.4 * ksi  # Compressive strength of plain concrete
    eps0 = 0.002  # Strain corresponding to fc'
    epss = 0.005  # Ultimate strain for unconfined concrete
    Ec = 57000.0 * sqrt(fc * 1000.0) / 1000.0  # Modulus of elasticity of concrete

    # Confined concrete
    sprime = stran - NoHoops * dh  # Clear distance between spirals
    # Calculate diameter of spirals between spiral bar centers (diameter of the confined core)
    ds = D - 2.0 * clearCover - dh

    # Total area of transverse reinforcement in the bundle
    Asp = Asp1 * NoHoops

    # Total area of the longitudinal steel in the section
    As = barArea * numBars

    # Area of core of section
    Ac = ds**2 * pi / 4.0

    # Ratio of area of longitudinal reinforcement to area of core of section
    rho_cc = As / Ac

    # Confinement effectiveness coefficient = Ae / Acc
    ke = (1.0 - sprime / 2.0 / ds) / (1.0 - rho_cc)

    # Ratio of transverse reinforcement
    rho_t = 4.0 * Asp / ds / stran

    # Effective lateral confining stress on the concrete
    fl = 1.0 / 2.0 * ke * rho_t * fyh

    # Confined concrete compressive strength
    fcc = fc * (-1.254 + 2.254 * sqrt(1.0 + 7.94 * fl / fc) - 2.0 * fl / fc)

    # Strain that corresponds to fcc'
    epscc = eps0 * (1.0 + 5.0 * (fcc / fc - 1.0))

    # Ultimate stress and strain
    ecr = Ec / (Ec - fcc / epscc)  # r factor (Eq. 6 in Mander, 1988)
    epscu = 0.004 + 0.14 * fyh / fc * rho_t  # Ultimate strain (by Dawn Lehman, 1998, PEER 1998/01)
    fcu = fcc * epscu / epscc * ecr / (ecr - 1.0 + (epscu / epscc)**ecr)  # Strength that corresponds to ultimate strain (Mander, 1988)

    # Define plain concrete and confined concrete materials
    model.uniaxialMaterial("Concrete02", coverTag, -fc, -2.0*fc / Ec, 0.0, -epss, 0.1, -0.04*fc, 0.04*fc/(2.0 * fc / Ec))  # Plain concrete
    model.uniaxialMaterial("Concrete02", coreTag, -fcc, -2.0*fcc / Ec, -fcu, -epscu, 0.1, -0.04*fcc, 0.04*fcc/(2.0 * fcc / Ec))  # Confined concrete

    # Define circular fiber section
    secnTag = 1
    nfCoreT = 12
    nfCoreR = 8
    nfCoverT = 12
    nfCoverR = 2
    ro = D / 2.0  # Radius of the column cross-section
    rl = ro - clearCover - dh - (db / 2.0)  # Distance from the column centroid to the centroid of the long. bar
    ri = (ds - sprime / 4.0) / 2.0  # Radius of the effectively confined core + s'/8

    # Define circular fiber section using patches and layers
    theta = 360.0 / numBars
    model.section("fiberSec", secnTag, GJ=1e8)
    # Core patch
    model.patch("circ", coreTag, nfCoreT, nfCoreR, 0, 0, 0, ri, 0.0, 360.0, section=secnTag)
    # Cover patch
    model.patch("circ", coverTag, nfCoverT, nfCoverR, 0, 0, ri, ro, 0.0, 360.0, section=secnTag)
    # Reinforcing bars
    model.layer("circ", steelTag, numBars, barArea, 0, 0, rl, theta / 2.0, 360.0 - theta / 2.0, section=secnTag)

    # Caltrans column shear capacity in English units (Chapter 3 of Caltrans SDC)
    poisson = 0.20
    G = Ec / (2.0 * (1.0 + poisson))

    fv1 = rho_t * fyh / 0.15 + 3.67 - 3.0
    if fv1 < 0.3:
        fv1 = 0.3
    if fv1 > 3:
        fv1 = 3

    # Area of the column cross-section
    ACol = (D ** 2) * (pi / 4.0)

    ALR = 0.0475 * ACol * fc * 1000.0 / 2000.0 / ACol
    fv2 = 1.0 + ALR
    if fv2 > 1.5:
        fv2 = 1.5

    vc = fv1 * fv2 * sqrt(fc * 1000.0)
    if vc > 4.0 * sqrt(fc * 1000.0):
        vc = 4.0 * sqrt(fc * 1000.0)

    Vc = 0.8 * ACol * vc / 1000.0

    Vs = Asp1 * pi / 2.0 * fyh * ds / stran
    Vn = Vc + Vs
    Vst = 3.0 / 4.0 * G * ACol
    gam_y = Vn / Vst

    # Define shear force-deformation relationship
    #                                matTag         Fy   E0     b
    model.uniaxialMaterial("Steel01", steelTag + 6, Vn, Vst, 1.0e-3)

    # Aggregate shear to the RC section
    secTag = secnTag + 1
    model.section("Aggregator", secTag, steelTag + 6, "Vy", "-section", secnTag)
    return secTag

def create_column(ne, nIP, element):

    # Create a 2D model with 3 DOFs per node
    model = xara.Model(ndm=2, ndf=3)

    # Input parameters
    H = 96.0 * inch  # Column height

    # Define nodes
    model.node(1, (0.0, 0.0))
    for i in range(ne):
        model.node(i + 2, (0.0, (i + 1) * H/ne))

    # Apply boundary conditions
    model.fix(1, (1, 1, 1))

    D = 24.0 * inch  # Column diameter
    clearCover = 0.75 * inch  # Clear cover of concrete
    secTag = lehman_section(model, D=D, clearCover=clearCover)

    #
    # Define elements
    #

    # Define coordinate transformation
    transfTag = 1
    model.geomTransf("Corotational", transfTag)

    for i in range(ne):
        model.element(element, i + 1, (i + 1, i + 2), nIP, secTag, transfTag)

    return model


def analyze_column(ne, nIP, eleType):

    model = create_column(ne, nIP, eleType)

    # Define Gravity Load
    IDctrlNode = ne + 1

    model.pattern("Plain", 1, "Linear", load={
        IDctrlNode: (0.0, -147.0, 0.0)
    })

    model.constraints("Plain")
    model.system("BandGeneral")
    model.test("NormDispIncr", 1.0e-8, 6)
    model.algorithm("Newton")
    model.integrator("LoadControl", 0.1)
    model.analysis("Static")
    # perform gravity analysis
    model.analyze(10)
    model.loadConst(time=0.0)  # hold gravity constant and restart time

    #
    # Cyclic load pattern
    #
    ductility = 7
    uy = 1.0
    n = 36
    dhpret = [0.06, 0.06, 0.06, 0.15, 0.15, 0.15, 0.3, 0.3, 0.3, 0.75, 0.75, 0.75, 1.00, 1.00, 1.00]
    dhpost = dhpret + [1.5, 1.5, 1.5, 0.5, 2.0, 2.0, 2.0, 0.65, 3.0, 3.0, 3.0, 1.0, 5, 5, 5]
    dhtot = dhpost
    tend = 0.0

    displacement = []
    cycles = len(dhtot)
    for k in range(cycles):
        thist, uhist = single_cycle(uy * dhtot[k], n, tend)
        tend = thist[-1]
        displacement += uhist.tolist()

    # plt.plot(displacement)
    # plt.show()

    anpts = (4 * n - 3) * cycles
    dt = tend / (anpts - 1)
    print(f"pts={anpts}, dt={dt}, tfinal={tend}")

    # Define time series
    model.timeSeries("Path", 2, dt=dt, values=displacement)
    IDctrlDOF = 1

    # Define load pattern
    model.pattern("Plain", 2, 2)
    model.sp(IDctrlNode, IDctrlDOF, 1.0, pattern=2)

    # Define recorders for displacement and force
    model.recorder("Node", "disp", "-time", file="out/_disp.out", node=ne+1, dof=1)
    model.recorder("Node", "reaction", "-time", file="out/_force.out", node=1, dof=1)

    # Cyclic analysis
    model.constraints("Penalty", 1.0e14, 1.0e14)
    model.integrator("LoadControl", dt)
    model.numberer("Plain")
    model.system("BandGeneral")
    model.test("NormDispIncr", 1.0e-7, 10, 0)
    model.algorithm("Newton")
    model.analysis("Static")

    ok = model.analyze(anpts)
    if ok != 0:
        raise Exception("Analysis failed")

    model.wipe()

    with open("out/_disp.out", "r") as f:
        lines = f.readlines()
        disp = [float(line.split()[1]) for line in lines]
        time = [float(line.split()[0]) for line in lines]
    with open("out/_force.out", "r") as f:
        lines = f.readlines()
        force = [float(line.split()[1]) for line in lines]

    os.remove("out/_disp.out")
    os.remove("out/_force.out")


    return time, disp, force

if __name__ == "__main__":

    fig, ax = plt.subplots()

    # Set element type (force-based = 1, displacement-based = 2)
    for element in "dispBeamColumn", "forceBeamColumn":
        # Number of finite elements and integration points per element
        if "force" in element:
            ne = 1
            nIP = 5
        else:
            # Displacement formulation
            ne = 4
            nIP = 3

        time, disp, force = analyze_column(ne, nIP, element)

        ax.plot(disp, force, label=element)

    ax.set_xlabel("Displacement [in]")
    ax.set_ylabel("Force [kips]")
    fig.legend()
    plt.show()


    fig, ax = plt.subplots()
    ax.plot(time, disp)
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Displacement [in]")
    plt.show()
