# reverses the shape of selected object in the specified direction
#-----------------------------------------------------------------------------------------------------------------

import pymel.core as pm

def ReverseShape(  objs=None, axis='x' ):
	
	scaleValue = ( -1, 1, 1 )
	if axis == 'y':
		scaleValue = ( 1, -1, 1 )
	elif axis == 'z':
		scaleValue = ( 1, 1, -1 )
	elif axis != 'x':
		pm.warning('Axis was not correct, used "x" axis instead.')
	
	if objs == None:
		objs = pm.ls( sl=True )
	else:
		objs = pm.ls( objs )
	
	for obj in objs:
		try:
			shape = obj.getShape()
			if shape.type() == 'mesh':
				pm.select( shape.vtx[:] )
				pm.scale( scaleValue )
				pm.select( objs )
			elif shape.type() == 'nurbsCurve':
				pm.select( shape.cv[:] )
				pm.scale( scaleValue )
				pm.select( objs )			
		except:
			pm.warning("Object doesn't have a shape. Skipped!")

		'''
		else:
			pm.warning('general.reverseShape() : %s is not a mesh or curve, skipped.' %( obj ) )     
		'''