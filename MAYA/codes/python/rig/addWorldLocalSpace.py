
'''
add space swith to selected control

1. first parent your control under the default control ( for example: parent your hand_IK_ctrl under torso_ctrl )
2. select control object that you want to add the "local-world" space switch for ( for example: hand_IK_ctrl )
3. shift select the object you as world ( for example:  main_control or COG_control )
4. run this

'''


import pymel.core as pm


def AddWorldLocalSpace(**kwargs ):
	"""
	select control object and a world control object, then run this. see script editor for more info.
	1. first parent your control under the default control ( for example: parent your hand_IK_ctrl under torso_ctrl )
	2. select control object that you want to add the "local-world" space switch for ( for example: hand_IK_ctrl )
	3. shift select the object you as world ( for example:  main_control or COG_control )
	4. run this
	"""	
	ctrl = kwargs.setdefault( 'ctrl' ) # object you want to create space switch for
	worldCtrl = kwargs.setdefault( 'worldCtrl' ) # world space node
	point = kwargs.setdefault( False )
	orient = kwargs.setdefault( False )

	objs = pm.ls(sl=True)
	
	if len(objs) != 2:
		pm.error( helpMessage )
	
	ctrl = objs[0]
	worldCtrl = objs[1]
	
	# create three zero groups matching the transfrom of selected control
	zeroGrp = pm.group( empty=True, name='%s_space'%ctrl.name() )
	pm.delete( pm.pointConstraint( ctrl, zeroGrp ) )
	pm.delete( pm.orientConstraint( ctrl, zeroGrp ) )

	localGrp = pm.duplicate( zeroGrp )[0]
	pm.rename( localGrp, '%s_spacelocal'%ctrl.name() )

	worldGrp = pm.duplicate( zeroGrp )[0]
	pm.rename( worldGrp, '%s_spaceworld'%ctrl.name() )


	# parent one under first parent and the other under second parent
	ctrlParent = ctrl.getParent()
	pm.parent( zeroGrp, ctrlParent )
	pm.parent( localGrp, ctrlParent )
	pm.parent( worldGrp, worldCtrl )
	pm.parent( ctrl, zeroGrp )


	# orient constraint zero group with two copied nulls as drivers
	if orient:
		const = pm.orientConstraint( worldGrp, localGrp, zeroGrp ) 	
	elif point:
		const = pm.pointConstraint( worldGrp, localGrp, zeroGrp ) 
	else: #parent
		const = pm.parentConstraint( worldGrp, localGrp, zeroGrp ) 	

	# add parentTo attribute with value '---------' and lock it
	pm.addAttr( ctrl, ln='parentTo', keyable=True, at="enum", en='---------' )
	pm.setAttr( ctrl.parentTo, lock=True )

	# make world_local attribute with the range 0-1 and connect it second weight of orient constraint
	pm.addAttr( ctrl, ln='world_local', nn='world <---> local', keyable=True, at="double", min=0.0, max=1.0 )
	ctrl.world_local	>>		const.attr( ('%sW1'%localGrp.name()) )


	# create reverse and connect it to second weight
	revNode = pm.createNode( 'reverse', name='%s_worldlocal_rev'%ctrl.name() )
	ctrl.world_local	>>		revNode.inputX
	revNode.outputX		>>		const.attr( '%sW0'%worldGrp.name() )