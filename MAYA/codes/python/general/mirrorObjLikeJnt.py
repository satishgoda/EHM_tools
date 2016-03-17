# ====================================================================
# mirrorObjLikeJnt()
# mirrors selected objects the way you mirror joints in behavior mode
# return newly created object
# ====================================================================

import pymel.core as pm

from codes.python.general import reverseShape

def MirrorObjLikeJnt( objs=None, returnValue=False ):
	
	if objs==None:
		objs = pm.ls( sl=True )
	else:
		objs = pm.ls( objs )
	
	
	newObjs = []
	values = []
		
	for obj in objs:
		nameSpaceAndName = obj.name().split(":")
		if len( nameSpaceAndName ) > 1:
			objNameSpace = nameSpaceAndName[0]
			objName = nameSpaceAndName[1]
		else:
			objName = obj.name()		
		if objName[:2]==('L_'):
			side = 'L'
			otherSide = 'R'
		elif objName[:2]==('R_'):
			side = 'R'
			otherSide = 'L'			
		else:
			side = ''
			otherSide = ''		
		
		origParent = obj.getParent()
		
		scale = obj.scale.get()
		obj.scale.set( 1,1,1 )
		
		pm.select( obj )

		jnt = pm.joint()

		pm.parent( jnt , w=True )
		pm.parent( obj, jnt )

		newJntStrings = pm.ls( pm.mirrorJoint( jnt, mirrorYZ=True, mirrorBehavior=True ) )
		for newJntString in newJntStrings:
			newName = newJntString.replace( side, otherSide  )[:-1]
			try:
				pm.rename( newJntString , newName )
			except:
				pass
		
		obj.scale.set( scale )
		
		newJnt = newJntStrings[0]
		newObj = newJntStrings[1]

		if not origParent:
			pm.parent( obj		, world=True )
			pm.parent( newObj	, world=True )
		else:
			pm.parent( obj		, origParent )
			pm.parent( newObj	, origParent )

		pm.delete( jnt , newJnt )
		reverseShape.ReverseShape( newObj )
		newObjs.append( newObj )
		newObj.scale.set( scale )		
		if returnValue:
			pos = pm.xform( newObj, q=True, ws=True, t=True )
			rot = pm.xform( newObj, q=True, ws=True, ro=True )
			values.append( (pos,rot) )
			
	if returnValue:
		pm.delete(newObjs)
		return values
	else:
		return newObjs
