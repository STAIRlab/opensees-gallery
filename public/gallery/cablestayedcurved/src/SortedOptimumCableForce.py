#-*-coding: UTF-8-*-
import numpy as np
from CoordinateTransform import *
import math
import os
import popen2
import random
from BnSpline import BnSpline
import matplotlib.pyplot as plt
import time
from BsplInterpolation import BsplineCurve
from compiler.ast import flatten
#######################################################

def cableLength (cableEleFile,cableNodesFile):

	EleN=np.shape(cableEleFile)[0]
	NodeN=np.shape(cableNodesFile)[0]
	element=np.mat(cableEleFile)
	node=np.mat(cableNodesFile)
	nodeList=list(node[:,0])

	listCableLength=[]

	for i1 in range(EleN):
		indexi=nodeList.index(element[i1,1])
		indexj=nodeList.index(element[i1,2])
		nodei=(node[indexi,1],node[indexi,2],node[indexi,3])
		nodej=(node[indexj,1],node[indexj,2],node[indexj,3])

		lengthSqrt=((nodei[0]-nodej[0])**2+(nodei[1]-nodej[1])**2+(nodei[2]-nodej[2])**2)**0.5
		listCableLength.append(lengthSqrt)

	return listCableLength

##########################################################################
Ntop=10

maxGirderDisp=np.loadtxt("maxGirderDisp.txt")
maxPylonDispx=np.loadtxt("maxPylonDispx.txt")
maxPylonDispy=np.loadtxt("maxPylonDispy.txt")
objFunValue=np.loadtxt("objectFunctionValue.txt")
cableForceValue=np.loadtxt("iterCableForceValue.txt")

listmaxGirderDisp=maxGirderDisp.tolist()
listmaxPylonDispx=maxPylonDispx.tolist()
listmaxPylonDispy=maxPylonDispy.tolist()
listcableForceValue=cableForceValue.tolist()
listobjFunValue=objFunValue.tolist()

mGirder=np.shape(maxGirderDisp)[0]
mPylonX=np.shape(maxPylonDispx)[0]
mPylonY=np.shape(maxPylonDispy)[0]
mobjFun=np.shape(objFunValue)[0]
mcableForce=np.shape(cableForceValue)[0]

listObjFun=objFunValue.tolist()
listObjFun.sort()

topObjFun=[]
for i1 in range(Ntop):
	topObjFun.append(listObjFun[i1])

topIndex=[]

for i2 in range(Ntop):
	topIndex.append(listobjFunValue.index(topObjFun[i2]))

obtainedGirderDisp=[]
obtainedPylonX=[]
obtainedPylonY=[]
obtainedCableForce=[]

for i3 in range(Ntop):
	obtainedGirderDisp.append(maxGirderDisp[topIndex[i3]])
	obtainedPylonX.append(maxPylonDispx[topIndex[i3]])
	obtainedPylonY.append(maxPylonDispy[topIndex[i3]])
	obtainedCableForce.append(cableForceValue[topIndex[i3]])

matCableForce=np.mat(obtainedCableForce)
print "GirderDisp:"
print np.mat(obtainedGirderDisp).T
np.savetxt("1000-2500resultsGirderDisp.txt",np.mat(obtainedGirderDisp).T,fmt="%.3f")
print "PylonDispx:"
print np.mat(obtainedPylonX).T
np.savetxt("1000-2500resultsPylonX.txt",np.mat(obtainedPylonX).T,fmt="%.3f")
print "PylonDispy"
print np.mat(obtainedPylonY).T
np.savetxt("1000-2500resultsPylonY.txt",np.mat(obtainedPylonY).T,fmt="%.3f")
print "CableForce:"
print obtainedCableForce
np.savetxt("1000-2500resultCableForce.txt",obtainedCableForce,fmt="%d")

#####################################################################

cableEle=np.loadtxt("CableEleForce.txt")
cableNode=np.loadtxt("CableNode.txt")
listCableLength=cableLength (cableEle,cableNode)

totalCable=[]

for i4 in range(Ntop):
	listCableForce=np.mat(matCableForce[i4,:]).tolist()[0]


	totaltrans= sum(map(lambda (a,b):a*b,zip(listCableForce,listCableLength)))
	totalCable.append(totaltrans)

matTotalCable=np.mat(totalCable).T
np.savetxt("1000-2500TotalCabe.txt",matTotalCable,fmt="%d")
print "TotalCableUsed:"
print  matTotalCable
