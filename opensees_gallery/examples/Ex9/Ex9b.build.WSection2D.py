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
# define MATERIAL properties ----------------------------------------
Fy = [expr, 60.0*ksi]
Es = 29000*ksi;
nu = 0.3;
Gs = Es/2./(1+nu)
Hiso = 0
Hkin = 1000
matIDhard = 1
model.uniaxialMaterial('Hardening',  matIDhard, Es, Fy, Hiso, Hkin)

# Structural-Steel W-section properties -------------------------------------------------------------------
SecTag = 1
WSec = 2

# from Steel Manuals:
# in × lb/ft        Area (in2)        d (in)        bf (in)        tf (in)        tw (in)        Ixx (in4)        Iyy (in4)
# W27x114         33.5               27.29        10.07        0.93        0.57        4090        159
d = 27.29*inch
tw = 0.57*inch
bf = 10.07*inch
tf = 0.93*inch
nfdw = 16;
nftw = 4;
nfbf = 16;
nftf = 4;

dw = (d - 2 * tf)
y1 = (-d/2)
y2 = (-dw/2)
y3 = ( dw/2)
y4 = ( d/2)

z1 = (-bf/2)
z2 = (-tw/2)
z3 = ( tw/2)
z4 = ( bf/2)


section.FiberSection( SecTag, GJ=1e8,  [
 patch.quadr(matIDhard nfbf nftf   y1 z4   y1 z1   y2 z1   y2 z4),
 patch.quadr(matIDhard nftw nfdw   y2 z3   y2 z2   y3 z2   y3 z3),
 patch.quadr(matIDhard nfbf nftf   y3 z4   y3 z1   y4 z1   y4 z4),
])
