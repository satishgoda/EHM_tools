import pymel.core as pm

def NoJointInViewport( jnts=None ) :
	
	if jnts==None:
		jnts = pm.ls (sl = True)
	else:
		jnts = pm.ls( jnts )
	
	for jnt in jnts:
		if jnt.type() == 'joint':
			jnt.drawStyle.set( 2 )