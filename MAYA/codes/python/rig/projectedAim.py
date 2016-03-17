'''
find projected on the floor rotation Y of the object 2 around object 1 
shoot = pm.ls(sl=True)
ProjectedAim( objs=shoot )

'''
import pymel.core as pm
import math
dt = pm.datatypes


def ProjectedAim( objs = pm.ls(sl=True), fullCircle=True ):
	objs = pm.ls( objs )
	if not objs:
		pm.error('ehm_tools...projectedAim: objs arugument accepts two object!' )

	if not len( objs )==2:
		pm.error('ehm_tools...projectedAim: objs arugument accepts two object!' )

	APos = pm.xform( objs[0], q=True, t=True, ws=True )
	BPos = pm.xform( objs[1], q=True, t=True, ws=True )

	A = dt.Vector( APos[0], 0, APos[2]  )
	B = dt.Vector( BPos[0], 0, BPos[2]  )

	AB_norm = (B - A).normal()
	

	x =  dt.degrees( math.acos( AB_norm[0] ) )

	if math.asin( AB_norm[2] ) > 0.0 :
		if fullCircle==True:
			x = 360 - x
		else:
			x = - x

	return x