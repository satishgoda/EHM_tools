'''
twist calculator for splineIK joints
---------------------------------------

select spline_ik handle, base ctrl, end ctrl and run this


'''


import pymel.core as pm

spline_ikh = pm.ls(sl=True)[0]
limb_base_ctrl = pm.ls(sl=True)[1]
limb_end_ctrl = pm.ls(sl=True)[2]
limb_direction = 'x'

joints = spline_ikh.getJointList()

# BASE SETUP
#-----------
# limbBase_direction_aim parented to limb_base_ctrl
# limbBase_direction_aim positioned one unit in the direction of the limb segmenty joints
limbBase_direction_aim = pm.spaceLocator( n = "%s_direction_aim" % ( limb_base_ctrl.name() ) )
limbBase_direction_aim.setParent( limb_base_ctrl )
limbBase_direction_aim.translate.set(0,0,0)
limbBase_direction_aim.attr( 'translate'+limb_direction.upper() ).set(1)


# limbBase_direction pointConstraint to limb_base_ctrl
# limbBase_direction aimConstraint to limbBase_direction_aim
limbBase_direction = pm.spaceLocator( n = "%s_direction" % ( limb_base_ctrl.name() ) )
pm.pointConstraint( limb_base_ctrl, limbBase_direction )
pm.aimConstraint( limbBase_direction_aim, limbBase_direction )

if limb_direction == 'x':
	aimVector = (1,0,0)
elif limb_direction == 'y':
	aimVector = (0,1,0)
elif limb_direction == 'z':
	aimVector = (0,0,1)
pm.aimConstraint( limbBase_direction_aim, limbBase_direction, aimVector=aimVector, worldUpType="none" )



# limbBase_twist pointConstraint to limb_base_ctrl
# limbBase_twist orientConstraint to limbBase_direction
limbBase_twist = pm.spaceLocator( n = "%s_twist" % ( limb_base_ctrl.name() ) )
limbBase_twist.setParent( limb_base_ctrl )
limbBase_twist.translate.set(0,0,0)
pm.orientConstraint( limbBase_direction, limbBase_twist )



# END SETUP
#-----------
# limbEnd_direction_aim parented to limb_end_ctrl
# limbEnd_direction_aim positioned one unit in the direction of the limb segmenty joints
limbEnd_direction_aim = pm.spaceLocator( n = "%s_direction_aim" % ( limb_end_ctrl.name() ) )
limbEnd_direction_aim.setParent( limb_end_ctrl )
limbEnd_direction_aim.translate.set(0,0,0)
limbEnd_direction_aim.attr( 'translate'+limb_direction.upper() ).set(1)


# limbEnd_direction pointConstraint to limb_end_ctrl
# limbEnd_direction aimConstraint to limbEnd_direction_aim
limbEnd_direction = pm.spaceLocator( n = "%s_direction" % ( limb_end_ctrl.name() ) )
pm.pointConstraint( limb_end_ctrl, limbEnd_direction )
pm.aimConstraint( limbEnd_direction_aim, limbEnd_direction, aimVector=aimVector, worldUpType="none" )



# limbEnd_twist pointConstraint to limb_end_ctrl
# limbEnd_twist orientConstraint to limbEnd_direction
limbEnd_twist = pm.spaceLocator( n = "%s_twist" % ( limb_end_ctrl.name() ) )
limbEnd_twist.setParent( limb_end_ctrl )
limbEnd_twist.translate.set(0,0,0)
pm.orientConstraint( limbEnd_direction, limbEnd_twist )



# RESULT SETUP
#-----------
# reverse result of limbBase_twist and connect it to spline_IK_roll
limbBase_twist_mdn = pm.createNode ("multiplyDivide" , n = "%s_twist_mdn" % ( limb_base_ctrl.name() ) )
limbBase_twist.attr( 'rotate'+limb_direction.upper() ) >> limbBase_twist_mdn.input1.input1X
limbBase_twist_mdn.input2.input2X.set( -1 ) 
limbBase_twist_mdn.outputX >> spline_ikh.roll

# add up result of limbBase_twist to reverse result of limbEnd_twist and connect it spline_IK_twist
limbEnd_twist_mdn = pm.createNode ("multiplyDivide" , n = "%s_twist_mdn" % ( limb_end_ctrl.name() ) )
limbEnd_twist.attr( 'rotate'+limb_direction.upper() ) >> limbEnd_twist_mdn.input1.input1X 
limbEnd_twist_mdn.input2.input2X.set( -1 ) 

limbEnd_twist_pma = pm.createNode ("plusMinusAverage" , n = "%s_twist_pma" % ( limb_end_ctrl.name() ) )
limbEnd_twist_mdn.outputX >> limbEnd_twist_pma.input1D[0]
limbBase_twist.attr( 'rotate'+limb_direction.upper() ) >> limbEnd_twist_pma.input1D[1] 


limbEnd_twist_pma.output1D >> spline_ikh.twist