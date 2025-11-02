import xara
import math
import veux
import matplotlib.pyplot as plt
try:
    plt.style.use("typewriter")
except:
    pass
import math

# Create a model
model = xara.Model(ndm=3, ndf=6)
E = 1e4
thickness = 1.0
nu = 0.0
model.section("ElasticShell", 1, E, nu, thickness)

# Create a mesh
Lx = 20.0
Ly = 1.0
Nx = 20
Ny = 1
EI = thickness**3*Lx/12
dLx = Lx/Nx
dLy = Ly/Ny
for j in range(Ny+1):
    offset = j*(Nx+1)
    yj = j*dLy
    for i in range(Nx+1):
        xi = i*dLx
        model.node(offset+i+1, (xi, yj, 0.0))

tag = 1
for j in range(Ny):
    for i in range(Nx):
        nodes = (j*(Nx+1)+i+1, j*(Nx+1)+i+2, (j+1)*(Nx+1)+i+2, (j+1)*(Nx+1)+i+1)
        model.element("ASDShellQ4", tag, nodes, 1, corotational=True)
        tag += 1

# fix
for j in range(Ny+1):
    model.fix(j*(Nx+1)+1, (1,1,1,1,1,1))

# load
Nrolls = 2
M = (Nrolls*2.0*math.pi*E*thickness**3/12/Lx)
dM = M/Ny/2
model.pattern("Plain", 1, "Linear")
for j in range(Ny):
    i = Nx-1
    n1 = j*(Nx+1)+i+2
    n2 = (j+1)*(Nx+1)+i+2
    model.load(n1, (0,0,0,0,-dM,0), pattern=1)
    model.load(n2, (0,0,0,0,-dM,0), pattern=1)

# analysis
duration = 1.0
nsteps = 40
dt = duration/nsteps
dt_record = 0.2
model.constraints("Transformation")
model.numberer("RCM")
model.system('UmfPack')
model.test('NormDispIncr', 1.0e-5, 100, 1)
model.algorithm('Newton')
model.integrator('LoadControl', dt)
model.analysis('Static')

#

# Render the reference configuration
artist = veux.create_artist(model, vertical=3)
artist.draw_surfaces()
artist.draw_outlines()

ctime = 0.0
load = [0.0]
u = [0.0]
tip = (Nx+1)*(Ny+1)

for i in range(nsteps):
    if model.analyze(1) != 0:
        break
    ctime += dt
    if ctime > dt_record:
        ctime = 0.0
        artist.draw_outlines(state=model.nodeDisp)

    load.append( model.getTime() )
    u.append(  model.nodeDisp(tip, 3) )

# Plot the nodal solution
fig,ax = plt.subplots()
ax.plot(load, u, label="ShellQ4")
# ax.plot(load, [0]+[-EI/(m*2*math.pi)*(math.cos(m*2*math.pi)-1) for m in load[1:]], label="Analytic")
ax.set_xlabel(r"Load factor $\lambda$")
ax.set_ylabel(r"Displacement $u_2$")
ax.legend()

# Compute exact solution at Nrolls number of rotations
ref_Uz = 0.0
ref_Ry = Nrolls*2*math.pi
num_Ry = -model.nodeDisp(tip, 5)
fmt_str = ' | '.join(['{:>12s}']*4)
fmt_num = ' | '.join(['{:>12s}'] + ['{:12.3g}']*3)
print('Summary')
print(fmt_str.format('Value', 'Exact', 'Numerical', 'Error'))
print(fmt_num.format('Uz', ref_Uz, u[-1], abs(u[-1]-ref_Uz)))
print(fmt_num.format('Ry', ref_Ry, num_Ry, abs(num_Ry-ref_Ry)))

artist.draw_surfaces(state=model.nodeDisp)
artist.draw_outlines(state=model.nodeDisp)
artist.save("circle.glb")
#fig.savefig("img/plot.png")
# show plot
veux.serve(artist)
plt.show()

