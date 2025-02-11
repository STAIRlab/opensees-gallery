from opensees import openseespy as _ops
import veux
import matplotlib.pyplot as plt
try:
    plt.style.use("typewriter")
except:
    pass
import math

# Create a model
ops = _ops.Model(ndm=3, ndf=6)
E = 1e4
thickness = 1.0
nu = 0.0
ops.section("ElasticShell", 1, E, nu, thickness)

# mesh
Lx = 20.0
Ly = 1.0
Nx = 20
Ny = 1
dLx = Lx/Nx
dLy = Ly/Ny
for j in range(Ny+1):
    offset = j*(Nx+1)
    yj = j*dLy
    for i in range(Nx+1):
        xi = i*dLx
        ops.node(offset+i+1, (xi, yj, 0.0))

tag = 1
for j in range(Ny):
    for i in range(Nx):
        nodes = (j*(Nx+1)+i+1, j*(Nx+1)+i+2, (j+1)*(Nx+1)+i+2, (j+1)*(Nx+1)+i+1)
        ops.element("ASDShellQ4", tag, nodes, 1, corotational=True)
        tag += 1

# fix
for j in range(Ny+1):
    ops.fix(j*(Nx+1)+1, (1,1,1,1,1,1))

# load
Nrolls = 2
M = (Nrolls*2.0*math.pi*E*thickness**3/12/Lx)
dM = M/Ny/2
ops.pattern("Plain", 1, "Linear")
for j in range(Ny):
    i = Nx-1
    n1 = j*(Nx+1)+i+2
    n2 = (j+1)*(Nx+1)+i+2
    ops.load(n1, (0,0,0,0,-dM,0), pattern=1)
    ops.load(n2, (0,0,0,0,-dM,0), pattern=1)

# analysis
duration = 1.0
nsteps = 40
dt = duration/nsteps
dt_record = 0.2
ops.constraints("Transformation")
ops.numberer("RCM")
ops.system('UmfPack')
ops.test('NormDispIncr', 1.0e-5, 100, 1)
ops.algorithm('Newton')
ops.integrator('LoadControl', dt)
ops.analysis('Static')

#

# Render the reference configuration
artist = veux.create_artist(ops, vertical=3)
artist.draw_surfaces()
artist.draw_outlines()

ctime = 0.0
load = [0.0]
u = [0.0]
tip = (Nx+1)*(Ny+1)

for i in range(nsteps):
    if ops.analyze(1) != 0:
        break
    ctime += dt
    if ctime > dt_record:
        ctime = 0.0
        artist.draw_outlines(state=ops.nodeDisp)

    load.append( ops.getTime() )
    u.append(  ops.nodeDisp(tip, 3) )

# Plot the nodal solution
fig,ax = plt.subplots()
ax.plot(load, u, label="ShellQ4")
ax.set_xlabel(r"Load factor $\lambda$")
ax.set_ylabel(r"Displacement $u_2$")
ax.legend()

# Compute exact solution at Nrolls number of rotations
ref_Uz = 0.0
ref_Ry = Nrolls*2*math.pi
num_Ry = -ops.nodeDisp(tip, 5)
fmt_str = ' | '.join(['{:>12s}']*4)
fmt_num = ' | '.join(['{:>12s}'] + ['{:12.3g}']*3)
print('Summary')
print(fmt_str.format('Value', 'Exact', 'Numerical', 'Error'))
print(fmt_num.format('Uz', ref_Uz, u[-1], abs(u[-1]-ref_Uz)))
print(fmt_num.format('Ry', ref_Ry, num_Ry, abs(num_Ry-ref_Ry)))

artist.draw_surfaces(state=ops.nodeDisp)
artist.draw_outlines(state=ops.nodeDisp)
artist.save("circle.glb")
#fig.savefig("img/plot.png")
# show plot
veux.serve(artist)
plt.show()

