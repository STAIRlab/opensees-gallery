import opensees.openseespy as ops

H = 360
L = 144

ops.wipe()
ops.model('basic','-ndm',2,'-ndf',3)

ops.node(1,0,0); ops.fix(1,1,1,1)
ops.node(2,0,L)
ops.node(3,H,L)
ops.node(4,H,0); ops.fix(4,1,1,1)

E = 29000

# W14x90
A = 26.5
Ic = 999
ops.section('Elastic',1,E,A,Ic)
ops.beamIntegration('Legendre',1,1,2)

# W18x76
A = 22.3
Ig = 1330
ops.section('Elastic',2,E,A,Ig)
ops.beamIntegration('Legendre',2,2,2)

# Corotational transformation
ops.geomTransf('Corotational',1)

# Number of elements/member
Nele = 8

# Columns
c = L/Nele
#               tag Npts nodes type dofs size eleType transfTag beamIntTag
ops.mesh('line', 1,   2,*[1,2],  0,   3,   c,  'dispBeamColumn',1,1)
ops.mesh('line', 2,   2,*[3,4],  0,   3,   c,  'dispBeamColumn',1,1)

# Beam
c = H/Nele
# tag Npts nodes type dofs size eleType transfTag beamIntTag
ops.mesh('line',3,2,*[2,3],0,3,c,'dispBeamColumn',1,2)


ops.print("-json")
