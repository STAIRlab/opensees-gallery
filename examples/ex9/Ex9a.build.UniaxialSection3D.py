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
SecTagFlex = 2;
SecTagAxial = 3;
SecTag = 1;

# COLUMN section
# calculated stiffness parameters
EASec = Ubig;
MySec = 130000*kip*inch
PhiYSec = 0.65e-4/inch
EICrack = MySec/PhiYSec;
b = 0.01 ;
model.uniaxialMaterial('Steel01', SecTagFlex, MySec, EICrack, b);
model.uniaxialMaterial('Elastic', SecTagAxial, EASec);

# assign torsional Stiffness for 3D Model
SecTagTorsion = 99;
SecTag3D = 5;
model.uniaxialMaterial('Elastic', SecTagTorsion, Ubig);
section, 'Aggregator', SecTag3D, SecTagAxial, P SecTagFlex, 'Mz', SecTagTorsion, T;
