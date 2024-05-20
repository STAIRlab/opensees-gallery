import openseespy.opensees as ops
import numpy as np

E = 29000
G = 11000
A = 9.12
I = 110
J = 20
L = 60

Nele = 2
dL = L/Nele

Pmax = 6*E*I/L**2

ops.wipe()
ops.model('basic','-ndm',3,'-ndf',6)

ops.geomTransf('Corotational',1,0,0,1)
ops.node(0,0,0,0); #ops.fix(0,1,1,1,1,1,1)
ops.fix(0,1,1,1,1,0,0)
for i in range(Nele):
    ops.node(i+1,(i+1)*dL,0,0)
    ops.element('elasticBeamColumn',i,i,i+1,A,E,G,J,I,I,1)
ops.fix(Nele,0,1,1,0,0,0)

ops.timeSeries('Linear',1)
ops.pattern('Plain',1,1)
ops.load(Nele,-1,0.0,0.0,0.01*L,0.01*L,0.01*L)

Nsteps = 1
dP = Pmax/100

ops.numberer('Plain')
ops.integrator('LoadControl',dP)
ops.system('FullGeneral')
ops.analysis('Static','-noWarnings')


for i in range(Nsteps):
    ok = ops.analyze(1)
    if ok < 0:
        break

K = ops.printA('-ret')
K = np.array(K)
Neqn = ops.systemSize()
K.shape = (Neqn,Neqn)

print('K-K^T =\n')
print(np.array_str(K-K.T, precision=2, suppress_small=True))
# Equation numbers in OpenSees
for nd in ops.getNodeTags():
    print(f'Node {nd}:',ops.nodeDOFs(nd))

