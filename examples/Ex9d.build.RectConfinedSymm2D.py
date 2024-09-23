from math import cos,sin,sqrt,pi
import opensees.openseespy as ops
# --------------------------------------------------------------------------------------------------
# build a section
#              Silvia Mazzoni & Frank McKenna, 2006
#

# SET UP ----------------------------------------------------------------------------
mode = ops.Model(ndm=2, ndf=3)
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
HSec = 5.*ft;
BSec = 3.*ft;
coverSec = 5.*inch
numBarsSec = 16;
barAreaSec = 2.25*in2;
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
#                       y
#                       ^
#                       |    
#             ---------------------
#             |\      cover        /|
#             | \------Top------/ |
#             |c|                   |c|
#             |o|                   |o|
#  z <-----|v|       core      |v|  Hsec
#             |e|                   |e|
#             |r|                    |r|
#             | /-------Bot------\ |
#             |/      cover        \|
#             ---------------------
#                       Bsec
#
# RC section: 
   coverY = HSec/2.0;
   coverZ = BSec/2.0;
   coreY = coverY-coverSec ;
   coreZ = coverZ-coverSec ;
   nfCoreY = 16;
   nfCoreZ = 4;
   nfCoverY = 16;
   nfCoverZ = 4;
   section.FiberSection(SecTag -GJ 1e8 , [

       patch.quadr(IDconcCore nfCoreZ nfCoreY coreY=coreZ,  coreY=True, coreZ=coreY,  coreZ=coreY,  coreZ),
      

       patch.quadr(IDconcCover 1 nfCoverY coverY=coverZ,  coreY=coreZ,  coreY coreZ coverY coverZ),
       patch.quadr(IDconcCover 1 nfCoverY coreY=True, coreZ=coverY, =True, coverZ=coverY,  coverZ=coreY,  coreZ=True),
       patch.quadr(IDconcCover nfCoverZ 1 coverY=coverZ,  coverY=True, coverZ=coreY, =True, coreZ= -coreY coreZ),
       patch.quadr(IDconcCover nfCoverZ 1 coreY coreZ coreY coreZ=coverY,  coverZ=coverY,  coverZ),


       layer.straight(IDreinf numBarsSec barAreaSec  coreY coreZ  coreY -coreZ),
       layer.straight(IDreinf numBarsSec barAreaSec -coreY coreZ -coreY -coreZ),
    };
