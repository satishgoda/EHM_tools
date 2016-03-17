# create extra controls for selected joints

import pymel.core as pm

from codes.python.rig import zeroGrp
reload( zeroGrp )
ZeroGrp = zeroGrp.ZeroGrp

from codes.python.curves import cubeCrv
reload( cubeCrv )
CubeCrv = cubeCrv.CubeCrv


def ExtraControlForJnt( jnts=None ) :

	if not jnts:
		jnts = pm.ls( sl=True )
	else:
		jnts = pm.ls( jnts )
	
	
	for jnt in jnts:
		
		# duplicate joint
		pm.select( clear=True )
		newJnt = pm.joint( p = [0,0,0], name= '%s_extra'%jnt.name() )
		pm.delete( pm.pointConstraint( jnt, newJnt ) )
		pm.delete( pm.orientConstraint( jnt, newJnt ) )
		pm.parent( newJnt, jnt )
		newJnt.jointOrient.set( jnt.jointOrient.get() )
		
		# create control curve for joint
		ctrl = CubeCrv( name = '%s_ctrl'%jnt.name() )
		pm.delete( pm.pointConstraint( jnt, ctrl ) )
		pm.delete( pm.orientConstraint( jnt, ctrl ) )
		zeroAndOfs = ZeroGrp( ctrl )
		ctrl.translate >> newJnt.translate
		ctrl.rotate >> newJnt.rotate
		ctrl.scale >> newJnt.scale
        
		# make controls to move with base joints
		pm.parentConstraint( jnt, zeroAndOfs[0] )
		pm.scaleConstraint( jnt, zeroAndOfs[0] )