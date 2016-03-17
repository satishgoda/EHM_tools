# ---------------------------------------------------------------------------------
# synopsis : 			makeIkStretchy ()
#
# what does this script do ?	 make ik chains stretchy
#
#
# how to use:        just give this your ikhandle
#
# ---------------------------------------------------------------------------------

import pymel.core as pm

def WorldPos( obj ):
	try:
		return pm.xform( obj,q=True,t=True,ws=True )
	except:
		raise Exception( 'ehm_tools...makeIkStretchy.WorldPos: could not query world position of object %s'%obj )



def MakeIkStretchy( ikh=None, elbowLock=True ):

	if ikh==None:
		ikh = pm.ls(sl=True)[0]

	locs = []
	dists = []

	# find joints connected to ikh
	mustStrechJnts = ikh.getJointList()
	endEffector = ikh.getEndEffector()


	if len(mustStrechJnts) > 1 : # more than one joint, meaning RPSolver

		# positions
		uplegPos =  WorldPos(mustStrechJnts[0])
		kneePos =  WorldPos(mustStrechJnts[1])
		kneeEndPos =  WorldPos(endEffector)

		# create locators and distance nodes
		uplegLoc = pm.spaceLocator()
		pm.rename( uplegLoc, "%s_stretch_start_loc"% ikh.name() )
		uplegLoc.translate.set( uplegPos )
		
		kneeLoc = pm.spaceLocator()
		pm.rename( uplegLoc, "%s_stretch_mid_loc"% ikh.name() )
		kneeLoc.translate.set( kneePos )
		
		kneeEndLoc = pm.spaceLocator()
		kneeEndLoc.translate.set( kneeEndPos )
		pm.rename( uplegLoc, "%s_stretch_end_loc"% ikh.name() )


		locs.append(uplegLoc)
		locs.append(kneeLoc)
		locs.append(kneeEndLoc)

		pm.select(uplegLoc, kneeLoc)
		uplegDistShape = pm.distanceDimension ()
		pm.select(kneeLoc, kneeEndLoc)
		kneeDistShape = pm.distanceDimension ()
		pm.select(uplegLoc, kneeEndLoc)
		legDistShape = pm.distanceDimension ()

		uplegDist = uplegDistShape.getParent()
		kneeDist = kneeDistShape.getParent()
		legDist = legDistShape.getParent()

		dists.append(uplegDist)
		dists.append(kneeDist)
		dists.append(legDist)

		pm.parent ( ikh , kneeEndLoc )

		# make ik joints stretchy
		defaultIKLegLen = uplegDistShape.distance.get() + kneeDistShape.distance.get()

		stretch_mdn = pm.createNode ("multiplyDivide" , n = "%s_stretch_mdn" % ( ikh.name() ) )
		stretch_mdn.input2X.set( defaultIKLegLen )
		legDistShape.distance >> stretch_mdn.input1X
		stretch_mdn.operation.set(2)

		stretch_cnd = pm.createNode ("condition" , n = "%s_stretch_cnd"% ( ikh.name() ) )
		legDistShape.distance >> stretch_cnd.firstTerm
		stretch_cnd.secondTerm.set(defaultIKLegLen)
		stretch_cnd.operation.set(2)

		stretch_mdn.outputX >> stretch_cnd.colorIfTrueR



		# stretch switch
		stretchSwitch_bln = pm.createNode ("blendColors" , n = "%s_stretchSwitch_bln" % ( ikh.name() ) )

		stretch_cnd.outColorR >> stretchSwitch_bln.color1R
		stretchSwitch_bln.color2R.set(1)


		# conncet result
		for jnt in mustStrechJnts:
			stretchSwitch_bln.outputR >> jnt.scaleX

		# create swtich attribute on last locator
		pm.addAttr(kneeEndLoc,  keyable=True, attributeType="double", min=0, max=1, defaultValue=1, longName="stretchable")
		kneeEndLoc.stretchable >> stretchSwitch_bln.blender


		#================================================================================
		# Elbow Lock
		if elbowLock==True:

			pm.addAttr ( kneeLoc ,dv = 0 ,min=0 ,max=10 , keyable =  True , ln = "elbowLock" , at = "double")

			defaultIKUpArmLen = pm.getAttr ( uplegDist.distance )
			elbowLock_mdn = pm.createNode ("multiplyDivide" , n = ikh.name()  + "_elbowLock_mdn" )
			pm.setAttr ( elbowLock_mdn.input2X, defaultIKUpArmLen )
			uplegDist.distance >> elbowLock_mdn.input1X
			pm.setAttr ( elbowLock_mdn.operation, 2 )


			defaultIKElbowLen = pm.getAttr ( kneeDist.distance )
			IKelbowLock_mdn = pm.createNode ("multiplyDivide" , n = ikh.name()  + "_elbowLock_mdn" )
			pm.setAttr ( IKelbowLock_mdn.input2X, defaultIKElbowLen )
			kneeDist.distance >> IKelbowLock_mdn.input1X
			pm.setAttr ( IKelbowLock_mdn.operation, 2 )


			#================================================================================
			# make elbowLock more animation friendly by dividing it by 10

			elbowLockAnimFriend_mdn = pm.createNode ("multiplyDivide" , n = ikh.name()  + "_elbowLockAnimFriend_mdn" )
			pm.setAttr ( elbowLockAnimFriend_mdn.input2X, 10 )
			pm.setAttr ( elbowLockAnimFriend_mdn.operation, 2 )
			kneeLoc.attr ( "elbowLock" )    >>      elbowLockAnimFriend_mdn.input1X


			#================================================================================
			# conncet result of stretch and elbow lock to joint with a blend switch on the elbow locator
			stretchUparmLock_bta     =                   pm.createNode ("blendTwoAttr" , n = ikh.name()  + "_stretchUparmLock_bta" )
			elbowLockAnimFriend_mdn.outputX      >>      stretchUparmLock_bta.attributesBlender
			stretchSwitch_bln.outputR            >>      stretchUparmLock_bta.input[0]
			elbowLock_mdn.outputX                >>      stretchUparmLock_bta.input[1]
			stretchUparmLock_bta.output          >>      mustStrechJnts[0].scaleX

			stretchElbowLock_bta     =                   pm.createNode ("blendTwoAttr" , n = ikh.name()  + "_stretchElbowLock_bta" )
			elbowLockAnimFriend_mdn.outputX      >>      stretchElbowLock_bta.attributesBlender
			stretchSwitch_bln.outputR            >>      stretchElbowLock_bta.input[0]
			IKelbowLock_mdn.outputX              >>      stretchElbowLock_bta.input[1]
			stretchElbowLock_bta.output          >>      mustStrechJnts[1].scaleX

	elif len(mustStrechJnts) == 1 : # one jnt meaning SCSolver
		# positions
		uplegPos =  WorldPos(mustStrechJnts[0])
		kneeEndPos =  WorldPos(endEffector)

		# create locators and distance nodes
		uplegLoc = pm.spaceLocator()
		uplegLoc.translate.set( uplegPos )
		kneeEndLoc = pm.spaceLocator()
		kneeEndLoc.translate.set( kneeEndPos )

		locs.append(uplegLoc)
		locs.append(kneeEndLoc)

		pm.select(uplegLoc, kneeEndLoc)
		legDistShape = pm.distanceDimension ()

		legDist = legDistShape.getParent()

		dists.append(legDist)

		pm.parent ( ikh , kneeEndLoc )

		# make ik joints stretchy
		defaultIKLegLen = legDistShape.distance.get()

		stretch_mdn = pm.createNode ("multiplyDivide" , n = "%s_stretch_mdn" % ( ikh.name() ) )
		stretch_mdn.input2X.set( defaultIKLegLen )
		legDistShape.distance >> stretch_mdn.input1X
		stretch_mdn.operation.set(2)


		# stretch switch
		stretchSwitch_bln = pm.createNode ("blendColors" , n = "%s_stretchSwitch_bln" % ( ikh.name() ) )
		stretch_mdn.outputX >> stretchSwitch_bln.color1R
		stretchSwitch_bln.color2R.set(1)

		# conncet result
		for jnt in mustStrechJnts:
			stretchSwitch_bln.outputR >> jnt.scaleX

		# create swtich attribute on last locator
		pm.addAttr(kneeEndLoc,  keyable=True, attributeType="double", min=0, max=1, defaultValue=1, longName="stretchable")
		kneeEndLoc.stretchable >> stretchSwitch_bln.blender


	return ( locs, dists)