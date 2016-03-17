import pymel.core as pm

#===========================================================================================
# follicle By World Pos definition
#===========================================================================================
def FollicleByWorldPos( sources=None, surf=None, parent=True ):

	if not ( surf and sources ):
		selectedObjs = pm.ls(sl=True)
		sources = pm.ls( selectedObjs[:-1] )
		surf = pm.ls( selectedObjs[-1] )
	else:
		sources = pm.ls( sources )
		surf = pm.ls( surf )
	

	surfShape = surf[0].getShape()
	folList = []
	folShapeList = []
	for source in sources:
		# create closet point on surface node
		# in order to find the U and V parameters on the surface for placing follicles
		#=====================================================================
		folWorldPos = pm.xform( source, q=True, t=True, ws=True )
		if surfShape.type() == 'mesh':

			pOnSurf = pm.createNode('closestPointOnMesh')
			surfShape.worldMatrix[0] >> pOnSurf.inputMatrix;
			surfShape.worldMesh[0] >> pOnSurf.inMesh

			pOnSurf.inPosition.set( folWorldPos )

			uPos = ( pOnSurf.result.parameterU.get() )
			vPos = ( pOnSurf.result.parameterV.get() )
			U =  uPos
			V =  vPos

		elif surfShape.type() == 'nurbsSurface':
			pOnSurf = pm.createNode('closestPointOnSurface')
			surfShape.worldSpace >> pOnSurf.inputSurface
		
		
			pOnSurf.inPosition.set( folWorldPos )


			maxU = surfShape.minMaxRangeU.maxValueU.get()
			maxV = surfShape.minMaxRangeV.maxValueV.get()
			pOnSurf.inPosition.set( folWorldPos )
			uPos = ( pOnSurf.result.parameterU.get() )
			vPos = ( pOnSurf.result.parameterV.get() )

			# U and V parameters are not normalized so we have to calcutate them
			U =  uPos / maxU
			V =  vPos / maxV




		#  now that we have U and V parameters, we can create folliclethe node
		#=====================================================================
		folShape = pm.createNode('follicle' )

		folShape.parameterU.set( U )
		folShape.parameterV.set( V )

		fol = folShape.getParent()
		pm.rename( fol, '%s_flc'%source.name() )

		if surfShape.type() == 'mesh':
			surfShape.outMesh >> folShape.inputMesh
			surfShape.worldMatrix[0] >> folShape.inputWorldMatrix

		elif surfShape.type() == 'nurbsSurface':
			surfShape.local >> folShape.inputSurface
			surfShape.worldMatrix[0] >> folShape.inputWorldMatrix

		folShape.outRotate >> fol.rotate
		folShape.outTranslate >> fol.translate

		folList.append( fol )
		folShapeList.append( folShape )
		# now that we've created follicle we can clean up extra nodes.
		pm.delete(pOnSurf)

		if parent:
			pm.parent( source, fol )
	return ( folList, folShapeList )
