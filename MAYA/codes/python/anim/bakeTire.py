# calculata car wheel rotation and bakes it
import pymel.core as pm
dt = pm.datatypes
import maya.mel as mel


def BakeTire():

	# tire = pm.PyNode( 'tire' ) # wheel node
	tire = pm.ls(sl=True)[0]
	diameter = 2.0

	try:
		diameter = tire.getShape().boundingBoxMaxZ.get() - tire.getShape().boundingBoxMinZ.get()
	except:
		pm.warning('Object\'s diamater could not be found, default of 2.0 was used.')   



	circumference = 3.14 * diameter
	carFront = pm.group( empty=True )
	carFrontGrp = pm.group()
	carFront.translateZ.set(1)
	pm.pointConstraint( tire, carFrontGrp)
	pm.orientConstraint( tire, carFrontGrp, skip=('x','z'))




	def getVectorChange( obj=None, obj2=None ):
		pm.currentTime( pm.currentTime(query=True)-1, e=True)
		Vec = dt.Vector( pm.xform( obj, q=True, ws=True, t=True) )
		FrontVec = dt.Vector( pm.xform( obj2, q=True, ws=True, t=True) )
		pm.currentTime( pm.currentTime(query=True)+1, e=True)
		return dt.Vector( FrontVec - Vec )

	def getTranslateChange( obj=None ):
		pm.currentTime( pm.currentTime(query=True)-1, e=True)
		Vec = dt.Vector( pm.xform( obj, q=True, ws=True, t=True) )
		pm.currentTime( pm.currentTime(query=True)+1, e=True) 
		FrontVec = dt.Vector( pm.xform( obj, q=True, ws=True, t=True) )      
		return dt.Vector( FrontVec - Vec )

	def getPreviousRotateX( obj=None):
		pm.currentTime( pm.currentTime(query=True)-1, e=True)
		rot = ( pm.xform( obj, q=True, ws=True, ro=True) )
		pm.currentTime( pm.currentTime(query=True)+1, e=True) 
		return rot[0]


	timeRange = mel.eval( 'timeControl -q -rangeArray $gPlayBackSlider' )
	if timeRange[1] - timeRange[0] < 2.0:
		timeRange =  [ 0, pm.playbackOptions( q=True, maxTime=True) ]
	
	pm.currentTime( timeRange[0] , edit=True)

	
	for frame in range( int(timeRange[0]),int(timeRange[1]) ):
		pm.currentTime( pm.currentTime(query=True)+1, e=True) 

		defaultVec = getVectorChange( tire, carFront ) # find how much car direction has changed from previous frame
		translateChange = getTranslateChange( tire ) # find how much car has moved
		translateInMult = translateChange.normal().dot( defaultVec ) # find a multiplier that shows how much car has moved forward.
		
		translateInZ = translateChange.length() * translateInMult # find how much has car moved forward.
		
		oldRx = getPreviousRotateX( tire ) # find wheel rotation in previous frame
		newRx = ( translateInZ / circumference * 360 ) +oldRx # calculate wheel's relative to previous frame rotation 
		tire.rotateX.set(newRx) # set new rotation for the wheel
		
		pm.setKeyframe( tire.rotateX ) # set a key for wheel's rotation

	pm.currentTime( timeRange[0], edit=True)

	pm.delete( carFrontGrp ) 