from math import cos,sin,sqrt,pi
import opensees.openseespy as ops
from  opensees.units.english import *
# --------------------------------------------------------------------------------------------------
# build a hollow reinforced concrete confined section
#              Vesna Terzic, 2010
#

# SET UP ----------------------------------------------------------------------------
mode = ops.Model(ndm=3, ndf=6)
dataDir = "Output";
file, 'mkdir', dataDir;

# MATERIAL parameters -------------------------------------------------------------------
IDconcCore = 1;
IDconcCover = 2;
IDreinf = 3;
# nominal concrete compressive strength
fc = -4.0*ksi;
Ec = 57*ksi*sqrt(-fc/psi);
# confined concrete
Kfc = 1.3;
fc1C = Kfc*fc;
eps1C = 2.*fc1C/Ec;
fc2C = 0.2*fc1C;
eps2C = 5*eps1C;
# unconfined concrete
fc1U   = fc;
eps1U  = -0.003;
fc2U   =  0.2*fc1U;
eps2U  = -0.01;
lamda  =  0.1;
# tensile-strength properties
ftC = -0.07*fc1C;
ftU = -0.07*fc1U;
Ets = ftU/0.002;
# -----------
Fy = 66.8*ksi;
Es = 29000.*ksi;
Bs = 0.01;
R0 = 18;
cR1 = 0.925;
cR2 = 0.15;
model.uniaxialMaterial('Concrete02', IDconcCore, fc1C, eps1C, fc2C, eps2C, lamda, ftC, Ets);
model.uniaxialMaterial('Concrete02', IDconcCover, fc1U, eps1U, fc2U, eps2U, lamda, ftU, Ets);
model.uniaxialMaterial('Steel02', IDreinf, Fy, Es, Bs, R0, cR1, cR2);

# Geometry of the section and reinforcement -------------------------------------------------------------------
SecTag = 1;
pi = 3.14
b = 400*cm;
d = 560*cm;
bh = 300*cm;
dh = 460*cm;
cover = 5*cm;
barD = 3.2*cm;
areaFiber = barD**2*pi/4;
dStirrup = 1*cm;
shift = 15*cm;

numFiber1 = 25;
numFiber2 = 13;

#number of subdivision for one patch 
numSubdivIJ1 = 112
numSubdivJK1 = 1
numSubdivIJ2 = 92
numSubdivJK2 = 1
numSubdivIJ3 = 1
numSubdivJK3 = 78
numSubdivIJ4 = 1
numSubdivJK4 = 62
numSubdivIJ5 = 110
numSubdivJK5 = 8
numSubdivIJ6 = 8
numSubdivJK6 = 62

#coordinates that define different patches of confined and unconfined concrete and layers of reinforcement
y1 = (d/2)
z1 = (b/2)
z2 = (z1-cover-dStirrup-barD/2)
y2 = (dh/2)
z4 = (bh/2)
z3 = (z4+cover+dStirrup+barD/2)
y3 = (y1-cover-dStirrup-barD/2)
y4 = (y2+cover+dStirrup+barD/2)

#coordiantes for steel layers 
z4s = (z4-shift)

section.Fiber(SecTag, GJ=1e8, [
       patch.quad(IDconcCover numSubdivIJ1 numSubdivJK1 -y1 z2 y1 z2 y1 z1 -y1 z1),
       patch.quad(IDconcCover numSubdivIJ1 numSubdivJK1 -y1 -z1 y1 -z1 y1 -z2 -y1 -z2),
       patch.quad(IDconcCover numSubdivIJ2 numSubdivJK2 -y2 z4 y2 z4 y2 z3 -y2 z3),
       patch.quad(IDconcCover numSubdivIJ2 numSubdivJK2 -y2 -z3 y2 -z3 y2 -z4 -y2 -z4),
       patch.quad(IDconcCover numSubdivIJ3 numSubdivJK3 y3 -z2 y1 -z2 y1 z2 y3 z2),
       patch.quad(IDconcCover numSubdivIJ3 numSubdivJK3 -y1 -z2 -y3 -z2 -y3 z2 -y1 z2),
       patch.quad(IDconcCover numSubdivIJ4 numSubdivJK4 y2 -z3 y4 -z3 y4 z3 y2 z3),
       patch.quad(IDconcCover numSubdivIJ4 numSubdivJK4 -y4 -z3 -y2 -z3 -y2 z3 -y4 z3),

       patch.quad(IDconcCore numSubdivIJ5 numSubdivJK5 -y3 z3 y3 z3 y3 z2 -y3 z2),
       patch.quad(IDconcCore numSubdivIJ5 numSubdivJK5 -y3 -z2 y3 -z2 y3 -z3 -y3 -z3),
       patch.quad(IDconcCore numSubdivIJ6 numSubdivJK6 y4 -z3 y3 -z3 y3 z3 y4 z3),
       patch.quad(IDconcCore numSubdivIJ6 numSubdivJK6 -y3 -z3 -y4 -z3 -y4 z3 -y3 z3),


       layer.straight(IDreinf numFiber1 areaFiber -y3 z2 y3 z2),
       layer.straight(IDreinf numFiber1 areaFiber -y3 -z2 y3 -z2),
       layer.straight(IDreinf numFiber1 areaFiber -y3 z3 y3 z3),
       layer.straight(IDreinf numFiber1 areaFiber -y3 -z3 y3 -z3),
       layer.straight(IDreinf numFiber2 areaFiber y3 -z4s y3 z4s),
       layer.straight(IDreinf numFiber2 areaFiber -y3 -z4s -y3 z4s),
       layer.straight(IDreinf numFiber2 areaFiber y4 -z4s y4 z4s),
       layer.straight(IDreinf numFiber2 areaFiber -y4 -z4s -y4 z4s),
])

# assign torsional Stiffness for 3D Model
SecTagTorsion = 99;
SecTag3D = 3;
model.uniaxialMaterial('Elastic', SecTagTorsion, Ubig);
section('Aggregator', SecTag3D, SecTagTorsion, "T", section=SecTag);

