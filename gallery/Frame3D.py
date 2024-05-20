#------------------------------------------------------------------------
#  3D frame example to show how to render opensees model and 
#  plot mode shapes
# 
#  By - Anurag Upadhyay, PhD Candidate, University of Utah.
#  Updated - 09/10/2020
#
#  https://openseespydoc.readthedocs.io/en/stable/src/ModelRendering.html
#------------------------------------------------------------------------

import opensees.openseespy
import numpy as np
from math import asin, sqrt


def frame(
    nbays    = (2,2),
    numFloor = 7,

    bayWidthX = 120.0,
    bayWidthY = 120.0,
    stories = [162.0, 162.0, 156.0, 156.0, 156.0, 156.0, 156.0, 156.0, 156.0, 156.0, 156.0],

    E = 29500.0,
    massX = 0.49,
    M = 0.,
    coordTransf = "Linear",  # Linear, PDelta, Corotational
    massType = "-lMass",  # -lMass, -cMass

    nodeTag = 1):

    numBayX, numBayY = nbays

    ops = opensees.openseespy.Model('Basic', '-ndm', 3, '-ndf', 6)

    # add the nodes
    #  - floor at a time
    zLoc = 0.
    for k in range(0, numFloor + 1):
        xLoc = 0.
        for i in range(0, numBayX + 1):
            yLoc = 0.
            for j in range(0, numBayY + 1):
                ops.node(nodeTag, xLoc, yLoc, zLoc)
                ops.mass(nodeTag, massX, massX, 0.01, 1.0e-10, 1.0e-10, 1.0e-10)
                if k == 0:
                    ops.fix(nodeTag, 1, 1, 1, 1, 1, 1)

                yLoc += bayWidthY
                nodeTag += 1

            xLoc += bayWidthX

        if k < numFloor:
            storyHeight = stories[k]

        zLoc += storyHeight

    # add column element
    ops.geomTransf(coordTransf, 1, 1, 0, 0)
    ops.geomTransf(coordTransf, 2, 0, 0, 1)

    eleTag = 1
    nodeTag1 = 1

    for k in range(0, numFloor):
        for i in range(0, numBayX+1):
            for j in range(0, numBayY+1):
                nodeTag2 = nodeTag1 + (numBayX+1)*(numBayY+1)
                iNode = ops.nodeCoord(nodeTag1)
                jNode = ops.nodeCoord(nodeTag2)
                ops.element('elasticBeamColumn', eleTag, nodeTag1, nodeTag2, 50., E, 1000., 1000., 2150., 2150., 1, '-mass', M, massType)
                eleTag += 1
                nodeTag1 += 1


    nodeTag1 = 1+ (numBayX+1)*(numBayY+1)
    #add beam elements
    for j in range(1, numFloor + 1):
        for i in range(0, numBayX):
            for k in range(0, numBayY+1):
                nodeTag2 = nodeTag1 + (numBayY+1)
                iNode = ops.nodeCoord(nodeTag1)
                jNode = ops.nodeCoord(nodeTag2)
                ops.element('elasticBeamColumn', eleTag, nodeTag1, nodeTag2, 50., E, 1000., 1000., 2150., 2150., 2, '-mass', M, massType)
                eleTag += 1
                nodeTag1 += 1

        nodeTag1 += (numBayY+1)

    nodeTag1 = 1+ (numBayX+1)*(numBayY+1)
    #add beam elements
    for j in range(1, numFloor + 1):
        for i in range(0, numBayY+1):
            for k in range(0, numBayX):
                nodeTag2 = nodeTag1 + 1
                iNode = ops.nodeCoord(nodeTag1)
                jNode = ops.nodeCoord(nodeTag2)
                ops.element('elasticBeamColumn', eleTag, nodeTag1, nodeTag2, 50., E, 1000., 1000., 2150., 2150., 2, '-mass', M, massType)
                eleTag += 1
                nodeTag1 += 1
            nodeTag1 += 1

    ops.print("-json")

frame()

