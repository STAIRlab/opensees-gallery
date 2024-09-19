from math import cos,sin,sqrt,pi
import opensees.openseespy as ops
# --------------------------------------------------------------------------------------------------
# build a section
#                     Silvia Mazzoni & Frank McKenna, 2006
#

# SET UP ----------------------------------------------------------------------------
mode = ops.Model(ndm=2, ndf=3)
dataDir = "Output";
file, 'mkdir', dataDir;
from  opensees.units.english import *

# MATERIAL parameters -------------------------------------------------------------------
IDconcU = 1;
IDreinf = 2;
# nominal concrete compressive strength
fc = -4.0*ksi;
Ec = 57*ksi*sqrt(-fc/psi);
# unconfined concrete
fc1U = fc;
eps1U = -0.003;
fc2U = 0.2*fc1U;
eps2U = -0.01;
lamda = 0.1;
# tensile-strength properties
ftU = -0.14*fc1U;
Ets = ftU/0.002;
# -----------
Fy = 66.8*ksi;
Es = 29000.*ksi;
Bs = 0.005;
R0 = 18;
cR1 = 0.925;
cR2 = 0.15;
model.uniaxialMaterial('Concrete02', IDconcU, fc1U, eps1U, fc2U, eps2U, lamda, ftU, Ets);
model.uniaxialMaterial('Steel02', IDreinf, Fy, Es, Bs, R0, cR1, cR2);

# section GEOMETRY -------------------------------------------------------------
HSec = 5.*ft;
BSec = 3.*ft;
coverSec = 5.*inch
numBarsSec = 4;
barAreaSec = 1*in2;
SecTag = 1;

# FIBER SECTION properties -------------------------------------------------------------
# symmetric section
#                        y
#                        ^
#                        |     
#             ---------------------     --   --
#             |   o     o     o    |     |    -- cover
#             |                       |     |
#             |                       |     |
#    z <--- |          +           |     H
#             |                       |     |
#             |                       |     |
#             |   o     o     o    |     |    -- cover
#             ---------------------     --   --
#             |-------- B --------|
#
# RC section: 
   coverY = HSec/2.0;
   coverZ = BSec/2.0;
   coreY = coverY-coverSec ;
   coreZ = coverZ-coverSec ;
   nfY = 16;
   nfZ = 4;
   section.FiberSection(SecTag -GJ 1e8 , [
       patch.quadr(IDconcU nfZ nfY -coverY coverZ -coverY -coverZ coverY -coverZ coverY coverZ),
       layer.straight(IDreinf numBarsSec barAreaSec  coreY coreZ  coreY -coreZ),
       layer.straight(IDreinf numBarsSec barAreaSec -coreY coreZ -coreY -coreZ),
    };

