
import sees
from math import cos,sin,sqrt,pi
import opensees.openseespy as ops
# ZeroLength5.tcl
# CE 221 Spring 1999 Midterm Problem
#
# Written: MHS
# Date: Jan 2000
#
#  |A        B
#  |@--------@------------
#  |    4          6     ^



def rotSpring2D(model, eleID, nodeR, nodeC, matID):
  # Procedure which creates a rotational spring for a planar problem
  #
  # SETS A MULTIPOINT CONSTRAINT ON THE TRANSLATIONAL DEGREES OF FREEDOM,
  # SO DO NOT USE THIS PROCEDURE IF THERE ARE TRANSLATIONAL ZEROLENGTH
  # ELEMENTS ALSO BEING USED BETWEEN THESE TWO NODES
  #
  # Written: MHS
  # Date: Jan 2000
  #
  # Arguments
  # eleID - unique element ID for this zero length rotational spring
  # nodeR - node ID which will be retained by the multi-point constraint
  # nodeC - node ID which will be constrained by the multi-point constraint
  # matID - material ID which represents the moment-rotation relationship
  # for the spring
  model.element('zeroLength', eleID, nodeR, nodeC, mat=matID,  dir=6)

  model.equalDOF(nodeR, nodeC, 1, 2)



# Define the model builder
model = ops.Model(ndm=2,  ndf=3)

# Define nodes
model.node(1,  0.0, 0.0)
model.node(2,  0.0, 0.0)
model.node(3,  4.0, 0.0)
model.node(4,  4.0, 0.0)
model.node(5, 10.0, 0.0)

# Define single point constraints
model.fix(1, 1, 1, 1)
model.fix(5, 1, 1, 0)

# Define moment-rotation relationship for spring A
model.uniaxialMaterial('ElasticPP', 1, 10, 0.8)

# Define moment-rotation relationship for spring B
model.uniaxialMaterial('ElasticPP', 3, 6, 1.0)
model.uniaxialMaterial('Elastic',   4, 4)
model.uniaxialMaterial('Parallel',  2, 3, 4)

# Geometric transformation
model.geomTransf('Linear', 1)

# Define beam elements
model.element('elasticBeamColumn', 3, 2, 3, 100, 1000, 1000, 1)
model.element('elasticBeamColumn', 4, 4, 5, 100, 1000, 1000, 1)


#                eleID nodeR nodeC matID
rotSpring2D(model, 1 ,   1, 2 ,   1)
rotSpring2D(model, 2 ,   3, 4 ,   2)

model.pattern("Plain", 1, "Linear", "{load  3  0.0 -1.0  0.0}")


model.integrator("LoadControl", 1, 1, 1, 1)
model.test("NormDispIncr", 1.0e-8, 10, 1)
model.numberer("Plain")
model.algorithm("KrylovNewton", maxDim=3)
model.constraints("Penalty", 1.0e12, 1.0e12)
model.system("UmfPack")
model.analysis("Static")

model.analyze(1)

artist = sees.render(model, canvas="plotly", ndf=3) #.canvas.popup()
sees.serve(sees.render(model, model.nodeDisp, canvas=artist.canvas, ndf=3)) #.canvas.popup()


model.analyze(9)
model.print( 'algorithm')
model.print( 'node', 4)


artist = sees.render(model, canvas="plotly", ndf=3) #.canvas.popup()
sees.serve(sees.render(model, model.nodeDisp, canvas=artist.canvas, ndf=3)) #.canvas.popup()

