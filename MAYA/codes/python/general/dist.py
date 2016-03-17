import pymel.core as pm
dt = pm.datatypes

#============================================================================
# find distance between to points
#============================================================================
def Dist( base=None, tip=None ):

	if base==None or tip==None:
		base,tip = pm.ls(sl=True)

	baseVec = dt.Vector(  pm.xform( base, q=True, t=True, ws=True ) )
	tipVec  = dt.Vector(  pm.xform( tip , q=True, t=True, ws=True ) )
	vec = tipVec - baseVec
	fullLen = vec.length()
	return fullLen


