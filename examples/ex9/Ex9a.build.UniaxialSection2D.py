
import opensees.openseespy as ops
# --------------------------------------------------------------------------------------------------
# build a section
#              Silvia Mazzoni & Frank McKenna, 2006
#

# SET UP ----------------------------------------------------------------------------

model = ops.Model(ndm=2, ndf=3)
dataDir = "Output"


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
model.uniaxialMaterial('Steel01', SecTagFlex, MySec, EICrack, b)
model.uniaxialMaterial('Elastic', SecTagAxial, EASec)
section('Aggregator', SecTag, SecTagAxial, "P", SecTagFlex, "Mz")

