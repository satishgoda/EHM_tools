import pymel.core as pm
from codes.python.rig import zeroGrp
ZeroGrp = zeroGrp.ZeroGrp

def Finger( rootJnts=None ):
	
	if not rootJnts:
		rootJnts = pm.ls( sl=True )
	else:
		rootJnts = pm.ls( rootJnts )


	for rootJnt in rootJnts:
		
		jnts = pm.listRelatives( rootJnt, ad=True )
		jnts.append( rootJnt )
		jnts.reverse()
		
		
		# create ctrls with zero groups for each joint
		ctrls = []
		
		for i in range( len(jnts)-1 ):
			ctrls.append( pm.curve(	  d = 1
									, p = [ (0, -1, 1), (0, 1, 1),  (0, 1, -1),  (0, -1, -1),  (0, -1, 1) ]		
									, k = [0, 1, 2, 3, 4]
									, name='%s_ctrl'%jnts[i].name() )
						)
			pm.delete( pm.pointConstraint( jnts[i], ctrls[i] ) )
			pm.delete( pm.orientConstraint( jnts[i], ctrls[i] ) )
			
			try:
				pm.parent( ctrls[i], ctrls[i-1] )
			except:
				try:
					pm.parent( ctrls[i], world=True )
				except:
					pass
		
		
		# create zero groups
		ctrlsZerosAndOfss = ZeroGrp( ctrls )
		ctrlsZeros = ctrlsZerosAndOfss[0]
		ctrlsOfss = ctrlsZerosAndOfss[1]
		
		jntsZerosAndOfss = ZeroGrp( jnts )
		jntsZeros = jntsZerosAndOfss[0]
		jntsOfss = jntsZerosAndOfss[1]
		
		
		# connect transforms of ctrls to joints
		for i in range( len( ctrlsZeros ) ):
			ctrls[i].translate		>>		jntsOfss[i].translate
			ctrls[i].rotate			>>		jntsOfss[i].rotate
			ctrls[i].scale			>>		jntsOfss[i].scale
		
		
		
		# create a group for reverse scale
		ctrlScaleGrps=[]
		jntScaleGrps=[]
		for i in range( len(jnts)-1 ):
			# create one for each ctrl
			ctrlScaleGrps.append( pm.group( em=True, name='%s_ctrl_scaleGrp'%jnts[i].name() ) )
		
			if i == len(jnts): # if last joint, no need to position as where child is
				pm.delete( pm.pointConstraint( jnts[i], ctrlScaleGrps[i] ) )
			else:
				pm.delete( pm.pointConstraint( jnts[i+1], ctrlScaleGrps[i] ) )
			pm.delete( pm.orientConstraint( jnts[i], ctrlScaleGrps[i] ) )			
			
			
			# we need one more for each jnt as well
			jntScaleGrps.append( pm.duplicate( ctrlScaleGrps[i])[0] )
			pm.rename( jntScaleGrps[i], '%s_jnt_scaleGrp'%jnts[i].name() )
			
			
			# set hierarchy
			if i < len(jnts)-2: # if last ctrl, do not parent anything under it
				ctrlScaleGrps[i].setParent( ctrls[i] )
				ctrlsZeros[i+1].setParent( ctrlScaleGrps[i] )
			else:
				ctrlScaleGrps[i].setParent( ctrls[i] )
			
			if i < len(jnts)-1: # if last joint, do not parent anything under it
				jntScaleGrps[i].setParent( jnts[i] )
				jntsZeros[i+1].setParent( jntScaleGrps[i] )		
					
		# reverse the scale and connect it to next ctrlScaleGrps		
		for i in range( len(ctrlsZeros)-1 ):	
			scaleRev = pm.createNode( 'multiplyDivide', name='%s_scaleRev'%ctrlsZeros[i].name() )
			scaleRev.input1.set(1,1,1)
			scaleRev.operation.set(2)
			ctrls[i].scale			>>		scaleRev.input2
			scaleRev.output			>>		ctrlScaleGrps[i].scale
			
		for i in range( len(jntsZeros)-1 ):	
			scaleRev = pm.createNode( 'multiplyDivide', name='%s_scaleRev'%jntsZeros[i].name() )
			scaleRev.input1.set(1,1,1)
			scaleRev.operation.set(2)
			jntsOfss[i].scale		>>		scaleRev.input2
			scaleRev.output			>>		jntScaleGrps[i].scale