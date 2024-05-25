from math import cos,sin,sqrt,pi
import opensees.openseespy as ops
# --------------------------------------------------------------------------------------------------
# build a section
#              Silvia Mazzoni & Frank McKenna, 2006
#

# SET UP ----------------------------------------------------------------------------
mode = ops.Model(ndm=3, ndf=6)
dataDir = "Output";
file, 'mkdir', dataDir;
from  opensees.units.english import *

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
fc1U = fc;
eps1U = -0.003;
fc2U = 0.2*fc1U;
eps2U = -0.01;
lamda = 0.1;
# tensile-strength properties
ftC = -0.14*fc1C;
ftU = -0.14*fc1U;
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

# section GEOMETRY -------------------------------------------------------------
DSec = 5.*ft;
coverSec = 5.*inch
numBarsSec = 16;
barAreaSec = 2.25*in2;
SecTag = 1;

# Generate a circular reinforced concrete section
# with one layer of steel evenly distributed around the perimeter and a confined core.
# confined core.
#              by:  Michael H. Scott, 2003
# 
#
# Notes
#    The center of the reinforcing bars are placed at the inner radius
#    The core concrete ends at the inner radius (same as reinforcing bars)
#    The reinforcing bars are all the same size
#    The center of the section is at (0,0) in the local axis system
#    Zero degrees is along section y-axis
# 
ri = 0.0;
ro = DSec/2;
nfCoreR = 8;
nfCoreT = 8;
nfCoverR = 4;
nfCoverT = 8;

# Define the fiber section
section.FiberSection(SecTag, GJ=1e8, [
       rc = ro-coverSec;
       patch.circ(IDconcCore nfCoreT nfCoreR 0 0 ri rc 0 360),
       patch.circ(IDconcCover nfCoverT nfCoverR 0 0 rc ro 0 360),
       theta = 360.0/numBarsSec;
       layer.circ(IDreinf numBarsSec barAreaSec 0 0 rc theta 360),


# assign torsional Stiffness for 3D Model
SecTagTorsion = 99;
SecTag3D = 3;
model.uniaxialMaterial('Elastic', SecTagTorsion, Ubig);
section, 'Aggregator', SecTag3D, SecTagTorsion, T -section, SecTag;
