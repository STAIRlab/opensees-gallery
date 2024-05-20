#-*-coding: UTF-8-*-
import numpy as np
import pylab as pl
from scipy import interpolate 

def BsplineCurve (x,y,Npoint=1000):
	"""Return cable forces based on Bspline
		input: x,y--coordinates of 4 control points
			x_new--the x coordinates of each cables
		output: cable forces
	"""
	x_new=np.linspace(x[0],x[-1],Npoint)
	tck = interpolate.splrep(x, y)
	y_bspline = interpolate.splev(x_new, tck)

	return x_new,y_bspline



###############################################
#x=[0,24,48,73.5]
#y=[1000,5000,3000,4000]
#xnew,ynew=BsplineCurve (x,y)
#pl.plot(x, y, "o",  label="OriginalData")
#pl.plot(xnew, ynew, label="B-spline")
#pl.legend()
#pl.show()

