#-*-coding: UTF-8-*-
import numpy as np
import math
from ErnstEquation import CableEqualStiffness


def PointsRotate (alpha,x,y):
	#input: x,y in global coordinate axis; alpha rotate angle (radian)-anticlockwise
	#output: newx,newy
	if x==0 and y==0:
			newX=0.0
			newY=0.0
	elif x>0.0 and y==0:
		length1=(x**2+y**2)**0.5
		angle1=0.0
		newAngle=angle1+alpha         
		newX=(length1*math.cos(newAngle))
		newY=(length1*math.sin(newAngle))
	elif x==0.0 and y>0:
		length2=(x**2+y**2)**0.5
		angle2=(90.0/float(180.0))*math.pi
		newAngle=angle2+alpha
		newX=(length2*math.cos(newAngle))
		newY=(length2*math.sin(newAngle))
	elif x<0.0 and y==0:
		length3=(x**2+y**2)**0.5
		angle3=(180.0/float(180.0))*math.pi
		newAngle=angle3+alpha
		newX=(length3*math.cos(newAngle))
		newY=(length3*math.sin(newAngle))
	elif x==0.0 and y<0:
		length4=(x**2+y**2)**0.5
		angle4=(270.0/float(180.0))*math.pi
		newAngle=angle4+alpha
		newX=(length4*math.cos(newAngle))
		newY=(length4*math.sin(newAngle))
	elif x>0.0 and y>0:
		length5=(x**2+y**2)**0.5
		angle5=math.atan(y/float(x))
		newAngle=angle5+alpha
		newX=(length5*math.cos(newAngle))
		newY=(length5*math.sin(newAngle))
	elif x<0.0 and y>0:
		length6=(x**2+y**2)**0.5
		angle6=math.atan(y/float(x))+math.pi
		newAngle=angle6+alpha
		newX=(length6*math.cos(newAngle))
		newY=(length6*math.sin(newAngle))
	elif x<0.0 and y<0:
		length7=(x**2+y**2)**0.5
		angle7=math.atan(y/float(x))+math.pi
		newAngle=angle7+alpha
		newX=(length7*math.cos(newAngle))
		newY=(length7*math.sin(newAngle))
	else:
		length8=(x**2+y**2)**0.5
		angle8=math.atan(y/float(x))+2*math.pi
		newAngle=angle8+alpha
		newX=(length8*math.cos(newAngle))
		newY=(length8*math.sin(newAngle))
	return newX,newY


def Localtransf (alpha,x,y):
	#input: (x,y) is vector in axial direction; alpha rotate angle (radian)-anticlockwise
	#output: transformx, transformy
	if x==0 and y==0:
		print "node error: There has two nodes with same coordinate value!"
	elif x>0.0 and y==0:
		angle1=0.0
		newAngle=angle1+alpha         
	elif x==0.0 and y>0:
		angle2=(90.0/float(180.0))*math.pi
		newAngle=angle2+alpha
	elif x<0.0 and y==0:
		angle3=(180.0/float(180.0))*math.pi
		newAngle=angle3+alpha
	elif x==0.0 and y<0:
		angle4=(270.0/float(180.0))*math.pi
		newAngle=angle4+alpha
	elif x>0.0 and y>0:
		angle5=math.atan(y/float(x))
		newAngle=angle5+alpha
	elif x<0.0 and y>0:
		angle6=math.atan(y/float(x))+math.pi
		newAngle=angle6+alpha
	elif x<0.0 and y<0:
		angle7=math.atan(y/float(x))+math.pi
		newAngle=angle7+alpha
	else:
		angle8=math.atan(y/float(x))+2*math.pi
		newAngle=angle8+alpha

	tranX=math.cos(newAngle)
	tranY=math.sin(newAngle)
	return tranX,tranY


########################################################################################################################
	
def PointTransform (alpha,girdernodes,savefilename):
	"""Return the new coordinate of nodes with rotation of alpha (anticlockwise is the positive direction)
	input: alpha-rotate angle, anticlockwise; girdernodes-[nodeNumber,x,y,z,nodemass] savefilename: "newGirderNodes.txt"
	output: newgirdernodes"""
	radianAlpha=(alpha/180.0)*math.pi
	shape=np.shape(girdernodes)
	m=shape[0]
	n=shape[1]
	newX=[]
	newY=[]
	nodes=np.mat(girdernodes)
	for i1 in range(m):
		newx,newy=PointsRotate (radianAlpha,nodes[i1,1],nodes[i1,2])
		newX.append(newx)
		newY.append(newy)

	newNumber=nodes[:,0]
	newX=np.mat(newX).T
	newY=np.mat(newY).T
	newZ=nodes[:,3]
	newMass=nodes[:,4]
	aa=np.hstack((newNumber,newX,newY,newZ,newMass))
	np.savetxt(savefilename,aa,fmt="%d %.3f %.3f %.3f %.3f")

########################################################################################################################
def GirderLocalAxis (alpha,girdernodes,elements):
	"""return girder local axis after alpha rotating
	input:alpha-rotate angle (anticlockwise);girdernodes-[nodeNumber,x,y,z,nodemass]
	      elements-[elenum,i,j,A,E,G,J,Iy,Iz,transfNumber]
	output:girder local axis-[number,x,y,z]
	                   x
	                   ^
				       |
					   |
					   |--------->z (local)"""
	radianAlpha=(alpha/float(180.0))*math.pi
	m=np.shape(elements)[0]
	n=np.shape(girdernodes)[0]
	element=np.mat(elements)
	node=np.mat(girdernodes)
	transNum=[]
	transx=[]
	transy=[]
	transz=[]
	for i1 in range(m):
		for i2 in range(n):
			if element[i1,1]==node[i2,0]:
				nodeix=node[i2,1]
				nodeiy=node[i2,2]
			if element[i1,2]==node[i2,0]:
				nodejx=node[i2,1]
				nodejy=node[i2,2]
		vectorx=nodejx-nodeix
		vectory=nodejy-nodeiy
		transnewx,transnewy=Localtransf (radianAlpha+1.5*math.pi,vectorx,vectory)
		transNum.append(int(element[i1,9]))
		transx.append(transnewx)
		transy.append(transnewy)
		transz.append(0.0)
	htransNum=np.mat(transNum).T
	htransx=np.mat(transx).T
	htransy=np.mat(transy).T
	htransz=np.mat(transz).T
	aa=np.hstack((htransNum,htransx,htransy,htransz))
	np.savetxt("newGirderTransf.txt",aa,fmt="%d %.6f %.6f %.6f")
########################################################################################################################

def CableMatEle (cableEleFile,cableNodesFile):
	EleN=np.shape(cableEleFile)[0]
	NodeN=np.shape(cableNodesFile)[0]
	element=np.mat(cableEleFile)
	node=np.mat(cableNodesFile)
	nodeList=list(node[:,0])
	MatTag=[]
	Ecable=[]
	PreStress=[]
	EleCableTag=[]
	NodeI=[]
	NodeJ=[]
	Acable=[]
	for i1 in range(EleN):
		indexi=nodeList.index(element[i1,1])
		indexj=nodeList.index(element[i1,2])
		nodei=(node[indexi,1],node[indexi,2],node[indexi,3])
		nodej=(node[indexj,1],node[indexj,2],node[indexj,3])
		cableForce=element[i1,3]
		EqualE,mu,A,TensionSigma=CableEqualStiffness(nodei,nodej,cableForce,k=5,sigma=1770000)
		MatTag.append(int(element[i1,0]))
		Ecable.append(EqualE)
		PreStress.append(TensionSigma)
		EleCableTag.append(int(element[i1,0]))
		NodeI.append(int(element[i1,1]))
		NodeJ.append(int(element[i1,2]))
		Acable.append(A)

		hEleCableTag=np.mat(EleCableTag).T
		hNodeI=np.mat(NodeI).T
		hNodeJ=np.mat(NodeJ).T
		hMatTag=np.mat(MatTag).T
		hEcable=np.mat(Ecable).T
		hPreStress=np.mat(PreStress).T
		hAcable=np.mat(Acable).T

	cableMat=np.hstack((hMatTag,hEcable,hPreStress))
	np.savetxt("newCableMat.txt",cableMat,fmt="%d %.6f %.6f")
	cableEle=np.hstack((hEleCableTag,hNodeI,hNodeJ,hAcable,hMatTag))
	np.savetxt("newCableEle.txt",cableEle,fmt="%d %d %d %.6f %d")
#######################################################################################################################

def PierLocalTransf (Newpiernodes,Newcablenodes,elements):
	"""return pier local axis after alpha rotating
	input:Newpiernodes-[nodeNumber,x,y,z,nodemass]
	      elements-[elenum,i,j,transfNumber]
	output:pier local axis-[number,x,y,z]"""

	ReferenceVector=[(2201,2301),(3201,3301),(4207,4307),(5207,5307),(6203,6303),(7203,7303),(8202,8302)]# ReferenceVector of pier 2,3,4,5,6,7
	element=np.mat(elements)
	piernode=np.mat(Newpiernodes)
	cablenode=np.mat(Newcablenodes)
	Npiernode=np.shape(piernode)[0]
	Ncablenode=np.shape(cablenode)[0]
	conNode=[]
	conX=[]
	conY=[]
	conZ=[]
	conM=[]

	for j1 in range(Npiernode):
		conNode.append(piernode[j1,0])
		conX.append(piernode[j1,1])
		conY.append(piernode[j1,2])
		conZ.append(piernode[j1,3])
		conM.append(piernode[j1,4])

	for j2 in range(Ncablenode):
		conNode.append(cablenode[j2,0])
		conX.append(cablenode[j2,1])
		conY.append(cablenode[j2,2])
		conZ.append(cablenode[j2,3])
		conM.append(cablenode[j2,4])

	hconNode=np.mat(conNode).T
	hconX=np.mat(conX).T
	hconY=np.mat(conY).T
	hconZ=np.mat(conZ).T
	hconM=np.mat(conM).T
	node=np.hstack((hconNode,hconX,hconY,hconZ,hconM))


	Ytransx=[]
	Ytransy=[]
	Ytransz=[]

	mr=len(ReferenceVector)
	m=np.shape(node)[0]
	
	for i2 in range(mr):
		for i3 in range(m):
			if ReferenceVector[i2][0]==node[i3,0]:
				nodeix=node[i3,1]
				nodeiy=node[i3,2]
			if ReferenceVector[i2][1]==node[i3,0]:
				nodejx=node[i3,1]
				nodejy=node[i3,2]
		vectorx=nodejx-nodeix
		vectory=nodejy-nodeiy
		tranX,tranY=Localtransf(0,vectorx,vectory)
		Ytransx.append(tranX)
		Ytransy.append(tranY)
		Ytransz.append(0.0)

	
	Znumber=[]
	Ztransx=[]
	Ztransy=[]
	Ztransz=[]


	for i6 in range(83):
		returnx,returny=Localtransf ((90.0/float(180.0))*math.pi,Ytransx[0],Ytransy[0])

		Znumber.append(element[i6,3])
		Ztransx.append(returnx)
		Ztransy.append(returny)
		Ztransz.append(0)

	for i7 in range(83,191):
		returnx,returny=Localtransf ((90.0/float(180.0))*math.pi,Ytransx[1],Ytransy[1])

		Znumber.append(element[i7,3])
		Ztransx.append(returnx)
		Ztransy.append(returny)
		Ztransz.append(0)

	for i8 in range(191,203):
		returnx,returny=Localtransf ((90.0/float(180.0))*math.pi,Ytransx[2],Ytransy[2])

		Znumber.append(element[i8,3])
		Ztransx.append(returnx)
		Ztransy.append(returny)
		Ztransz.append(0)

	for i9 in range(203,215):
		returnx,returny=Localtransf ((90.0/float(180.0))*math.pi,Ytransx[3],Ytransy[3])

		Znumber.append(element[i9,3])
		Ztransx.append(returnx)
		Ztransy.append(returny)
		Ztransz.append(0)

	for i10 in range(215,219):
		returnx,returny=Localtransf ((90.0/float(180.0))*math.pi,Ytransx[4],Ytransy[4])

		Znumber.append(element[i10,3])
		Ztransx.append(returnx)
		Ztransy.append(returny)
		Ztransz.append(0)

	for i11 in range(219,223):
		returnx,returny=Localtransf ((90.0/float(180.0))*math.pi,Ytransx[5],Ytransy[5])

		Znumber.append(element[i11,3])
		Ztransx.append(returnx)
		Ztransy.append(returny)
		Ztransz.append(0)

	for i12 in range(223,225):
		returnx,returny=Localtransf ((90.0/float(180.0))*math.pi,Ytransx[6],Ytransy[6])

		Znumber.append(element[i12,3])
		Ztransx.append(returnx)
		Ztransy.append(returny)
		Ztransz.append(0)

	
	hZnumber=np.mat(Znumber).T
	hZtransx=np.mat(Ztransx).T
	hZtransy=np.mat(Ztransy).T
	hZtransz=np.mat(Ztransz).T
	aa=np.hstack((hZnumber,hZtransx,hZtransy,hZtransz))
	np.savetxt("newPierTransf.txt",aa,fmt="%d %.6f %.6f %.6f")
#######################################################################################################################

def CrossBeamLocalTransf (Newpiernodes,CrossBeamEle):
	"""return crossbeam local axis after alpha rotating
	input:Newpiernodes-[nodeNumber,x,y,z,nodemass]
	      CrossBeamEle-[elenum,i,j,A,E,G,J,Iy,Iz,transfNumber]
	output:crossBeam local axis-[number,x,y,z]"""
	ReferenceVector=[(2201,2301),(8202,8302)]
	
	node=np.mat(Newpiernodes)
	crossBeamEle=np.mat(CrossBeamEle)
	m=np.shape(node)[0]
	mr=len(ReferenceVector)
	n=np.shape(crossBeamEle)[0]
	Znumber=[]
	Ztransx=[]
	Ztransy=[]
	Ztransz=[]
	ZZtransx=[]
	ZZtransy=[]
	ZZtransz=[]

	for i2 in range(mr):
		for i3 in range(m):
			if ReferenceVector[i2][0]==node[i3,0]:
				nodeix=node[i3,1]
				nodeiy=node[i3,2]
			if ReferenceVector[i2][1]==node[i3,0]:
				nodejx=node[i3,1]
				nodejy=node[i3,2]
		vectorx=nodejx-nodeix
		vectory=nodejy-nodeiy
		tranX,tranY=Localtransf((270.0/float(180.0))*math.pi,vectorx,vectory)
		Ztransx.append(tranX)
		Ztransy.append(tranY)
		Ztransz.append(0.0)
	for i3 in range(6):
		Znumber.append(crossBeamEle[i3,7])
		ZZtransx.append(Ztransx[0])
		ZZtransy.append(Ztransy[0])
		ZZtransz.append(Ztransz[0])
	for i4 in range(6,n):
		Znumber.append(crossBeamEle[i4,7])
		ZZtransx.append(Ztransx[1])
		ZZtransy.append(Ztransy[1])
		ZZtransz.append(Ztransz[1])

		
		

	hZnumber=np.mat(Znumber).T
	hZtransx=np.mat(ZZtransx).T
	hZtransy=np.mat(ZZtransy).T
	hZtransz=np.mat(ZZtransz).T
	aa=np.hstack((hZnumber,hZtransx,hZtransy,hZtransz))
	np.savetxt("newCrossBeamTransf.txt",aa,fmt="%d %.6f %.6f %.6f")


######################################################################################################################
def EqualDOFLocalTransf (Newpiernodes):
	"""return EqualDOF local axis after alpha rotating
	input:Newpiernodes-[nodeNumber,x,y,z,nodemass]
	output:equalDOF local axis-[number,x,y,z]"""
	ReferenceVector=[(2201,2301)]

	node=np.mat(Newpiernodes)
	m=np.shape(node)[0]
	mr=len(ReferenceVector)
	Ztransx=[]
	Ztransy=[]
	Ztransz=[]

	for i2 in range(mr):
		for i3 in range(m):
			if ReferenceVector[i2][0]==node[i3,0]:
				nodeix=node[i3,1]
				nodeiy=node[i3,2]
			if ReferenceVector[i2][1]==node[i3,0]:
				nodejx=node[i3,1]
				nodejy=node[i3,2]
		vectorx=nodejx-nodeix
		vectory=nodejy-nodeiy
		tranX,tranY=Localtransf((270.0/float(180.0))*math.pi,vectorx,vectory)
		Ztransx.append(tranX)
		Ztransy.append(tranY)
		Ztransz.append(0.0)

		
		

	hZtransx=np.mat(Ztransx).T
	hZtransy=np.mat(Ztransy).T
	hZtransz=np.mat(Ztransz).T
	aa=np.hstack((hZtransx,hZtransy,hZtransz))
	np.savetxt("newEqualDOFTransf.txt",aa,fmt="%.6f %.6f %.6f")
#######################################################################################################################
def BearingLocalTransf (Newpiernodes,Newcablenodes):
	"""return bearing local axis after alpha rotating
	input:Newpiernodes-[nodeNumber,x,y,z,nodemass]
	output:bearing local axis in horizontal direction-[x,y,z]"""

	ReferenceVector=[(2201,2301),(3201,3301),(4207,4307),(5207,5307),(6203,6303),(7203,7303),(8202,8302)]# ReferenceVector of pier 2,3,4,5,6,7
	piernode=np.mat(Newpiernodes)
	cablenode=np.mat(Newcablenodes)
	Npiernode=np.shape(piernode)[0]
	Ncablenode=np.shape(cablenode)[0]
	conNode=[]
	conX=[]
	conY=[]
	conZ=[]
	conM=[]

	for j1 in range(Npiernode):
		conNode.append(piernode[j1,0])
		conX.append(piernode[j1,1])
		conY.append(piernode[j1,2])
		conZ.append(piernode[j1,3])
		conM.append(piernode[j1,4])

	for j2 in range(Ncablenode):
		conNode.append(cablenode[j2,0])
		conX.append(cablenode[j2,1])
		conY.append(cablenode[j2,2])
		conZ.append(cablenode[j2,3])
		conM.append(cablenode[j2,4])

	hconNode=np.mat(conNode).T
	hconX=np.mat(conX).T
	hconY=np.mat(conY).T
	hconZ=np.mat(conZ).T
	hconM=np.mat(conM).T
	node=np.hstack((hconNode,hconX,hconY,hconZ,hconM))


	Ytransx=[]
	Ytransy=[]
	Ytransz=[]

	mr=len(ReferenceVector)
	m=np.shape(node)[0]
	
	for i2 in range(mr):
		for i3 in range(m):
			if ReferenceVector[i2][0]==node[i3,0]:
				nodeix=node[i3,1]
				nodeiy=node[i3,2]
			if ReferenceVector[i2][1]==node[i3,0]:
				nodejx=node[i3,1]
				nodejy=node[i3,2]
		vectorx=nodejx-nodeix
		vectory=nodejy-nodeiy
		tranX,tranY=Localtransf((270.0/float(180.0))*math.pi,vectorx,vectory)
		Ytransx.append(tranX)
		Ytransy.append(tranY)
		Ytransz.append(0.0)

	hZtransx=np.mat(Ytransx).T
	hZtransy=np.mat(Ytransy).T
	hZtransz=np.mat(Ytransz).T
	aa=np.hstack((hZtransx,hZtransy,hZtransz))
	np.savetxt("newBearingTransf.txt",aa,fmt="%.6f %.6f %.6f")
	






if __name__=='__main__':

#	girderNodes=np.loadtxt("GirderNode.txt")
#	GirderPointTransform(210,girderNodes)
###########################################################

#	x,y=PointsRotate (float(30)/180*3.14,1,0)
#	print x,y

###########################################################
#	girderNodes=np.loadtxt("GirderNode.txt")
#	elements=np.loadtxt("GirderEle.txt")
#	GirderLocalAxis (0,girderNodes,elements)


###########################################################
	cableEle=np.loadtxt("CableEleForce.txt")
	cableNode=np.loadtxt("CableNode.txt")
	CableMatEle (cableEle,cableNode)

###########################################################
#	Newpiernodes=np.loadtxt("newPylonNodes.txt")
#	Newcablenodes=np.loadtxt("newCableNodes.txt")
#	elements=np.loadtxt("PylonEle.txt")
#	PierLocalTransf (Newpiernodes,Newcablenodes,elements)

###########################################################
#	Newpiernodes=np.loadtxt("newPylonNodes.txt")
#	CrossBeamEle=np.loadtxt("CrossBeamEle.txt")
#	CrossBeamLocalTransf (Newpiernodes,CrossBeamEle)


###########################################################
	
#	Newpiernodes=np.loadtxt("newPylonNodes.txt")
#	EqualDOFLocalTransf (Newpiernodes)

###########################################################
#	Newpiernodes=np.loadtxt("newPylonNodes.txt")
#	Newcablenodes=np.loadtxt("newCableNodes.txt")
#	BearingLocalTransf (Newpiernodes,Newcablenodes)