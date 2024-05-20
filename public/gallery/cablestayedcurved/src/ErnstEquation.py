#-*-coding: UTF-8-*-

def CableEqualStiffness (iNode,jNode,T,gamma=78.5,k=2.5,E=2e8,sigma=1860000):
	"""Units: Length-m, Force-kN, mass-ton, Stress-kpa(10e-3MPa), g=9.81m/s2
		Function: This function calculates the equalStiffness of cable by Ernst formula
		inputs: inode,jnode--The end nodes of the cable((xi,yi,zi),(xj,yj,zj))
			T-tension force of cable(kN);
			gamma-Weight per m3,default is 78.5kN/m3
			k-safety factor of cable, default is 2.5
			E-Elastic stiffness of cable, default is 2e8kpa
			sigma-cable design stress, default is 1860000kPa
		outPuts: EqualE,mu,A,TensionSigma
			EqualE--The modified elastic stiffness (kPa)
			mu--Modified factor
			A--Area of the cable (m2)
			TensionSigma--Real stress in cable (kPa)"""
	A=float(T*k)/float(sigma)
	deltaX=jNode[0]-iNode[0]
	deltaY=jNode[1]-iNode[1]
	L=(deltaX**2+deltaY**2)**0.5
	TensionSigma=T/float(A)
	mu=1/float(1+gamma**2*L**2*E/float(12*TensionSigma**3))
	EqualE=E*mu
	return EqualE,mu,A,TensionSigma


if __name__=='__main__':
	EqualE,mu,A,RealSigma=CableEqualStiffness((5.4,17.6,0),(215,12,20),2711,sigma=1770000,k=5)
	print "equalE=:",EqualE
	print "mu=:", mu
	print "A=:", A
	print "RealSigma=:",RealSigma

	

	
	