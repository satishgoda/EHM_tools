# connects seleted objects to selected curve's shape

sels = pm.ls( sl=True )
locs = sels[:-1]
curveNode = sels[-1]
curveShape = curveNode.getShape()


for loc in locs:
	
	
	# find the parametric position of the loc on the curve
	locWorldPos = pm.xform( loc, q=True, t=True, ws=True )

	pOnSurf = pm.createNode('nearestPointOnCurve')

	curveShape.worldSpace[0] >> pOnSurf.inputCurve

	pOnSurf.inPosition.set( locWorldPos )

	uPos = ( pOnSurf.result.parameter.get() )
	parametricPosition =  uPos
	
	pm.delete( pOnSurf )


	# create pointOnCurveInfo node and using it connect loc to curve

	pointOnCurveNode = pm.createNode( "pointOnCurveInfo" )

	curveShape.worldSpace[0]		>>		pointOnCurveNode.inputCurve



	pointOnCurveNode.position		>>		loc.translate

	pointOnCurveNode.parameter.set( parametricPosition )