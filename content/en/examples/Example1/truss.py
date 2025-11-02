# ===----------------------------------------------------------------------===//
# 
#         OpenSees - Open System for Earthquake Engineering Simulation    
#                Structural Artificial Intelligence Laboratory
# 
# ===----------------------------------------------------------------------===//
#
# Basic Truss Example 1.1
# -----------------------
#  2D Elastic Truss
#  Single Nodal Load, Static Analysis
#

import xara 
from xara.load import NodalLoads

#
# 1) Build a Model
#

# Create a Model with two-dimensions and 2 DOF/node
model = xara.Model(ndm=2, ndf=2)

# Create nodes
model.node(1, (  0.0,  0.0))
model.node(2, (144.0,  0.0))
model.node(3, (168.0,  0.0))
model.node(4, ( 72.0, 96.0))

# Restrain nodes 1, 2, and 3 in both directions
model.fix(1, (1, 1))
model.fix(2, (1, 1))
model.fix(3, (1, 1))

# Define materials
model.material("Elastic", 1, E=3000.0, nu=0.3)

# Define sections, referencing material 1
model.section("Truss", 1, A=10.0, material=1)
model.section("Truss", 2, A=5.0,  material=1)

# Define truss elements
model.element("Truss", 1, (1, 4), section=1)
model.element("Truss", 2, (2, 4), section=2)
model.element("Truss", 3, (3, 4), section=2)

#
# 2) Define loads
#
# Define a load at node 4 with components 100 and -50 in x and y:
load = NodalLoads({4: [100, -50.0]})


#
# 3) Finally perform the analysis
#
xara.solve(model, load)

#
# Print results
#

# print the current state at node 4 and at all elements
u4 = model.state.u(4)
print(f"u4 = {u4}")
