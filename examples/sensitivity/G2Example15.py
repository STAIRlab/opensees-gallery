# ------------------------------------------------------------------------
# The following Python code is implemented by Professor Terje Haukaas at
# the University of British Columbia in Vancouver, Canada. It is made
# freely available online at terje.civil.ubc.ca together with notes,
# examples, and additional Python code. Please be cautious when using
# this code; it may contain bugs and comes without warranty of any kind.
# ------------------------------------------------------------------------

from G2AnalysisLinearStatic import *
from G2Model import *

#              |
#              | P
#              |
#              V
#        ----> * -----> F
#        ----> |
#        ----> |
#        ----> |
#        ----> |
#      q ----> | L
#        ----> |
#        ----> |
#        ----> |
#        ----> |
#        ----> |
#            -----

# Input [N, m, kg, sec]
L = 5.0              # Total length of cantilever
elementType = 5      # Linear frame element
nel = 5              # Number of elements along cantilever
F = 300000.0         # Lateral point load
P = 0.0              # Axial force
q = 10000.0          # Distributed load
E = 200e9            # Modulus of elasticity
hw = 0.355            # Web height
bf = 0.365           # Flange width
tf = 0.018           # Flange thickness
tw = 0.011           # Web thickness
nf = 3               # Number of fibers in the flange
nw = 8               # Number of fibres in the web
trackNode = nel+1    # Node to be plotted
trackDOF = 1         # DOF to be plotted

# Area and moment of inertia
A = tw * (hw - 2 * tf) + 2 * bf * tf
I = tw * (hw - 2 * tf) ** 3 / 12.0 + 2 * bf * tf * (0.5 * (hw - tf)) ** 2

# Nodal coordinates
NODES = []
for i in range(nel+1):
    NODES.append([0.0, i*L/nel])

# Boundary conditions (0=free, 1=fixed, sets #DOFs per node)
CONSTRAINTS = [[1, 1, 1]]
for i in range(nel):
    CONSTRAINTS.append([0, 0, 0])

# Element connectivity and type
ELEMENTS = []
for i in range(nel):
    ELEMENTS.append([elementType, E, A, I, q, i+1, i+2])

# Nodal loads
LOADS = np.zeros((nel+1, 3))
LOADS[nel, 0] = F
LOADS[nel, 1] = -P

# Empty arrays
MASS = np.zeros((nel+1, 3))
SECTIONS = np.zeros(nel)
MATERIALS = np.zeros(nel)

# Create the model object
a = [NODES, CONSTRAINTS, ELEMENTS, SECTIONS, MATERIALS, LOADS, MASS]
m = model(a)

# Request response sensitivities calculated with the direct differentiation method (DDM)
DDMparameters = [['Element', 'E', range(1, nel+1)],
                 ['Element', 'I', range(1, nel+1)],
                 ['Nodal load', nel+1, 1],
                 ['Element', 'q', range(1, nel+1)]]

# Analyze
linearStaticAnalysis(m, trackNode, trackDOF, DDMparameters)

# Analytical DDM sensitivities
print('\n'"Analytical displacement:     %.5e" % (F * L ** 3 / (3 * E * I) + q * L ** 4 / (8 * E * I)))
print("Analytical E sensitivity:    %.5e" % (- F * L ** 3 / (3 * E ** 2 * I) - q * L ** 4 / (8 * E ** 2 * I)))
print("Analytical I sensitivity:    %.5e" % (- F * L**3 / (3 * E * I**2) - q * L**4 / (8 * E * I**2) ))
print("Analytical F sensitivity:    %.5e" % (L ** 3 / (3 * E * I)))
print("Analytical q sensitivity:    %.5e" % (L ** 4 / (8 * E * I)))
