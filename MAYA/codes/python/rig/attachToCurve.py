# ---------------------------------------------------------------------------------
'''
synopsis : 			AttachToCurve( worldPos , crv )

what does this script do ?	 create and attach locators on a curve using a world position of the locator

flags :				crv [nurbsCurve]	                =>  curve you want to parent objects to
					worldPos [float,float,float]		=>  position of the object you want to be attached to curve 

how to use:
    
1. run the whole code once. 

2. first, select the object you want to attach to a curve and then the curve:    

3. run four lines below:

objs = pm.ls(sl=True)
objPos = pm.xform( objs[0], q=True, t=True, ws=True )
loc = AttachToCurve( worldPos=objPos , crv=objs[1]  )
objs[0].setParent( loc )


Author: Ehsan HM
'''
# ---------------------------------------------------------------------------------


import pymel.core as pm

def AttachToCurve( createNewLocator=False, objectToConnect=None, worldPos=(0,0,0), crv=None ):
	if objectToConnect==None:
		objectToConnect = pm.ls(sl=True)[0]	
	if crv==None:
		crv = pm.ls(sl=True)[-1]
	if crv.type() != 'nurbsCurve':
		crvShape = crv.getShape()
		if crvShape.type() != 'nurbsCurve' :
			pm.error("Select and object to attach to curve then shift select the curve.")		
	else:
		crvShape = crv
		
	# create nearest point on Curve node 
	# in order to find the U  parameter on the Curve
	# to place the locator there
	#=====================================================================
	pOnCrv = pm.createNode('nearestPointOnCurve')
	
	crvShape.worldSpace >> pOnCrv.inputCurve
	pOnCrv.inPosition.set( worldPos )
	
	U = ( pOnCrv.result.parameter.get() )
	
	#  now that we have U parameters, we can create locator node
	#=====================================================================
	if createNewLocator:
		loc = pm.spaceLocator()
	else:
		loc = objectToConnect
	
	locShape = loc.getShape()
	
	motionPath = pm.createNode("motionPath")
	
	motionPath.uValue.set( U )
	
	crvShape.worldSpace >> motionPath.geometryPath
	motionPath.allCoordinates >> loc.translate
	
	# now that we've created locator we can clean up extra nodes.
	pm.delete(pOnCrv)
	
	return ( loc, locShape )