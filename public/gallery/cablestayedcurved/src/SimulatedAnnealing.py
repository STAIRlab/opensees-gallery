#-*-coding: UTF-8-*-
################################################################################
#  Author: Junjun Guo
#  E-mail: guojj@tongji.edu.cn/guojj_ce@163.com
#  Date: 20/03/2019
#  Environment: Successfully excucted in python 2.7
################################################################################
import numpy as np
import matplotlib.pyplot as plt
from CoordinateTransform import *
import popen2
import os
import random
import time
from BsplInterpolation import BsplineCurve



def Bspline2CableForce (x_new,forcex,forcey):
	Force1=[]

	for i1 in range(len(x_new)-1):
		for j1 in range(len(forcex)):
			if x_new[i1]<=forcex[j1]:
				Force1.append(forcey[j1])
				break

	Force1.append(forcey[-1])

#	plt.plot(forcex,forcey)
#	plt.plot(x_new,Force1,"o")
#	plt.show()
	return Force1

#######################################################################################################################
def CalculateNewObjectFunction (cableForceList):

	cableEle=np.loadtxt("CableEleForce.txt")
	cableEle[:,3]=cableForceList
	np.savetxt("CableEleForce.txt",cableEle,fmt="%d %d %d %.2f")

	cableNodes=np.loadtxt("CableNode.txt")
	cableEle=np.loadtxt("CableEleForce.txt")
	CableMatEle (cableEle,cableNodes)
#######################################
	a,b =  popen2.popen2('OpenSees.exe')
	b.write("source CurvedCableStayedBridge.tcl\n")
#######################################
#	time.sleep(10)
######################################
	pathDir =os.listdir('GirderResponse/GirderNodeDisp')
	number=[]
	for allDir in pathDir:
		child =  os.path.splitext(allDir)
		number.append(int(child[0]))
	number.sort()

	girderDisp=[]
	for i2 in range(len(number)):
		cwd=os.getcwd()
		pathall=os.path.join(cwd,'GirderResponse/GirderNodeDisp/',str(number[i2]),"1.out")
		txtopen=np.loadtxt(pathall)
		sect=np.mat(txtopen)
		girderDisp.append(sect[0,3])

	absGirderDisp = map(abs, girderDisp)
	maxGirderDisp=max(absGirderDisp)

	squareGirderDisp=map(lambda x: x**2,absGirderDisp)
	sumGirderDisp=sum(squareGirderDisp)



	pathDir1 =  os.listdir('PylonNodeDispSet')
	number1=[]
	for allDir1 in pathDir1:
		child1 =  os.path.splitext(allDir1)
		number1.append(int(child1[0]))
	number1.sort()

	PylonDispx=[]
	PylonDispy=[]
	for i3 in range(len(number1)):
		cwd=os.getcwd()
		pathall=os.path.join(cwd,'PylonNodeDispSet/',str(number1[i3]),"1.out")
		txtopen=np.loadtxt(pathall)
		sect=np.mat(txtopen)
		PylonDispx.append(sect[0,1])
		PylonDispy.append(sect[0,2])

	absPylonDispx = map(abs, PylonDispx)
	absPylonDispy = map(abs, PylonDispy)


	maxPylonDispx=max(absPylonDispx)
	maxPylonDispy=max(absPylonDispy)

	squarePylonDispx=map(lambda x: x**2,absPylonDispx)
	squarePylonDispy=map(lambda x: x**2,absPylonDispy)

	sumPylonDispx=sum(squarePylonDispx)
	sumPylonDispy=sum(squarePylonDispy)

	objectFunction=(sumGirderDisp+sumPylonDispx)**0.5

	return objectFunction, maxGirderDisp,maxPylonDispx,maxPylonDispy

	

########################################################################################################################
def sgnFun (t):
	if t>0:
		return 1
	elif t<0:
		return -1
	else:
		return 0
########################################################################################################################
def yChange (T):
	
	u=random.uniform(0,1)
	y=T*sgnFun(u-0.5)*((1+1/float(T))**abs(2*u-1)-1)
	return y
#######################################################################################################################
def UpdateCableForce (newX1,newX2,newX3,newX4,newY1,newY2,newY3,newY4,x_new1,x_new2,x_new3,x_new4):


	forcex1,forcey1=BsplineCurve (newX1,newY1)
#	forcex1,forcey1=BnSpline (newX1,newY1,3,0.01)
	cableForce1=Bspline2CableForce (x_new1,forcex1,forcey1)

	forcex2,forcey2=BsplineCurve (newX2,newY2)
#	forcex2,forcey2=BnSpline (newX2,newY2,3,0.01)
	cableForce2=Bspline2CableForce (x_new2,forcex2,forcey2)

	forcex3,forcey3=BsplineCurve (newX3,newY3)
#	forcex3,forcey3=BnSpline (newX3,newY3,3,0.01)
	cableForce3=Bspline2CableForce (x_new3,forcex3,forcey3)

	forcex4,forcey4=BsplineCurve (newX4,newY4)
#	forcex4,forcey4=BnSpline (newX4,newY4,3,0.01)
	cableForce4=Bspline2CableForce (x_new4,forcex4,forcey4)

	cableForceList=cableForce1+cableForce1+cableForce2+cableForce2+cableForce3+cableForce3+cableForce4+cableForce4

	return cableForceList
##########################################################################################################################
def UpdateCoordinatesValue (T,initX1,initX2,initX3,initX4,initY1,initY2,initY3,initY4):
	newX1=[initX1[0],initX1[1]+yChange (T)*(24-24),initX1[2]+yChange (T)*(48-48),initX1[3]]
	newX2=[initX2[0],initX2[1]+yChange (T)*(40-40),initX2[2]+yChange (T)*(80-80),initX2[3]]
	newX3=[initX3[0],initX3[1]+yChange (T)*(60-60),initX3[2]+yChange (T)*(120-120),initX3[3]]
	newX4=[initX4[0],initX4[1]+yChange (T)*(35-35),initX4[2]+yChange (T)*(70-70),initX4[3]]

	
	while True:
		newY1=[initY1[0]+yChange (T)*1000,initY1[1]+yChange (T)*1000,initY1[2]+yChange (T)*1000,initY1[3]+yChange (T)*1000]
		if 1000<newY1[0]<newY1[1]<newY1[2]<newY1[3]<5500:
			break
		else:
			continue
	while True:
		newY2=[initY2[0]+yChange (T)*1000,initY2[1]+yChange (T)*1000,initY2[2]+yChange (T)*1000,initY2[3]+yChange (T)*1000]
		if 1000<newY2[0]<newY2[1]<newY2[2]<newY2[3]<5500:
			break
		else:
			continue
	while True:
		newY3=[initY3[0]+yChange (T)*1000,initY3[1]+yChange (T)*1000,initY3[2]+yChange (T)*1000,initY3[3]+yChange (T)*1000]
		if 1000<newY3[0]<newY3[1]<newY3[2]<newY3[3]<5500:
			break
		else:
			continue
	while True:
		newY4=[initY4[0]+yChange (T)*1000,initY4[1]+yChange (T)*1000,initY4[2]+yChange (T)*1000,initY4[3]+yChange (T)*1000]
		if 1000<newY4[0]<newY4[1]<newY4[2]<newY4[3]<5500:
			break
		else:
			continue

	return newX1,newX2,newX3,newX4,newY1,newY2,newY3,newY4
	
##########################################################################################################################

def SA (maxT,minT,nIter,initX1,initX2,initX3,initX4,initY1,initY2,initY3,initY4,x_new1,x_new2,x_new3,x_new4):

	T=maxT
	k=0
	savenewmaxGDisp=[]
	savenewmaxPyDispx=[]
	savenewmaxPyDispy=[]
	savenewE=[]
	savecableForceList=[]
	savek=[]

	
	
	while T>=minT:

		kk=0
		savekk=[]

		for iiter in range(nIter):

			oldCableForceList=UpdateCableForce (initX1,initX2,initX3,initX4,initY1,initY2,initY3,initY4,x_new1,x_new2,x_new3,x_new4)


			while True:
				try:
					oldE, oldMaxGDisp,oldMaxPyDispx,oldMaxPyDispy=CalculateNewObjectFunction (oldCableForceList)
					break
				except IndexError:
					break


			
			newX1,newX2,newX3,newX4,newY1,newY2,newY3,newY4=UpdateCoordinatesValue (T,initX1,initX2,initX3,initX4,initY1,initY2,initY3,initY4)
			newCableForceList=UpdateCableForce (newX1,newX2,newX3,newX4,newY1,newY2,newY3,newY4,x_new1,x_new2,x_new3,x_new4)

			while True:
				try:
					newE,newMaxGDisp,newMaxPyDispx,newMaxPyDispy=CalculateNewObjectFunction (newCableForceList)
					break
				except IndexError:
					newX1,newX2,newX3,newX4,newY1,newY2,newY3,newY4=UpdateCoordinatesValue (T,newX1,newX2,newX3,newX4,newY1,newY2,newY3,newY4)
					newCableForceList=UpdateCableForce (newX1,newX2,newX3,newX4,newY1,newY2,newY3,newY4,x_new1,x_new2,x_new3,x_new4)

			deltaE=newE-oldE

			if deltaE<0:
				initX1=newX1
				initX2=newX2
				initX3=newX3
				initX4=newX4

				initY1=newY1
				initY2=newY2
				initY3=newY3
				initY4=newY4

			else:
				p=np.exp(-deltaE/float(T))
				if p>(random.uniform(0,1)):
					initX1=newX1
					initX2=newX2
					initX3=newX3
					initX4=newX4

					initY1=newY1
					initY2=newY2
					initY3=newY3
					initY4=newY4

			kk=kk+1
			savekk.append(kk)

			np.savetxt("iterInternal.txt",savekk,fmt="%d")
###################################################################################################################
#		
		savenewmaxGDisp.append(oldMaxGDisp)
		savenewmaxPyDispx.append(oldMaxPyDispx)
		savenewmaxPyDispy.append(oldMaxPyDispy)
		savenewE.append(oldE)
		savecableForceList.append(oldCableForceList)
		savek.append(k)

		
		np.savetxt("maxGirderDisp.txt",savenewmaxGDisp,fmt="%.6f")

		np.savetxt("maxPylonDispx.txt",savenewmaxPyDispx,fmt="%.6f")

		np.savetxt("maxPylonDispy.txt",savenewmaxPyDispy,fmt="%.6f")

		np.savetxt("objectFunctionValue.txt",savenewE,fmt="%.6f")

		np.savetxt("iterCableForceValue.txt",savecableForceList,fmt="%.2f")                                        

		np.savetxt("iterNumber.txt",savek,fmt="%d")

		k=k+1
		alpha=0.95 #alpha [0.7 1]
		T=maxT*alpha**k


################################################# Main program ##############################
x1Initial=[0.00,24.00,48.00,73.15]
x2Initial=[0.00,40.00,80.00,122.74]
x3Initial=[0.00,60.00,120.00,192.00]
x4Initial=[0.00,35.00,70.00,117.42]
y1Initial=[1000,2500,4000,5500]
y2Initial=[1000,2500,4000,5500]
y3Initial=[1000,2500,4000,5500]
y4Initial=[1000,2500,4000,5500]
x_new1=[0,7.83,15.63,23.4,31.15,38.88,46.57,54.23,61.86,67.51,73.15]#1101-1111
x_new2=[0.00,12.21,24.46,36.74,49.04,61.36,73.69,86.01,98.30,110.55,122.74 ]#1301-1311
x_new3=[0.00,11.99,23.98,35.96,47.95,59.94,71.93,83.92,95.91,107.89,119.88,131.87,143.86,155.85,167.86,179.91,192.00]#1501-1517
x_new4=[0.00,7.79,15.58,23.38,31.10,38.90,46.69,54.48,62.27,70.07,77.86,85.65,93.44,101.11,108.77,113.09,117.42]#1701-1717
####################################################################
maxT=20
minT=1e-5
nIter=2

SA(maxT,minT,nIter,x1Initial,x2Initial,x3Initial,x4Initial,y1Initial,y2Initial,y3Initial,y4Initial,x_new1,x_new2,x_new3,x_new4)