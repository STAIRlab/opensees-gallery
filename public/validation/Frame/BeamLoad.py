import opensees.openseespy as ops
"""
https://portwooddigital.com/2020/11/28/the-linear-algorithm-strikes-again/

Midspan moment    = wL^2/8
support reactions = wL/2
Support rotations = wL^3/(24EI)
"""

L = 240.0
E = 29000.0
A = 20.0
I = 1400.0
w = 1.5

model = ops.Model(ndm=2, ndf=3)

model.node(1,0,0)
model.fix(1,1,1,0)
model.node(2,L,0)
model.fix(2,1,1,0)

model.geomTransf('Linear',12)

model.section('Elastic',1,E,A,I)
model.beamIntegration('Lobatto',1,1,5)

model.element('forceBeamColumn',1,1,2,12,1)

model.pattern("Plain",1,"Linear")
model.eleLoad('-ele',1,'-type','beamUniform',-w)

Nsteps = 2
model.integrator('LoadControl',1.0/Nsteps)
model.algorithm('Linear')
model.analysis('Static')

model.analyze(Nsteps)
model.reactions()

print(model.nodeReaction(1))
print(model.nodeReaction(2))

