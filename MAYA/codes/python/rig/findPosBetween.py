# find Pos Between to objects by a precent

import pymel.core as pm
import pymel.core.datatypes as dt

def FindPosBetween( **kwargs ):
	percent = kwargs.setdefault( 'percent' , 50 )
	base = kwargs.setdefault( 'base' )
	tip = kwargs.setdefault( 'tip' )


	if not ( base and tip ):
		base,tip = pm.ls(sl=True)

	baseVec = dt.Vector(  pm.xform( base, q=True, t=True, ws=True ) )
	tipVec  = dt.Vector(  pm.xform( tip , q=True, t=True, ws=True ) )
	vec = tipVec - baseVec
	normVec =  vec.normal()
	fullLen = vec.length()
	partialVec = normVec * fullLen / 100.0 * percent
	finalVec = partialVec + baseVec
	return finalVec
