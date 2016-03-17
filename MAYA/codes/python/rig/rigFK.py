#===============================================================================
'''
jnts = pm.ls(sl=True)
RigFK( jnts = jnts )
RigFK()
prepares selected joint to be animatable as FK joints
'''
#===============================================================================

import pymel.core as pm

from codes.python.general import  colorize
Colorize = colorize.Colorize

from codes.python.general.lockHideAttr import  LockHideAttr
from codes.python.rig import jntToCrv
JntToCrv = jntToCrv.JntToCrv


def RigFK( jnts=None, side='L', ctrlSize=1.0, stretch=True, color='r' ):
	
	if not jnts:
		jnts = pm.ls( sl=True )
	else:
		jnts = pm.ls( jnts )
	# find color of the ctrls
	color = 'y'
	if side == 'L':
		color = 'r'
	elif side == 'R':
		color = 'b'
	
	shapes = []

	for jnt in jnts:
	
		if not jnt or not jnt.type()=='joint':
			pm.warning('ehm_tools...RigFK: %s was not a joint, skipped!'%jnt)

		
		shapes.append( (JntToCrv ( jnts = jnt , size = ctrlSize )).newShapes )
		LockHideAttr( objs=jnt, attrs='t' )
		LockHideAttr( objs=jnt, attrs='radius' )

		if stretch == True:
			# add length attribute and connect it to scale
			pm.addAttr (  jnt , ln = "length"  , at = "double"  , min = 0 , dv = 1 , k = True  )
			jnt.length >> jnt.scaleX
			LockHideAttr( objs=jnt, attrs='s' )

	Colorize( shapes=shapes, color=color )


	return shapes