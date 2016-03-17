# ---------------------------------------------------------------------------------
# synopsis : 			oriJnt ()
#
# what does this script do ?	 orient joints using aim constraint
#
#
# how to use:        needs an upVector for aim and an axis to point to upVector
#                    It automatically aims +x axis to child joint
#
# ---------------------------------------------------------------------------------

import pymel.core as pm

def OriJnt( jnt=None, upAim=None, aimAxis='z'):

	if jnt==None or upAim==None:
		temp = pm.ls(sl=True)
		jnts = temp[ : len(temp)-1 ]
		upAim = temp[ len(temp)-1 ]
	else:
		jnts = pm.ls(jnt)
	
	for jnt in jnts:
		if aimAxis == 'x':
			axis = (1,0,0)     
		elif aimAxis == '-x':
			axis = (-1,0,0)    
		elif aimAxis == 'y':
			axis = (0,1,0)
		elif aimAxis == '-y':
			axis = (0,-1,0)
		elif aimAxis == 'z':
			axis = (0,0,1)
		elif aimAxis == '-z':
			axis = (0,0,-1)        
		# unparent joing before aim constraining
		child = jnt.getChildren()
		pm.parent(child, w=True)
		#pm.makeIdentity ( jnts[0] , apply = True , r = 1 )
		tempAim = pm.aimConstraint ( child
					, jnt
					, mo  = False
					, offset = (0,0,0)  
					, weight = 1 
					, aimVector = (1,0,0) 
					, upVector = axis 
					, worldUpType = "object" 
					, worldUpObject = upAim  )
		# delete aim constraint
		pm.delete ( tempAim )
		# freeze the joint
		pm.makeIdentity ( jnt , apply = True , r = 1 )
		pm.parent( child , jnt )

