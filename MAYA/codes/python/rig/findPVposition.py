'''
objs = pm.ls(sl=True)
FindPVposition( objs=objs )

This script guesstimates the best location of pole vectors in world space
ie: give it uparm, elbow and hand joints to find the best polevector position

returns None if limbs are straight

'''

import pymel.core as pm
dt = pm.datatypes

def FindPVposition( objs=pm.ls(sl=True) ):

	if not len(objs) == 3:
		pm.error( 'ehm_tools...findPVposition: objs arguments takes exactly 3 objects. %s was given.'%len(objs) )

	base = objs[0]
	mid  = objs[1]
	tip  = objs[2]

	A = dt.Vector( pm.xform( base, q=True, t=True, ws=True ) )
	B = dt.Vector( pm.xform( mid, q=True, t=True, ws=True ) )
	C = dt.Vector( pm.xform( tip, q=True, t=True, ws=True ) )

	AC = C - A
	AB = B - A

	D =  A + ( (dt.dot(AB,AC.normal()))  * AC.normal() ) # AB projected on AC

	position =  B + B - D
	
	if (position[0]  - B[0] < 0.001) and (position[1]  - B[1] < 0.001) and (position[2]  - B[2] < 0.001):
		pm.warning( 'ehm_tools...FindPVposition: Limbs were straight. None was returned!' )
		return None
	else:
		return position

	
	
		
