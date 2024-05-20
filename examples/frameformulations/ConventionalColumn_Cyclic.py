#########################################################
# Cyclic analysis of a Lehman's Column 415 (PEER 1998/01)
#########################################################
from opensees.openseespy import *
from opensees.units.iks import *

# Written: Vesna Terzic (vesna@berkeley.edu)
# Created: 12/2011


# Set element type (force-based = 1, displacement-based = 2)
eleType = 1

# Number of finite elements and integration points per element
if eleType == 1:
    NoEle = 1
    nIP = 5
elif eleType == 2:
    NoEle = 4
    nIP = 3

# Create a 2D model with 3 DOFs per node
model("BasicBuilder", "-ndm", 2, "-ndf", 3)

# Input parameters
HCol = 96.0 * inch  # Column height
DCol = 24.0 * inch  # Column diameter
clearCover = 0.75 * inch  # Clear cover of concrete

# Derived quantities
HEle = HCol / NoEle  # Height of one finite element
ACol = (DCol ** 2) * (PI / 4.0)  # Area of the column cross-section

# Define nodes
node(1, 0.0, 0.0)
for i in range(NoEle):
    node(i + 2, 0.0, (i + 1) * HEle)

# Apply boundary conditions
fix(1, 1, 1, 1)

# Define coordinate transformation
transfTag = 1
geomTransf("Corotational", transfTag)

# Define uniaxial materials (concrete and steel)
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
uniaxialMaterial("Steel02", steelTag + 1, fy, Es, 0.025, 18.0, 0.925, 0.15)
uniaxialMaterial("MinMax", steelTag, steelTag + 1, "-min", -0.080, "-max", 0.080)

# Define concrete model (plain and confined)
# Plain (unconfined) concrete
fc = 4.4 * ksi  # Compressive strength of plain concrete
eps0 = 0.002  # Strain corresponding to fc'
epss = 0.005  # Ultimate strain for unconfined concrete
Ec = 57000.0 * sqrt(fc * 1000.0) / 1000.0  # Modulus of elasticity of concrete

# Confined concrete
sprime = stran - NoHoops * dh  # Clear distance between spirals
# Calculate diameter of spirals between spiral bar centers (diameter of the confined core)
ds = DCol - 2.0 * clearCover - dh

# Total area of transverse reinforcement in the bundle
Asp = Asp1 * NoHoops

# Total area of the longitudinal steel in the section
As = barArea * numBars

# Area of core of section
Ac = ds**2 * PI / 4.0

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
fcu = fcc * epscu / epscc * ecr / (ecr - 1.0 + pow(epscu / epscc, ecr))  # Strength that corresponds to ultimate strain (Mander, 1988)

# Define plain concrete and confined concrete materials
uniaxialMaterial("Concrete02", coverTag, -fc, -2.0 * fc / Ec, 0.0, -epss, 0.1, -0.04 * fc, 0.04 * fc / (2.0 * fc / Ec))  # Plain concrete
uniaxialMaterial("Concrete02", coreTag, -fcc, -2.0 * fcc / Ec, -fcu, -epscu, 0.1, -0.04 * fcc, 0.04 * fcc / (2.0 * fcc / Ec))  # Confined concrete

# Define circular fiber section
secnTag = 1
ro = DCol / 2.0  # Radius of the column cross-section
rl = ro - clearCover - dh - (db / 2.0)  # Distance from the column centroid to the centroid of the long. bar
ri = (ds - sprime / 4.0) / 2.0  # Radius of the effectively confined core + s'/8

# Define circular fiber section using patches and layers
section("fiberSec", secnTag, "-GJ", 1e8, {
    # Define the core patch
    patch("circ", coreTag, nfCoreT, nfCoreR, 0, 0, 0, ri, 0.0, 360.0)
    # Define the cover patch
    patch("circ", coverTag, nfCoverT, nfCoverR, 0, 0, ri, ro, 0.0, 360.0)
    # Define the reinforcing layer
    theta = 360.0 / numBars
    layer("circ", steelTag, numBars, barArea, 0, 0, rl, theta / 2.0, 360.0 - theta / 2.0)
})

# Caltrans column shear capacity in English units (Chapter 3 of Caltrans SDC)
poisson = 0.20
G = Ec / (2.0 * (1.0 + poisson))

fv1 = rho_t * fyh / 0.15 + 3.67 - 3.0
if fv1 < 0.3:
    fv1 = 0.3
if fv1 > 3:
    fv1 = 3

ALR = 0.0475 * ACol * fc * 1000.0 / 2000.0 / ACol
fv2 = 1.0 + ALR
if fv2 > 1.5:
    fv2 = 1.5

vc = fv1 * fv2 * sqrt(fc * 1000.0)
if vc > 4.0 * sqrt(fc * 1000.0):
    vc = 4.0 * sqrt(fc * 1000.0)

Vc = 0.8 * ACol * vc / 1000.0

Vs = Asp1 * PI / 2.0 * fyh * ds / stran
Vn = Vc + Vs
Vst = 3.0 / 4.0 * G * ACol
gam_y = Vn / Vst

# Define shear force-deformation relationship
# matTag         Fy     E0     b
uniaxialMaterial("Steel01", steelTag + 6, Vn, Vst, 1.0e-3)

# Aggregate shear to the RC section
secTag = secnTag + 1
section("Aggregator", secTag, steelTag + 6, "Vy", "-section", secnTag)

# Define elements
for i in range(NoEle):
    if eleType == 1:
        element("forceBeamColumn", i + 1, i + 1, i + 2, nIP, secTag, transfTag)
    elif eleType == 2:
        element("dispBeamColumn", i + 1, i + 1, i + 2, nIP, secTag, transfTag)


# Define Gravity Load
IDctrlNode = NoEle + 1

pattern("Plain", 1, "Linear", {
    load(IDctrlNode, 0.0, -147.0, 0.0)  # node#, FX FY MZ
})

constraints("Plain")  # how it handles boundary conditions
numberer("Plain")  # renumber dof's to minimize band-width (optimization), if you want to
system("BandGeneral")  # how to store and solve the system of equations in the analysis
test("NormDispIncr", 1.0e-8, 6)  # determine if convergence has been achieved at the end of an iteration step
algorithm("Newton")  # use Newton's solution algorithm: updates tangent stiffness at every iteration
integrator("LoadControl", 0.1)  # determine the next time step for an analysis, apply gravity in 10 steps
analysis("Static")  # define type of analysis
analyze(10)  # perform gravity analysis
loadConst("-time", 0.0)  # hold gravity constant and restart time

# Cyclic load pattern
# write displacement history into a file
file.mkdir("out")
fileu = open("out/displacement.txt", "w")
fileu.close()

ductility = 7
uy = 1.0
n = 36
dhpret = [0.06, 0.06, 0.06, 0.15, 0.15, 0.15, 0.3, 0.3, 0.3, 0.75, 0.75, 0.75, 1.00, 1.00, 1.00]
dhpost = dhpret + [1.5, 1.5, 1.5, 0.5, 2.0, 2.0, 2.0, 0.65, 3.0, 3.0, 3.0, 1.0, 5, 5, 5]
dhtot = dhpost
running = 0.0

cycles = len(dhtot)
for k in range(cycles):
    cycmax = uy * dhtot[k]
    thist = singlecycle(cycmax, n, running)
    running += thist

anpts = (4 * n - 3) * cycles
dt = running / (anpts - 1)
print(f"pts={anpts}, dt={dt}, tfinal={running}")

# Define time series
model.timeSeries("Path", 2, "-dt", dt, "-filePath", "out/displacement.txt")
IDctrlDOF = 1

# Define load pattern
model.pattern("Plain", 2, 2, {
    sp(IDctrlNode, IDctrlDOF, 1.0)
})

# Define recorders for displacement and force
model.recorder("Node", "-file", "out/Disp.out", "-time", "-node", NoEle + 1, "-dof", 1, "disp")  # records displacement at the top node (TN)
model.recorder("Node", "-file", "out/Force.out", "-time", "-node", 1, "-dof", 1, "reaction")  # records displacement at the top node (TN)

# Cyclic analysis objects
model.constraints("Penalty", 1.0e14, 1.0e14)
model.integrator("LoadControl", dt)
model.numberer("Plain")
model.system("BandGeneral")
model.test("NormDispIncr", 1.0e-7, 10, 0)
model.algorithm("Newton")
model.analysis("Static")

ok = model.analyze(anpts)


