import opensees.openseespy as ops
import pandas as pd

model = ops.Model(ndm=3, ndf=6, echo_file=open("/dev/stdout", "w"))

L  =  1.0
A  =  1.0
E  =  1.0
G  =  1.0
J  =  1.0
Iy =  1.0
Iz =  1.0


model.node(1, 0.0, 0.0, 0.0)
model.node(2,   L, 0.0, 0.0)

model.geomTransf("Linear", 1, (0, 1, 0))

model.element("ElasticBeamColumn", 1, (1, 2), A, E, G, J, Iy, Iz, 1)

model.analysis("Static")
print(pd.DataFrame(model.getTangent(k=1)))
