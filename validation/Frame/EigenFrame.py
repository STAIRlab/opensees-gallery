# This Extends EigenFrame.tcl verification test to:
#   1) run different element options to test: ForceBeamColumn, DspBeamColumn, ElasticSection and FiberSection2d.
#   2) run different solver options to test:

# REFERENCES
#   as per EigenFrame.tcl

model("Basic", "-ndm", 2)

#    units kip, ft                                                                                                                              

# properties  
bayWidth = 20.0
storyHeight = 10.0

numBay = 10
numFloor = 9
A = 3.0  # area = 3ft^2    
E = 432000.0  # youngs mod = 432000 k/ft^2  
I = 1.0  # second moment of area I=1ft^4       
M = 3.0  # mas/length = 4 kip sec^2/ft^2       
coordTransf = "Linear"  # Linear, PDelta, Corotational
massType = "-lMass"  # -lMass, -cMass


# add the nodes         
#  - floor at a time    
nodeTag = 1
yLoc = 0.0
for j in range(numFloor + 1):
    xLoc = 0.0
    for i in range(numBay + 1):
        node(nodeTag, xLoc, yLoc)
        xLoc += bayWidth
        nodeTag += 1
    yLoc += storyHeight

# fix base nodes        
for i in range(1, numBay + 2):
    fix(i, 1, 1, 1)

# add column element    
geomTransf(coordTransf, 1)
eleTag = 1
for i in range(numBay + 1):
    end1 = i + 1
    end2 = end1 + numBay + 1
    for j in range(numFloor):
        element("elasticBeamColumn", eleTag, end1, end2, A, E, I, 1, "-mass", M, massType)
        end1 = end2
        end2 = end1 + numBay + 1
        eleTag += 1

# add beam elements     
for j in range(1, numFloor + 1):
    end1 = (numBay + 1) * j + 1
    end2 = end1 + 1
    for i in range(numBay):
        element("elasticBeamColumn", eleTag, end1, end2, A, E, I, 1, "-mass", M, massType)
        end1 = end2
        end2 = end1 + 1
        eleTag += 1


