import pymel.core as pm
from codes.python.rig import zeroGrp
ZeroGrp = zeroGrp.ZeroGrp


rootJnts = pm.ls( sl=True )

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
	
	
	# reverse the scale and connect it to next zeroGrp	
	for i in range( len(ctrlsZeros)-1 ):	
		scaleRev = pm.createNode( 'multiplyDivide', name='%s_scaleRev'%ctrlsZeros[i].name() )
		scaleRev.input1.set(1,1,1)
		scaleRev.operation.set(2)
		ctrls[i].scale			>>		scaleRev.input2
		scaleRev.output			>>		ctrlsZeros[i+1].scale
		
	for i in range( len(jntsZeros)-1 ):	
		scaleRev = pm.createNode( 'multiplyDivide', name='%s_scaleRev'%jntsZeros[i].name() )
		scaleRev.input1.set(1,1,1)
		scaleRev.operation.set(2)
		jntsOfss[i].scale		>>		scaleRev.input2
		scaleRev.output			>>		jntsZeros[i+1].scale